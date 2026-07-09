"""Arithmetic engine: Decimal-based operations and the operator registry."""

from calcstack.engine.errors import (
    CalculatorError,
    DivisionByZeroError,
    UnknownOperatorError,
)
from calcstack.engine.operations import OPERATORS, Operator, apply_operator

__all__ = [
    "OPERATORS",
    "CalculatorError",
    "DivisionByZeroError",
    "Operator",
    "UnknownOperatorError",
    "apply_operator",
]
