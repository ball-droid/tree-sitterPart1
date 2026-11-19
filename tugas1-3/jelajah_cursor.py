"""Tugas 2 — Penjelajah node [Pengayaan] versi TreeCursor.

Versi kedua dari jelajah.py yang memakai TreeCursor
(goto_first_child / goto_next_sibling / goto_parent) alih-alih rekursi.
Output harus IDENTIK dengan jelajah.py untuk file apa pun.
Node anonim dilewati: tidak dicetak dan subtree-nya tidak ditelusuri,
sama seperti versi rekursif.
"""
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def cetak(node, kedalaman, field):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")


def jelajah_cursor(tree):
    cursor = tree.walk()
    kedalaman = 0
    cetak(cursor.node, kedalaman, cursor.field_name)  # root selalu bernama
    masuk = True
    while True:
        if masuk and cursor.goto_first_child():
            kedalaman += 1
            if cursor.node.is_named:
                cetak(cursor.node, kedalaman, cursor.field_name)
                masuk = True
            else:
                masuk = False  # node anonim: jangan masuk subtree-nya
        else:
            # tidak bisa masuk lagi — cari saudara berikutnya
            while not cursor.goto_next_sibling():
                if not cursor.goto_parent():
                    return  # selesai, sudah kembali ke root
                kedalaman -= 1
            if cursor.node.is_named:
                cetak(cursor.node, kedalaman, cursor.field_name)
                masuk = True
            else:
                masuk = False


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah_cursor(tree)
