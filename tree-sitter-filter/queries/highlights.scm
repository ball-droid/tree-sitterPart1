; Highlight untuk grammar filter (Tugas 5)

; kata kunci
["and" "or" "not" "in" "contains"] @keyword

; operator perbandingan
["=" "!=" ">" "<" ">=" "<="] @operator

; nilai
(string) @string
(number) @number
(boolean) @constant.builtin

; tanda baca
["(" ")"] @punctuation.bracket
[","] @punctuation.delimiter

; nama field (kolom) di sisi kiri perbandingan / in / contains
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
