from datetime import date, datetime
from typing import Any

from pydantic import BeforeValidator, PlainSerializer
from typing_extensions import Annotated


def _parse_br_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        raw = value.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw, fmt).date()
            except ValueError:
                continue
    raise ValueError("Date must be in dd/mm/yyyy format.")


BRDate = Annotated[
    date,
    BeforeValidator(_parse_br_date),
    PlainSerializer(lambda v: v.strftime("%d/%m/%Y"), return_type=str, when_used="json"),
]
