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

