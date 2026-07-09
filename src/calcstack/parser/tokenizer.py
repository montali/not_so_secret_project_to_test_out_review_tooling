"""A tiny hand-written tokenizer for arithmetic expressions.

It recognises numbers (integers and decimals), the operator symbols registered
in :data:`calcstack.engine.operations.OPERATORS`, and parentheses. Anything
else raises :class:`calcstack.engine.errors.CalculatorError`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from calcstack.engine.errors import CalculatorError
from calcstack.engine.operations import OPERATORS


class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str


def tokenize(expression: str) -> list[Token]:
    """Split ``expression`` into a flat list of tokens.

    Raises :class:`CalculatorError` on any unexpected character or malformed
    number (e.g. ``"1.2.3"``).
    """
    tokens: list[Token] = []
    index = 0
    length = len(expression)

    while index < length:
        char = expression[index]

        if char.isspace():
            index += 1
            continue

        if char == "(":
            tokens.append(Token(TokenType.LPAREN, char))
            index += 1
            continue

        if char == ")":
            tokens.append(Token(TokenType.RPAREN, char))
            index += 1
            continue

        if char in OPERATORS:
            tokens.append(Token(TokenType.OPERATOR, char))
            index += 1
            continue

        if char.isdigit() or char == ".":
            number, index = _consume_number(expression, index)
            tokens.append(Token(TokenType.NUMBER, number))
            continue

        raise CalculatorError(f"unexpected character {char!r} at position {index}")

    return tokens


def _consume_number(expression: str, start: int) -> tuple[str, int]:
    index = start
    seen_dot = False
    while index < len(expression):
        char = expression[index]
        if char == ".":
            if seen_dot:
                raise CalculatorError(f"malformed number near position {start}")
            seen_dot = True
        elif not char.isdigit():
            break
        index += 1

    literal = expression[start:index]
    if literal in {"", "."}:
        raise CalculatorError(f"malformed number near position {start}")
    return literal, index
