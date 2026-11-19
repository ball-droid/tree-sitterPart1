; Nama node diambil dari output jelajah.py pada impor.py
; (bukan ditebak): import_statement name: dotted_name,
; import_from_statement module_name: dotted_name + name: dotted_name
(import_statement
  name: (dotted_name (identifier) @modul)) @impor

(import_from_statement
  module_name: (dotted_name (identifier) @modul)) @impor
