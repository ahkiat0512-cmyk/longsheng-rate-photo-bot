import re

from .models import RateSheet


class RateSheetError(ValueError):
    pass


RATE_RE = re.compile(r"(?<!\d)(\d\.\d{3}|\d\.\d{2})(?!\d)")
DATE_RE = re.compile(r"(\d{1,2}/\d{1,2}/\d{4})")


def _section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        raise RateSheetError(f"缺少：{heading}")
    start += len(heading)
    end = text.find(next_heading, start) if next_heading else len(text)
    return text[start:] if end < 0 else text[start:end]


def _rates(text: str, expected: int, name: str) -> tuple[str, ...]:
    found = tuple(RATE_RE.findall(text))
    if len(found) < expected:
        raise RateSheetError(f"{name} 汇率数量不足")
    return found[:expected]


def parse_rate_sheet(text: str) -> RateSheet:
    normalized = text.replace("**", "").replace("\\", "").replace("\r", "")
    date_match = DATE_RE.search(normalized)
    if not date_match:
        raise RateSheetError("缺少日期，例如：26/10/2026")

    transfer = _section(normalized, "马币转账", "马币现金")
    cash = _section(normalized, "马币现金", "人民币")
    rmb = _section(normalized, "人民币", None)
    local_rate, foreign_tng_rate = _rates(transfer, 2, "马币转账")
    cash_rates = _rates(cash, 3, "马币现金")
    rmb_rates = _rates(rmb, 2, "人民币")

    return RateSheet(
        date=date_match.group(1),
        local_rate=local_rate,
        foreign_tng_rate=foreign_tng_rate,
        cash_rates=(cash_rates[0], cash_rates[1], cash_rates[2]),
        rmb_rates=(rmb_rates[0], rmb_rates[1]),
    )
