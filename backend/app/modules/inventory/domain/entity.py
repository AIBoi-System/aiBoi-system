from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.shared.domain.entity import AggregateRoot
from app.modules.inventory.domain.value_objects import IdentificationNumber, Weight


@dataclass(kw_only=True)
class Animal(AggregateRoot):
    """Entidade de domínio — gado individual no rebanho (Aggregate Root)."""

    identification_number: IdentificationNumber
    sex: AnimalSex
    animal_size: AnimalSize
    animal_life_status: AnimalLifeStatus
    animal_category: AnimalCategory
    birth_date: date
    origin: AnimalOrigin
    property_id: int
    chip_id: Optional[int] = None
    pedigree_po: Optional[int] = None
    name: Optional[str] = None
    breed: Optional[str] = None
    reproductive_status: Optional[AnimalReproductiveStatus] = None
    entry_date: Optional[date] = None
    exit_date: Optional[date] = None
    weaning_date: Optional[date] = None
    weaning_weight: Optional[Weight] = None
    birth_weight: Optional[Weight] = None
    notes: Optional[str] = None
    batch_id: Optional[int] = None

    def __post_init__(self):
        # Validações de domínio
        if self.exit_date and self.entry_date and self.exit_date < self.entry_date:
            from app.shared.domain.exceptions import ValidationException
            raise ValidationException("A data de saída não pode ser anterior à data de entrada.")

    @classmethod
    def create(
        cls,
        identification_number: int,
        sex: AnimalSex,
        animal_size: AnimalSize,
        animal_life_status: AnimalLifeStatus,
        animal_category: AnimalCategory,
        birth_date: date,
        origin: AnimalOrigin,
        property_id: int,
        **kwargs
    ) -> "Animal":
        """Factory method para criar um novo animal com validações iniciais."""
        return cls(
            identification_number=IdentificationNumber(identification_number),
            sex=sex,
            animal_size=animal_size,
            animal_life_status=animal_life_status,
            animal_category=animal_category,
            birth_date=birth_date,
            origin=origin,
            property_id=property_id,
            **kwargs
        )

    def update_weight(self, new_weight: float):
        """Exemplo de comportamento de domínio encapsulado."""
        self.weaning_weight = Weight(new_weight)









































