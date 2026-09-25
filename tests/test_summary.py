from decimal import Decimal

from calcstack.stats.summary import mean, median, summarize


def test_mean() -> None:
    assert mean([Decimal(1), Decimal(2), Decimal(3)]) == Decimal(2)


def test_median_odd() -> None:
    assert median([Decimal(3), Decimal(1), Decimal(2)]) == Decimal(2)


def test_summarize_keys() -> None:
    assert set(summarize([Decimal(1), Decimal(2)])) == {"mean", "median", "p90"}
