from decimal import ROUND_HALF_EVEN, Decimal


def round_to(value: Decimal, places: int) -> Decimal:
    quantum = Decimal(1).scaleb(-places)
    return value.quantize(quantum, rounding=ROUND_HALF_EVEN)
