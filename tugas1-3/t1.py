"""Tugas 1 — Membaca pohon.

Parse potongan kode Python, cetak tree.root_node, lihat node anonim,
bandingkan children vs named_children, dan demonstrasi ERROR/MISSING.
Pohon perkiraan untuk tiap potongan ada di perkiraan-t1.txt (ditulis
sebelum skrip ini dijalankan).
"""
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

POTONGAN = {
    "1-fungsi": b"def sapa(nama):\n    return nama\n",
    "2-if-else": b'if x > 0:\n    print("positif")\nelse:\n    print("negatif")\n',
    "3-kelas": b"class Kalkulator:\n    def tambah(self, a, b):\n        return a + b\n",
}

# Kasus dasar dari materi
tree = parser.parse(b"x = 1\n")
print("=== kasus dasar: x = 1 ===")
print(tree.root_node)
print()

for judul, kode in POTONGAN.items():
    tree = parser.parse(kode)
    print(f"=== potongan {judul} ===")
    print(tree.root_node)
    print()

# --- Node anonim pada potongan fungsi (langkah 4 di materi) ---
tree = parser.parse(POTONGAN["1-fungsi"])
stmt = tree.root_node.children[0]
print("=== anak node function_definition (potongan fungsi) ===")
for c in stmt.children:
    print(c.type, "bernama" if c.is_named else "anonim")

print()
print("=== anak node parameters ===")
params = stmt.child_by_field_name("parameters")
assert params is not None, "field parameters tidak ditemukan"
for c in params.children:
    print(c.type, "bernama" if c.is_named else "anonim")

# --- children vs named_children ---
print()
print("=== children vs named_children (function_definition) ===")
print("children      :", [c.type for c in stmt.children])
print("named_children:", [c.type for c in stmt.named_children])

# --- Kode rusak: ':' setelah def sapa(nama) dihapus ---
print()
print("=== kode rusak: def sapa(nama) tanpa ':' ===")
rusak = b"def sapa(nama)\n    return nama\n"
tree = parser.parse(rusak)
print(tree.root_node)


def cari_error(node):
    if node.is_error or node.is_missing:
        baris, kolom = node.start_point
        jenis = "MISSING" if node.is_missing else "ERROR"
        print(f"{jenis} node={node.type!r} di baris {baris + 1}:{kolom}")
    for c in node.children:
        cari_error(c)


cari_error(tree.root_node)
print("root.has_error =", tree.root_node.has_error)
