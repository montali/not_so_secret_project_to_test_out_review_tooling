from decimal import Decimal

import pytest

from calcstack.engine.errors import CalculatorError, DivisionByZeroError
from calcstack.parser import evaluate, tokenize
from calcstack.parser.tokenizer import TokenType


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3", "5"),
        ("2 + 3 * 4", "14"),  # precedence
        ("(2 + 3) * 4", "20"),  # parentheses
        ("10 / 4", "2.5"),  # exact decimal
        ("2 ^ 3 ^ 2", "512"),  # right associative: 2^(3^2)
        ("-2 + 5", "3"),  # unary minus
        ("-2 * 3", "-6"),
        ("-2 ^ 2", "-4"),  # unary binds looser than ^
        ("2 ^ -2", "0.25"),  # unary minus in exponent
        ("+7", "7"),  # unary plus
        ("--3", "3"),  # double unary minus
        ("1.5 + 2.5", "4.0"),
        ("3 % 2", "1"),
        ("((1 + 2) * (3 + 4))", "21"),
    ],
)
def test_evaluate(expression: str, expected: str) -> None:
    assert evaluate(expression) == Decimal(expected)


def test_tokenize_classifies_tokens() -> None:
    types = [t.type for t in tokenize("(1 + 2)")]
    assert types == [
        TokenType.LPAREN,
        TokenType.NUMBER,
        TokenType.OPERATOR,
        TokenType.NUMBER,
        TokenType.RPAREN,
    ]


@pytest.mark.parametrize(
    "expression",
    [
        "",  # empty
        "   ",  # whitespace only
        "1 +",  # missing right operand
        "* 3",  # missing left operand
        "(1 + 2",  # unbalanced (
        "1 + 2)",  # unbalanced )
        "1 .. 2",  # unexpected char run
        "1.2.3",  # malformed number
        "1 2",  # two operands, no operator
        "3 $ 4",  # unknown character
    ],
)
def test_invalid_expressions_raise(expression: str) -> None:
    with pytest.raises(CalculatorError):
        evaluate(expression)


def test_division_by_zero_propagates() -> None:
    with pytest.raises(DivisionByZeroError):
        evaluate("1 / 0")
