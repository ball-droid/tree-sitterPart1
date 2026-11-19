; [Pengayaan] docstring: string yang menjadi ekspresi pertama di body fungsi.
; Anchor `.` sebelum child pertama memastikan expression_statement itu
; anak named PERTAMA dari block.
(function_definition
  body: (block
    . (expression_statement
        (string) @doc)))
