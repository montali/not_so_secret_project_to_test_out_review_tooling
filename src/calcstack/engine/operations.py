"""The binary operations calcstack understands, plus their parsing metadata.

Everything is computed with :class:`decimal.Decimal` so results are exact and
easy to assert against in tests (no binary floating-point surprises).

The :data:`OPERATORS` registry is the single source of truth shared by the
engine and the parser: it maps a symbol to the function that applies it and to
the precedence/associativity the shunting-yard evaluator needs.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal

from calcstack.engine.errors import DivisionByZeroError, UnknownOperatorError


@dataclass(frozen=True)
class Operator:
    """A binary operator and the metadata the parser needs to order it."""

    symbol: str
    precedence: int
    right_associative: bool
    apply: Callable[[Decimal, Decimal], Decimal]


def add(a: Decimal, b: Decimal) -> Decimal:
    return a + b


def subtract(a: Decimal, b: Decimal) -> Decimal:
    return a - b


def multiply(a: Decimal, b: Decimal) -> Decimal:
    return a * b


def divide(a: Decimal, b: Decimal) -> Decimal:
    if b == 0:
        raise DivisionByZeroError
    return a / b


def modulo(a: Decimal, b: Decimal) -> Decimal:
    if b == 0:
        raise DivisionByZeroError("modulo by zero")
    return a % b


def power(a: Decimal, b: Decimal) -> Decimal:
    return a**b


OPERATORS: dict[str, Operator] = {
    "+": Operator("+", precedence=1, right_associative=False, apply=add),
    "-": Operator("-", precedence=1, right_associative=False, apply=subtract),
    "*": Operator("*", precedence=2, right_associative=False, apply=multiply),
    "/": Operator("/", precedence=2, right_associative=False, apply=divide),
    "%": Operator("%", precedence=2, right_associative=False, apply=modulo),
    "^": Operator("^", precedence=3, right_associative=True, apply=power),
}


def apply_operator(symbol: str, a: Decimal, b: Decimal) -> Decimal:
    """Apply the operator named ``symbol`` to ``a`` and ``b``.

    Raises :class:`UnknownOperatorError` if the symbol is not registered.
    """
    try:
        operator = OPERATORS[symbol]
    except KeyError:
        raise UnknownOperatorError(symbol) from None
    return operator.apply(a, b)
