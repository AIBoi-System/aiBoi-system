from datetime import date, datetime
from typing import Any, Optional # <-- IMPORTAÇÃO ADICIONADA AQUI

from pydantic import BeforeValidator, PlainSerializer
from typing_extensions import Annotated


def _parse_br_date(value: Any) -> Optional[date]: # O uso já estava correto após o primeiro patch, mas garantimos a tipagem aqui.
    if value is None:
        return None  # Trata explicitamente Nulo de entrada
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        raw = value.strip()
        # **CORREÇÃO: Adiciona tratamento para o valor inválido do DB**
        if raw == "0000-00-00":
            return None  # Retorna None em vez de lançar ValueError
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw, fmt).date()
            except ValueError:
                continue
    raise ValueError("Date must be a valid date format (dd/mm/yyyy or YYYY-MM-DD) or None.")


BRDate = Annotated[
    Optional[date],  # Tornar o tipo opcional para aceitar 'None' retornado pelo parser
    BeforeValidator(_parse_br_date),
    PlainSerializer(lambda v: v.strftime("%d/%m/%Y") if v else None, return_type=str, when_used="json"),
]
