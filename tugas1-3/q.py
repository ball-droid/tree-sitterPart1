"""Tugas 3 — Penjalang query (kerangka dari materi).

Pemakaian:
    python q.py <file.py> <pola.scm>            -> mode captures
    python q.py <file.py> <pola.scm> matches    -> mode matches
        (untuk query yang butuh pasangan capture dalam satu match,
        mis. nama fungsi + jumlah parameter)
"""
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)
kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

if len(sys.argv) > 3 and sys.argv[3] == "matches":
    for i, (_, cap) in enumerate(
        QueryCursor(Query(PY, pola)).matches(tree.root_node), 1
    ):
        print(f"-- match {i} --")
        for nama, nodes in cap.items():
            for n in nodes:
                print(f"@{nama}  baris {n.start_point[0] + 1}: {(n.text or b'').decode(errors='replace')}")
        if "nama" in cap and "params" in cap:
            nama = (cap["nama"][0].text or b"").decode(errors="replace")
            jumlah = cap["params"][0].named_child_count
            print(f">>> {nama}: {jumlah} parameter")
else:
    hasil = QueryCursor(Query(PY, pola)).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            print(f"@{nama}  baris {n.start_point[0] + 1}: {(n.text or b'').decode(errors='replace')}")
