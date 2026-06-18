from dataclasses import dataclass
from app.shared.domain.value_objects import ValueObject


@dataclass(frozen=True)
class Weight(ValueObject):
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("O peso não pode ser negativo.")

    def __str__(self):
        return f"{self.value} kg"


@dataclass(frozen=True)
class IdentificationNumber(ValueObject):
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("O número de identificação deve ser positivo.")

    def __str__(self):
        return str(self.value)









































