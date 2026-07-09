"""Evaluate arithmetic expressions using the shunting-yard algorithm.

The expression is tokenized, converted to Reverse Polish Notation (respecting
operator precedence, associativity, parentheses and unary minus), and then the
RPN stream is evaluated with the engine's :data:`OPERATORS` registry.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from calcstack.engine.errors import CalculatorError
from calcstack.engine.operations import OPERATORS, apply_operator
from calcstack.parser.tokenizer import Token, TokenType, tokenize

# Unary minus is modelled as an internal pseudo-operator. Its precedence sits
# above the binary operators but below exponentiation, so that ``-2^2`` parses
# as ``-(2^2)`` (matching normal maths / Python's ``-2**2``).
_UNARY_MINUS = "u-"
_UNARY_PRECEDENCE = 3
_EXPONENT_PRECEDENCE = 4


def evaluate(expression: str) -> Decimal:
    """Evaluate ``expression`` and return the exact :class:`Decimal` result.

    Raises :class:`CalculatorError` for empty input, unbalanced parentheses,
    malformed numbers, or any other syntactic problem.
    """
    tokens = tokenize(expression)
    if not tokens:
        raise CalculatorError("empty expression")
    rpn = _to_rpn(tokens)
    return _evaluate_rpn(rpn)


def _to_rpn(tokens: list[Token]) -> list[Token]:
    output: list[Token] = []
    operators: list[Token] = []
    # An operand is expected at the start and after any operator or "(".
    expect_operand = True

    for token in tokens:
        if token.type is TokenType.NUMBER:
            output.append(token)
            expect_operand = False
        elif token.type is TokenType.OPERATOR:
            op = _resolve_operator(token, expect_operand)
            _drain_for_operator(op, operators, output)
            operators.append(op)
            expect_operand = True
        elif token.type is TokenType.LPAREN:
            operators.append(token)
            expect_operand = True
        else:  # RPAREN
            _drain_until_lparen(operators, output)
            expect_operand = False

    while operators:
        top = operators.pop()
        if top.type is TokenType.LPAREN:
            raise CalculatorError("unbalanced parentheses")
        output.append(top)
    return output


def _resolve_operator(token: Token, expect_operand: bool) -> Token:
    """Turn a raw operator token into a binary op or a unary prefix op.

    When an operand was expected, a leading ``-`` is unary minus and a leading
    ``+`` is unary plus (identity). Any other operator in that position is an
    error (it has no left operand, e.g. ``"* 3"``).
    """
    if expect_operand:
        if token.value == "-":
            return Token(TokenType.OPERATOR, _UNARY_MINUS)
        if token.value == "+":
            return Token(TokenType.OPERATOR, "u+")
        raise CalculatorError(f"operator {token.value!r} is missing a left operand")
    return token


def _precedence(symbol: str) -> int:
    if symbol in (_UNARY_MINUS, "u+"):
        return _UNARY_PRECEDENCE
    return OPERATORS[symbol].precedence


def _is_right_associative(symbol: str) -> bool:
    if symbol in (_UNARY_MINUS, "u+"):
        return True
    return OPERATORS[symbol].right_associative


def _drain_for_operator(op: Token, operators: list[Token], output: list[Token]) -> None:
    while operators:
        top = operators[-1]
        if top.type is not TokenType.OPERATOR:
            break
        top_prec = _precedence(top.value)
        op_prec = _precedence(op.value)
        if top_prec > op_prec or (top_prec == op_prec and not _is_right_associative(op.value)):
            output.append(operators.pop())
        else:
            break


def _drain_until_lparen(operators: list[Token], output: list[Token]) -> None:
    while operators and operators[-1].type is not TokenType.LPAREN:
        output.append(operators.pop())
    if not operators:
        raise CalculatorError("unbalanced parentheses")
    operators.pop()  # discard the matching "("


def _evaluate_rpn(rpn: list[Token]) -> Decimal:
    stack: list[Decimal] = []
    for token in rpn:
        if token.type is TokenType.NUMBER:
            try:
                stack.append(Decimal(token.value))
            except InvalidOperation as exc:  # pragma: no cover - tokenizer guards this
                raise CalculatorError(f"invalid number {token.value!r}") from exc
        elif token.value == "u+":
            _require(stack, 1)
        elif token.value == _UNARY_MINUS:
            _require(stack, 1)
            stack.append(-stack.pop())
        else:
            _require(stack, 2)
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_operator(token.value, a, b))

    if len(stack) != 1:
        raise CalculatorError("malformed expression")
    return stack[0]


def _require(stack: list[Decimal], count: int) -> None:
    if len(stack) < count:
        raise CalculatorError("malformed expression")
