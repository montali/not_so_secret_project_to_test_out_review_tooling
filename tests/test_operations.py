from decimal import Decimal

import pytest

from calcstack.engine import (
    DivisionByZeroError,
    UnknownOperatorError,
    apply_operator,
)
from calcstack.engine.operations import OPERATORS


def d(value: str) -> Decimal:
    return Decimal(value)


@pytest.mark.parametrize(
    ("symbol", "a", "b", "expected"),
    [
        ("+", "2", "3", "5"),
        ("-", "2", "3", "-1"),
        ("*", "4", "5", "20"),
        ("/", "10", "4", "2.5"),
        ("%", "10", "3", "1"),
        ("^", "2", "10", "1024"),
    ],
)
def test_apply_operator(symbol: str, a: str, b: str, expected: str) -> None:
    assert apply_operator(symbol, d(a), d(b)) == d(expected)


def test_division_is_exact() -> None:
    # Decimal keeps this exact where binary floats would drift.
    assert apply_operator("/", d("1"), d("3")) == Decimal("1") / Decimal("3")


def test_divide_by_zero_raises() -> None:
    with pytest.raises(DivisionByZeroError):
        apply_operator("/", d("1"), d("0"))


def test_modulo_by_zero_raises() -> None:
    with pytest.raises(DivisionByZeroError):
        apply_operator("%", d("1"), d("0"))


def test_unknown_operator_raises() -> None:
    with pytest.raises(UnknownOperatorError) as excinfo:
        apply_operator("$", d("1"), d("2"))
    assert excinfo.value.symbol == "$"


def test_power_is_right_associative_in_registry() -> None:
    assert OPERATORS["^"].right_associative is True
    assert OPERATORS["+"].right_associative is False
