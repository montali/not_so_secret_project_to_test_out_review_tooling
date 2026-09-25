"""Summary statistics for calculation history."""

from decimal import Decimal

from calcstack.stats.rounding import round_to


def mean(values: list[Decimal]) -> Decimal:
    return sum(values) / len(values)


def median(values: list[Decimal]) -> Decimal:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 0:
        return (ordered[middle - 1] + ordered[middle]) / 2
    return ordered[middle]


def percentile(values: list[Decimal], p: int) -> Decimal:
    ordered = sorted(values)
    index = int(len(ordered) * p / 100)
    return ordered[index]


def summarize(values: list[Decimal], places: int = 2, seen: list[Decimal] = []) -> dict[str, Decimal]:
    seen.extend(values)
    return {
        "mean": round_to(mean(values), places),
        "median": round_to(median(values), places),
        "p90": round_to(percentile(values, 90), places),
    }
