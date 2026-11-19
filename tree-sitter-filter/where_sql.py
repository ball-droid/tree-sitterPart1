"""Tugas 4 [Pengayaan] — ubah pohon DSL filter menjadi klausa WHERE SQL.

Keamanan: nilai TIDAK PERNAH digabung ke dalam teks SQL. Semua nilai
dikirim sebagai parameter `?` (parameterized query) dalam urutan yang
sama dengan kemunculannya di klausa. Nama kolom divalidasi dengan
regex identifier sehingga tidak bisa dipakai untuk injeksi.

Pemakaian:
    python where_sql.py <file.filter>

Contoh:
    python where_sql.py contoh.filter
"""
import ctypes
import re
import sys
from pathlib import Path

from tree_sitter import Language, Parser

# Muat grammar filter hasil `tree-sitter build` (filter.dll / filter.so).
_DIR = Path(__file__).resolve().parent
_LIB = _DIR / ("filter.dll" if sys.platform == "win32" else "filter.so")
_lib = ctypes.CDLL(str(_LIB))
_lib.tree_sitter_filter.restype = ctypes.c_void_p

_PyCapsule_New = ctypes.pythonapi.PyCapsule_New
_PyCapsule_New.restype = ctypes.py_object
_PyCapsule_New.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]

LANG = Language(_PyCapsule_New(_lib.tree_sitter_filter(), b"tree_sitter.Language", None))
parser = Parser(LANG)

KOLOM_AMAN = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")


def teks(node):
    return (node.text or b"").decode("utf-8", errors="replace")


def nilai_param(node):
    """Ubah node nilai menjadi parameter yang aman (tanpa kutip)."""
    tipe = node.type
    t = teks(node)
    if tipe == "string":
        return t[1:-1] if len(t) >= 2 and t[0] == '"' and t[-1] == '"' else t
    if tipe == "number":
        return float(t) if "." in t else int(t)
    if tipe == "boolean":
        return t == "true"
    return t


def anak_field(node, nama):
    """Anak berdasarkan field; node anonim ber-field pun ikut ditemukan."""
    for i, c in enumerate(node.children):
        if node.field_name_for_child(i) == nama:
            return c
    return None


def operand_sql(node, params):
    """SQL untuk satu operand; ekspresi compound dibungkus kurung."""
    sql, _ = ke_sql(node, params)
    if node.type in ("and_expression", "or_expression"):
        return f"({sql})"
    return sql


def ke_sql(node, params):
    """Kembalikan (sql, params) untuk satu node ekspresi."""
    tipe = node.type

    if tipe == "comparison":
        kolom = teks(anak_field(node, "field"))
        if not KOLOM_AMAN.match(kolom):
            raise ValueError(f"nama kolom tidak aman: {kolom!r}")
        op = teks(anak_field(node, "operator"))
        params.append(nilai_param(anak_field(node, "value")))
        return f"{kolom} {op} ?", params

    if tipe == "and_expression":
        kiri = operand_sql(anak_field(node, "left"), params)
        kanan = operand_sql(anak_field(node, "right"), params)
        return f"{kiri} AND {kanan}", params

    if tipe == "or_expression":
        kiri = operand_sql(anak_field(node, "left"), params)
        kanan = operand_sql(anak_field(node, "right"), params)
        return f"{kiri} OR {kanan}", params

    if tipe == "not_expression":
        isi, _ = ke_sql(anak_field(node, "operand"), params)
        return f"NOT ({isi})", params

    if tipe == "parenthesized":
        isi, _ = ke_sql(node.named_children[0], params)
        return f"({isi})", params

    if tipe == "in_expression":
        kolom = teks(anak_field(node, "field"))
        if not KOLOM_AMAN.match(kolom):
            raise ValueError(f"nama kolom tidak aman: {kolom!r}")
        nilai = [c for i, c in enumerate(node.children)
                 if node.field_name_for_child(i) == "values" and c.is_named]
        for c in nilai:
            params.append(nilai_param(c))
        tanda = ", ".join("?" for _ in nilai)
        return f"{kolom} IN ({tanda})", params

    if tipe == "contains_expression":
        kolom = teks(anak_field(node, "field"))
        if not KOLOM_AMAN.match(kolom):
            raise ValueError(f"nama kolom tidak aman: {kolom!r}")
        params.append(f"%{nilai_param(anak_field(node, 'value'))}%")
        return f"{kolom} LIKE ?", params

    raise ValueError(f"tipe node tidak dikenal: {tipe}")


def main():
    kode = Path(sys.argv[1]).read_bytes()
    tree = parser.parse(kode)
    if tree.root_node.has_error:
        sys.exit(f"input tidak valid (ada ERROR di pohon): {sys.argv[1]}")

    params = []
    sql, _ = ke_sql(tree.root_node.named_children[0], params)
    print("WHERE:", sql)
    print("PARAMS:", params)


if __name__ == "__main__":
    main()
