# cek.py — pendeteksi TODO, fungsi panjang, dan file bererror

Mini proyek Tugas 6: CLI kecil `cek.py <folder>` yang mem-parse file
Python (dan JavaScript) dengan tree-sitter lalu melaporkan:

1. Setiap komentar berisi `TODO` atau `FIXME` — beserta file dan baris.
2. Setiap fungsi yang lebih dari 30 baris — beserta nama dan jumlah baris.
3. Setiap file yang pohonnya mengandung error sintaks — beserta baris
   `ERROR`/`MISSING` pertama.

## Instalasi dependensi

Butuh Python 3.10+ dan paket binding tree-sitter:

    python -m pip install tree-sitter tree-sitter-python tree-sitter-javascript

(tree-sitter-javascript hanya untuk dukungan file `.js` [pengayaan];
tanpanya, hapus entri `".js"` di `BAHASA` pada cek.py.)

## Cara menjalankan

    python cek.py <folder>

Contoh (dari folder `cek/`):

    python cek.py uji/

Output per baris: `<path>:<baris>: <temuan>`.

## Contoh output

    $ python cek.py uji/
    uji\panjang.py:7: fungsi 'proses_data' 39 baris (>30)
    uji\rusak.py: pohon bererror -- ERROR 'ERROR' di baris 3
    uji\todo.js:2: // TODO: tambahkan validasi input
    uji\todo.py:4: # TODO: tangani b = 0
    uji\todo.py:9: # FIXME: escape karakter khusus

Pada repo nyata (psf/requests, 130 file) hasilnya ada di
`output-repo-requests.txt` (63 temuan).

## Catatan perilaku

- **Semua fungsi dihitung**, termasuk method di dalam kelas dan fungsi
  bersarang. Fungsi dihitung dari baris `def` sampai baris terakhir
  body-nya; yang dilaporkan hanya yang > 30 baris (batas ketat,
  30 baris persis tidak dilaporkan).
- Untuk JavaScript, yang dihitung: `function_declaration`,
  `generator_function_declaration`, dan `method_definition`. Arrow
  function tanpa nama tidak dihitung (tidak punya field `name`).
- Folder `venv/`, `.git/`, `node_modules/`, `__pycache__/`, `target/`,
  `dist/` dilewati.
- File dengan encoding aneh tidak membuat skrip gagal
  (`decode(errors="replace")`).
- Deteksi error memakai `root_node.has_error`, lalu mencari node
  `ERROR`/`MISSING` pertama secara preorder untuk melaporkan barisnya.

## Isi folder ini

    cek.py                skrip utama
    uji/                  file uji buatan sendiri (todo.py, panjang.py,
                          rusak.py, todo.js)
    output-uji.txt        hasil cek.py pada uji/
    output-repo-requests.txt  hasil cek.py pada repo psf/requests
    output-t6.txt         verifikasi silang 2 file acak vs cek manual
