from datetime import date
from typing import Optional, List

from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_size import AnimalSize
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.animal.animal_origin import AnimalOrigin


class Animal:

    def __init__(
        self,
        id_animal: int,
        identification_number: int,
        chip_id: int,
        pedigree_po: int,
        name: str,
        sex: AnimalSex,
        breed: str,
        category: str,
        animal_size: AnimalSize,
        animal_life_status: AnimalLifeStatus,
        reproductive_status: AnimalReproductiveStatus,
        birth_date: date,
        origin: AnimalOrigin,
        entry_date: Optional[date],
        exit_date: Optional[date],
        weaning_date: Optional[date],
        weaning_weight: Optional[float],
        birth_weight: Optional[float],
        notes: Optional[str],
        animal_category: AnimalCategory
    ):
        self.id_animal = id_animal
        self.identification_number = identification_number
        self.chip_id = chip_id
        self.pedigree_po = pedigree_po
        self.name = name
        self.sex = sex
        self.breed = breed
        self.category = category
        self.animal_size = animal_size
        self.animal_life_status = animal_life_status
        self.reproductive_status = reproductive_status
        self.birth_date = birth_date
        self.origin = origin
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.weaning_date = weaning_date
        self.weaning_weight = weaning_weight
        self.birth_weight = birth_weight
        self.notes = notes
        self.animal_category = animal_category

        # Relacionamentos
        self.weights: List = []
        self.health_records: List = []
        self.reproductions: List = []