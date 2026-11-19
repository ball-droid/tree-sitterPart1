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

## Tugas 4 — Grammar DSL filter

1. Diminta ke AI: membuat proyek grammar `filter` (tree-sitter init),
   membangun grammar bertahap (awal, 4a–4f) dengan generate+parse per
   langkah, menambah `in`/`contains`, menulis test corpus (minimal 5),
   memastikan `tree-sitter test` lulus semua termasuk prioritas
   and/or, plus pengayaan demo konflik tanpa prec dan skrip WHERE SQL
   parameterized.
2. Kesalahan/kekurangan hasil AI yang ditemukan:
   - Percobaan pertama demo "hapus semua prec" TIDAK mengubah
     grammar.js sama sekali (penulisan file ditolak karena konten
     terdeteksi masih berisi prefix tampilan read_file), sehingga
     `generate` yang diklaim jalan sebenarnya memakai grammar lama
     tanpa konflik. Ketahuan dari error tool write + hasil generate
     yang mustahil bersih; diulang lewat terminal dengan backup dan
     menghasilkan konflik nyata (konflik-tanpa-prec.txt).
   - `field('values', seq('(', $._value, repeat(...), ')'))` dari
     petunjuk materi rupanya melabeli SEMUA anak seq dengan field
     `values:`, termasuk token anonim `(`, `,`, `)` — versi pertama
     where_sql.py memasukkan token itu sebagai parameter (13 parameter
     alih-alih 8). Ditemukan dengan menjalankan where_sql.py pada
     contoh.filter dan mencocokkan jumlah parameter dengan jumlah
     nilai input; diperbaiki dengan filter `c.is_named`.
   - Pertama AI mengira konflik associativity akan muncul di langkah
     4c (seperti uraian materi); kenyataannya `and_expression` sudah
     konflik di 4b sehingga `prec.left(2, ...)` harus dipasang lebih
     awal. Dicatat apa adanya di output-t4.txt.
   - Tool tulis-file berulang kali menolak overwrite dengan alasan
     "stale view" meski file sudah dibaca penuh — AI sempat
     mengulang tanpa perubahan (loop); diselesaikan dengan
     menghapus file via terminal lalu menulis sebagai file baru.
3. Bukti verifikasi: `tree-sitter-filter/output-t4.txt` (log tiap
   langkah berisi input, pohon aktual, pesan konflik asli),
   `tree-sitter test` 8/8 lulus (termasuk tes `a = 1 or b = 2 and c = 3`
   yang terkelompok `a = 1 or (b = 2 and c = 3)` dan `in` tiga nilai),
   `konflik-tanpa-prec.txt`, serta output where_sql.py yang
   dicocokkan manual dengan jumlah nilai di input (8 = 8).

## Tugas 5 — Highlight untuk DSL filter

1. Diminta ke AI: menyiapkan `tree-sitter init-config` + parser-directories,
   memeriksa tree-sitter.json, membuat `queries/highlights.scm`
   (dimulai dari `(string) @string`), menambahkan capture kata kunci
   (termasuk `in`/`contains`), operator, string, angka, boolean, dan
   nama field, lalu memverifikasi warna `tree-sitter highlight`.
2. Kesalahan/kekurangan hasil AI yang ditemukan:
   - AI mengira konfigurasi highlight cukup dengan queries/highlights.scm;
     ternyata `tree-sitter highlight` memberi WARNING bahwa tree-sitter.json
     perlu entri `"highlights": "queries/highlights.scm"` di objek grammar.
     Bentuk key ini dikonfirmasi dari dokumentasi resmi bagian "Query Paths"
     (bukan ditebak), lalu ditambahkan — warning hilang.
   - Pada tema default, `@constant.builtin` (boolean) dan `@number`
     terpetakan ke warna yang SAMA (94) sehingga `true` dan `2` tidak
     terlihat beda — melanggar kriteria "setiap jenis token berwarna
     berbeda". Ditemukan dengan membaca kode ANSI hasil `tree-sitter
     highlight` (cat -v), diperbaiki dengan mengubah `constant.builtin`
     ke warna 172 di tema config.json.
   - Percobaan pertama menulis ulang highlights.scm ditolak tool tulis
     file (stale view) dan AI sempat menulis output verifikasi ke path
     yang salah karena `cd` di dalam blok shell mengubah direktori
     kerja sebelum `cat` dijalankan; kedua hal diperbaiki (patch file,
     lalu path absolut).
3. Bukti verifikasi: `tree-sitter-filter/output-t5-mentah.txt` berisi
   output ANSI penuh (warna per token terbaca: 124/239-tebal/28/56/
   94-tebal/172-tebal/239) dan hasil `tree-sitter highlight --check`
   "All highlight captures conform to standards."; ringkasan tabel di
   `tree-sitter-filter/output-t5.txt`.

## Tugas 6 — Mini proyek cek.py

1. Diminta ke AI: membuat `cek.py <folder>` dari kerangka materi
   (fitur 1 TODO/FIXME sudah ada), menambah fitur 2 (fungsi >30 baris
   via query+matches) dan fitur 3 (file bererror via has_error +
   rekursi cari ERROR/MISSING), membuat folder `uji/`, mengujinya pada
   repo open source nyata (psf/requests), memverifikasi 2 file acak
   secara manual, menulis README, plus pengayaan dukungan JavaScript.
2. Kesalahan/kekurangan hasil AI yang ditemukan:
   - Draft query JS pertama memakai `name: (identifier)` untuk semua
     fungsi; probe parse JS yang dijalankan lebih dulu menunjukkan
     `method_definition` justru ber-field `property_identifier` —
     draft itu akan SENYAP melewatkan semua method. Diperbaiki sebelum
     dipakai, dengan query terpisah per jenis fungsi.
   - Header file uji `todo.py` semula berbunyi "komentar TODO/FIXME"
     sehingga komentar header itu IKUT terdeteksi (3 temuan, padahal
     yang dimaksud 2) — membingungkan saat verifikasi manual.
     Ketahuan karena jumlah temuan tidak cocok dengan hitungan manual;
     header diganti dan jumlah menjadi 2 = 2.
   - Perkiraan AI soal panjang fungsi `proses_data` meleset
     (dikira ~47 baris); pengecekan manual span baris 7-45 membuktikan
     39 baris — angka cek.py yang benar, perkiraan AI yang salah.
   - Eksekusi shell berisi `cd` di dalam blok `{ ... } > file`
     menyebabkan perintah `cat` di akhir berjalan di direktori lain
     (path jadi tidak valid); output sebenarnya tersimpan, hanya
     pembacaannya yang gagal — diperbaiki dengan path absolut.
3. Bukti verifikasi: `cek/output-uji.txt` (output pada folder uji,
   semua temuan cocok dengan hitungan manual), `cek/output-repo-requests.txt`
   (63 temuan pada psf/requests), dan `cek/output-t6.txt` — verifikasi
   silang 2 file ACAK (exceptions.py, cookies.py dipilih dengan `shuf`):
   semua temuan cocok manual (create_cookie baris 494-528 = 35 baris
   persis; _find_no_duplicates 423-452 = 30 baris tepat di ambang dan
   benar tidak dilaporkan), plus `python -m py_compile` sebagai cek
   independen bahwa kedua file memang tidak bererror.

