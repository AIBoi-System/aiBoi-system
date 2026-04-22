from datetime import date
from app.core.database import Base
from typing import Optional

class DeathRecord(Base):
  

    def __init__(
        self, 
        cause: str, 
        death_date: date, 
        animal_id: int,
        id: Optional[int] = None
    ):
        self.id = id
        self.cause = cause
        self.death_date = death_date
        self.animal_id = animal_id