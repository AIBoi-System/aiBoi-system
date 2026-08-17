from dataclasses import dataclass
import re
from typing import Any

from app.shared.domain.exceptions import ValidationException


@dataclass(frozen=True)
class ValueObject:
    """Classe base para Value Objects no DDD."""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ValueObject):
            return False
        return self.__dict__ == other.__dict__


@dataclass(frozen=True, init=False)
class CPF(ValueObject):
    """Brazilian CPF normalized to eleven digits and fully validated."""

    digits: str

    def __init__(self, value: str):
        digits = self.clean(value)
        if not self.is_valid(digits):
            raise ValidationException("CPF inválido.")
        object.__setattr__(self, "digits", digits)

    @staticmethod
    def clean(value: str) -> str:
        return "".join(character for character in str(value) if character.isdigit())

    @staticmethod
    def _limpar(value: str) -> str:
        return CPF.clean(value)

    @staticmethod
    def is_valid(value: str) -> bool:
        if len(value) != 11 or len(set(value)) == 1:
            return False

        first_sum = sum(int(value[index]) * (10 - index) for index in range(9))
        first_remainder = first_sum % 11
        first_digit = 0 if first_remainder < 2 else 11 - first_remainder

        second_sum = sum(int(value[index]) * (11 - index) for index in range(10))
        second_remainder = second_sum % 11
        second_digit = 0 if second_remainder < 2 else 11 - second_remainder
        return value[-2:] == f"{first_digit}{second_digit}"

    @staticmethod
    def validar(value: str) -> bool:
        return CPF.is_valid(CPF.clean(value))

    @property
    def value(self) -> str:
        return self.digits

    @property
    def valor(self) -> str:
        """Compatibility alias using the formatted legacy representation."""
        return self.formatted

    @property
    def formatted(self) -> str:
        return self.format(self.digits)

    @staticmethod
    def format(value: str) -> str:
        return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"

    @staticmethod
    def formatar(value: str) -> str:
        return CPF.format(CPF.clean(value))

    def __str__(self) -> str:
        return self.formatted


@dataclass(frozen=True, init=False)
class EmailAddress(ValueObject):
    value: str

    _PATTERN = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
    )

    def __init__(self, value: str):
        normalized = str(value).strip().casefold()
        if len(normalized) > 255 or not self._PATTERN.fullmatch(normalized):
            raise ValidationException("E-mail inválido.")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, init=False)
class BrazilianPhone(ValueObject):
    """Brazilian landline or mobile number, including its two-digit DDD."""

    digits: str

    OFFICIAL_AREA_CODES = frozenset(
        {
            "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "21", "22", "24", "27", "28", "31", "32", "33", "34",
            "35", "37", "38", "41", "42", "43", "44", "45", "46",
            "47", "48", "49", "51", "53", "54", "55", "61", "62",
            "63", "64", "65", "66", "67", "68", "69", "71", "73",
            "74", "75", "77", "79", "81", "82", "83", "84", "85",
            "86", "87", "88", "89", "91", "92", "93", "94", "95",
            "96", "97", "98", "99",
        }
    )

    def __init__(self, value: str):
        digits = "".join(character for character in str(value) if character.isdigit())
        if len(digits) not in {10, 11}:
            raise ValidationException("Telefone deve possuir 10 ou 11 dígitos.")
        if digits[:2] not in self.OFFICIAL_AREA_CODES or digits[2] in {"0", "1"}:
            raise ValidationException("Telefone brasileiro inválido.")
        object.__setattr__(self, "digits", digits)

    @property
    def value(self) -> str:
        return self.digits

    def __str__(self) -> str:
        return self.digits


@dataclass(frozen=True, kw_only=True)
class BrazilianAddress(ValueObject):
    zip_code: str
    state: str
    neighborhood: str
    street_name: str
    number: str
    complement: str | None = None

    OFFICIAL_STATES = frozenset(
        {
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
        }
    )

    def __post_init__(self):
        zip_code = "".join(
            character for character in str(self.zip_code) if character.isdigit()
        )
        state = str(self.state).strip().upper()
        if len(zip_code) != 8:
            raise ValidationException("CEP deve possuir 8 dígitos.")
        if state not in self.OFFICIAL_STATES:
            raise ValidationException("UF brasileira inválida.")

        normalized_fields = {
            "neighborhood": self._required(self.neighborhood, "Bairro", 100),
            "street_name": self._required(self.street_name, "Logradouro", 150),
            "number": self._required(self.number, "Número", 20),
        }
        complement = None
        if self.complement is not None and str(self.complement).strip():
            complement = self._required(self.complement, "Complemento", 255)

        object.__setattr__(self, "zip_code", zip_code)
        object.__setattr__(self, "state", state)
        for field_name, value in normalized_fields.items():
            object.__setattr__(self, field_name, value)
        object.__setattr__(self, "complement", complement)

    @staticmethod
    def _required(value: str, field_name: str, maximum: int) -> str:
        normalized = str(value).strip()
        if not normalized or len(normalized) > maximum:
            raise ValidationException(f"{field_name} inválido.")
        return normalized









































