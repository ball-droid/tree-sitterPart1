module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison, $.and_expression, $.or_expression,
      $.not_expression, $.in_expression, $.contains_expression,
      $.parenthesized,
    ),

    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value),
    ),
    and_expression: $ => prec.left(2, seq(field('left', $._expr), 'and', field('right', $._expr))),
    or_expression: $ => prec.left(1, seq(field('left', $._expr), 'or', field('right', $._expr))),
    parenthesized: $ => seq('(', $._expr, ')'),
    not_expression: $ => prec(3, seq('not', field('operand', $._expr))),
    in_expression: $ => seq(
      field('field', $.identifier),
      'in',
      field('values', seq('(', $._value, repeat(seq(',', $._value)), ')')),
    ),
    contains_expression: $ => seq(
      field('field', $.identifier),
      'contains',
      field('value', $._value),
    ),

    word: $ => $.identifier,
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    _value: $ => choice($.string, $.number, $.boolean),
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    boolean: $ => choice('true', 'false'),
  }
});
