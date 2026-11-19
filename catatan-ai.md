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

