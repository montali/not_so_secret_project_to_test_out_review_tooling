"""Typed errors raised by the arithmetic engine and the parser.

A small, explicit hierarchy makes it easy for the CLI and the API to translate
failures into user-facing messages (a Rich panel, a 400 response) instead of
leaking raw Python exceptions.
"""

from __future__ import annotations


class CalculatorError(Exception):
    """Base class for every error calcstack raises on bad input."""


class DivisionByZeroError(CalculatorError):
    """Raised when an expression divides (or takes a modulo) by zero."""

    def __init__(self, message: str = "division by zero") -> None:
        super().__init__(message)


class UnknownOperatorError(CalculatorError):
    """Raised when the engine is asked to apply an operator it does not know."""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        super().__init__(f"unknown operator: {symbol!r}")
