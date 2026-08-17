from pydantic import BaseModel
from typing import Optional
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_size import AnimalSize
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus

class AnimalUpdate(BaseModel):
    identification_number: Optional[int] = None
    name: Optional[str] = None
    # Use o Enum específico ou Any (maiúsculo)
    sex: Optional[AnimalSex] = None
    animal_size: Optional[AnimalSize] = None
    animal_life_status: Optional[AnimalLifeStatus] = None
    reproductive_status: Optional[AnimalReproductiveStatus] = None
    animal_category: Optional[AnimalCategory] = None
    notes: Optional[str] = None
    batch_id: Optional[int] = None

    class Config:
        from_attributes = True









































