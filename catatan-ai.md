# Catatan Penggunaan AI (wajib untuk laporan)

Format per tugas: (1) apa yang diminta ke AI, (2) minimal satu
kesalahan/kekurangan hasil AI yang ditemukan, (3) bukti verifikasinya.

## Tugas 1 — Membaca pohon

1. Diminta ke AI: membuat `t1.py` (kerangka materi) untuk mem-parse 3
   potongan Python (fungsi, if/else, kelas+method), mencetak
   `tree.root_node`, menampilkan node anonim, membandingkan `children`
   vs `named_children`, dan mendemonstrasikan node ERROR/MISSING.
   AI juga diminta menulis pohon PERKIRAAN dulu di `perkiraan-t1.txt`
   sebelum parser dijalankan.
2. Kesalahan hasil AI yang ditemukan:
   - Pohon perkiraan AI untuk potongan if/else menulis field
     `left:`/`right:` pada node `comparison_operator` — padahal hasil
     parse aktual TIDAK punya field itu: `(comparison_operator
     (identifier) (integer))`.
   - Pohon perkiraan AI menggambarkan string cukup `(string)`, sedangkan
     grammar tree-sitter-python sekarang memecahnya menjadi
     `(string (string_start) (string_content) (string_end))`.
3. Bukti verifikasi: `tugas1-3/output-t1.txt` memuat pohon perkiraan
   (ditulis sebelum eksekusi) di sebelah output verbatim `python t1.py`,
   lalu analisis selisih per potongan. Kasus dasar `x = 1` cocok persis
   dengan contoh output di materi, dan potongan fungsi serta kelas cocok
   100% dengan perkiraan. Kesalahan di atas ditemukan JUSTRU karena
   aturan "lihat pohonnya dulu, jangan menebak nama node/field".

## Tugas 2 — Penjelajah node

1. Diminta ke AI: mengisi `TODO` kerangka `jelajah.py` dari materi
   (rekursi `enumerate(node.children)`, filter `is_named`,
   `field_name_for_child(i)`), membuat versi pengayaan `TreeCursor`,
   lalu mengujinya pada `kecil.py` dan file Python nyata >= 100 baris
   (requests/src/requests/sessions.py, 920 baris) serta memverifikasi
   output-nya.
2. Kesalahan/kekurangan hasil AI yang ditemukan:
   - AI menjalankan `jelajah.py` dengan argumen path gaya MSYS
     (`/j/treesitter/...`) yang TIDAK bisa dibuka Python Windows native
     (FileNotFoundError). Hasilnya kosong/traceback; harus diulang
     dengan path native `J:/treesitter/...`.
   - Percobaan verifikasi pertama AI memakai `grep "class Session"`
     pada output jelajah — padahal output itu berisi TIPE node
     (`class_definition`), bukan teks sumber. Pencocokan pertama nihil
     dan salah arah; diperbaiki dengan meng-grep `class_definition`
     lalu membandingkan angka baris/kolomnya ke baris sumber.
   - (lint) `child_by_field_name()` mengembalikan Optional; kode awal
     AI tidak menangani `None` (ditandai Pyright), diperbaiki dengan
     assert eksplisit.
3. Bukti verifikasi: `tugas1-3/output-t2.txt` — output `kecil.py` cocok
   persis dengan contoh materi; `diff` versi rekursif vs TreeCursor
   identik untuk kedua file uji; 5 pengecekan manual posisi/field ke
   file sumber semuanya cocok (mis. `class_definition [127:0]` vs
   baris 127 `class SessionRedirectMixin:`, `name: identifier [127:6]`
   vs kolom 6).

## Tugas 3 — Query pertama

1. Diminta ke AI: membuat `q.py` (penjalang query dari kerangka materi,
   mode `captures` dan `matches`), lalu menulis query untuk (a) semua
   identifier, (b) nama fungsi + jumlah parameter, (c) pemanggilan
   `print(...)`, (d) import/from-import + nama modul, (e) [pengayaan]
   docstring — dan memverifikasinya dengan hitungan manual pada
   `contoh.py`.
2. Kesalahan/kekurangan hasil AI yang ditemukan:
   - Kerangka `q.py` dari materi memakai `n.text.decode()`; salinan
     pertama AI mempertahankannya sehingga Pyright menandai `text`
     bisa `None` (3 error `reportOptionalMemberAccess`). Diperbaiki
     dengan `(n.text or b"").decode(errors="replace")`.
   - Tanpa melihat pohon, query import hampir pasti salah: AI harus
     benar-benar menjalankan `jelajah.py` pada `impor.py` untuk tahu
     bahwa `from x import y` memakai field `module_name:` untuk modul
     dan `name:` untuk simbol. Query yang menebak field `name:` untuk
     modul akan menghasilkan `Path`/`path` (simbol), bukan modulnya.
   - Pengecekan awal AI mengasumsikan komentar `# TODO` berada di
     dalam `block` (sehingga bisa menggeser "baris pertama body");
     hasil `jelajah.py` menunjukkan `comment` justru anak langsung
     `function_definition`, di antara `parameters` dan `body` —
     asumsi itu salah dan dikoreksi dari pohon.
3. Bukti verifikasi: `tugas1-3/output-t3.txt` memuat hitungan manual
   per baris (31 identifier, 4 fungsi: sapa=1, jumlah=3, jalan=1,
   berhenti=2 parameter; 4 print; 4 import; 1 docstring) yang semuanya
   cocok dengan hasil query di `output-t3-mentah.txt`.

