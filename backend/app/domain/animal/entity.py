from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domain.enums.animal.animal_category import AnimalCategory
from app.domain.enums.animal.animal_life_status import AnimalLifeStatus
from app.domain.enums.animal.animal_origin import AnimalOrigin
from app.domain.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.domain.enums.animal.animal_sex import AnimalSex
from app.domain.enums.animal.animal_size import AnimalSize


@dataclass
class Animal:
    """Entidade de domínio — gado individual no rebanho."""

    identification_number: int
    sex: AnimalSex
    animal_size: AnimalSize
    animal_life_status: AnimalLifeStatus
    animal_category: AnimalCategory
    birth_date: date
    origin: AnimalOrigin
    id_animal: Optional[int] = None
    chip_id: Optional[int] = None
    pedigree_po: Optional[int] = None
    name: Optional[str] = None
    breed: Optional[str] = None
    reproductive_status: Optional[AnimalReproductiveStatus] = None
    entry_date: Optional[date] = None
    exit_date: Optional[date] = None
    weaning_date: Optional[date] = None
    weaning_weight: Optional[float] = None
    birth_weight: Optional[float] = None
    notes: Optional[str] = None
    batch_id: Optional[int] = None

    def ensure_unique_identification(self, exists: bool) -> None:
        from app.domain.shared.exceptions import DuplicateEntityError

        if exists:
            raise DuplicateEntityError(
                "Animal", "identification_number", self.identification_number
            )
