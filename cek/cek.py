"""Tugas 6 — cek.py <folder>: pendeteksi TODO, fungsi panjang, file error.

Fitur:
  1. Komentar TODO/FIXME            -> <file>:<baris>: teks komentar
  2. Fungsi ber-body > 30 baris     -> <file>:<baris>: fungsi '<nama>' N baris
  3. File yang pohonnya bererror    -> <file>: ERROR/MISSING pertama + baris

[Pengayaan] mendukung Python (.py) dan JavaScript (.js).
Semua fungsi dihitung — termasuk method di kelas dan fungsi bersarang.
Untuk JS, arrow function tanpa nama tidak dihitung (tidak punya
field name); function_declaration, generator_function_declaration, dan
method_definition dihitung.

Pemakaian: python cek.py <folder>
"""
import sys
from pathlib import Path

import tree_sitter_javascript as tsjs
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
JS = Language(tsjs.language())

BAHASA = {
    ".py": {
        "parser": Parser(PY),
        "todo": Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))'),
        "fungsi": Query(
            PY, '(function_definition name: (identifier) @nama) @fungsi'
        ),
    },
    ".js": {
        "parser": Parser(JS),
        "todo": Query(JS, '((comment) @c (#match? @c "TODO|FIXME"))'),
        "fungsi": Query(
            JS,
            """
            (function_declaration name: (identifier) @nama) @fungsi
            (generator_function_declaration name: (identifier) @nama) @fungsi
            (method_definition name: (property_identifier) @nama) @fungsi
            """,
        ),
    },
}

LEWATI = {"venv", ".git", "node_modules", "__pycache__", "target", "dist"}


def cari_error(node):
    """Node ERROR/MISSING pertama secara preorder, atau None."""
    if node.is_error or node.is_missing:
        return node
    for c in node.children:
        hasil = cari_error(c)
        if hasil is not None:
            return hasil
    return None


def teks(node):
    return (node.text or b"").decode("utf-8", errors="replace").strip()


def cek_file(path, lang):
    tree = lang["parser"].parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME (contoh dari materi)
    for node in QueryCursor(lang["todo"]).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {teks(node)}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(lang["fungsi"]).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = teks(cap["nama"][0])
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > 30:
            print(f"{path}:{fungsi.start_point[0] + 1}: "
                  f"fungsi '{nama}' {jumlah} baris (>30)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        n = cari_error(tree.root_node)
        jenis = "MISSING" if n.is_missing else "ERROR"
        print(f"{path}: pohon bererror -- {jenis} '{n.type}' "
              f"di baris {n.start_point[0] + 1}")


def main():
    root = Path(sys.argv[1])
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if set(path.parts) & LEWATI:
            continue
        lang = BAHASA.get(path.suffix.lower())
        if lang is not None:
            cek_file(path, lang)


if __name__ == "__main__":
    main()
