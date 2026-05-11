from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_size import AnimalSize
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.animal.animal_origin import AnimalOrigin


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

    birth_date: date
    origin: AnimalOrigin
    entry_date: Optional[date] = None
    exit_date: Optional[date] = None
    weaning_date: Optional[date] = None

    weaning_weight: Optional[float] = None
    birth_weight: Optional[float] = None

    notes: Optional[str] = None
    batch_id: Optional[int] = None