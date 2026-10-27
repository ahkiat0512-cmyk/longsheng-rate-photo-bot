from dataclasses import dataclass


@dataclass(frozen=True)
class RateSheet:
    date: str
    local_rate: str
    foreign_tng_rate: str
    cash_rates: tuple[str, str, str]
    rmb_rates: tuple[str, str]
