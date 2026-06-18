from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ValueObject:
    """Classe base para Value Objects no DDD."""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ValueObject):
            return False
        return self.__dict__ == other.__dict__









































