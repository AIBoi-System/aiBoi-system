from pydantic import BaseModel
from typing import Optional

from app.domain.enums.animal.animal_sex import AnimalSex
from app.domain.enums.animal.animal_life_status import AnimalLifeStatus
from app.domain.enums.animal.animal_size import AnimalSize
from app.domain.enums.animal.animal_category import AnimalCategory
from app.domain.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.domain.enums.animal.animal_origin import AnimalOrigin
from app.presentation.schemas.common import BRDate


class AnimalBase(BaseModel):
    identification_number: int
    chip_id: Optional[int] = None
    pedigree_po: Optional[int] = None
    name: Optional[str] = None

    sex: AnimalSex
    breed: Optional[str] = None
    animal_size: AnimalSize
    animal_life_status: AnimalLifeStatus
    reproductive_status: Optional[AnimalReproductiveStatus] = None
    animal_category: AnimalCategory

    birth_date: BRDate
    origin: AnimalOrigin
    entry_date: Optional[BRDate] = None
    exit_date: Optional[BRDate] = None
    weaning_date: Optional[BRDate] = None

    weaning_weight: Optional[float] = None
    birth_weight: Optional[float] = None

    notes: Optional[str] = None
    batch_id: Optional[int] = None