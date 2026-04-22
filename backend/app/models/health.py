from datetime import date
from typing import Optional

from app.enums.health.health_type import HealthType


class Health:

    def __init__(
        self,
        id_health_record: int,
        health_type: HealthType,
        product_name: str,
        application_date: date,
        responsible: str,
        dosage: float,
        unit_price: float,
        notes: Optional[str],
        animal_id: int
    ):
        self.id_health_record = id_health_record
        self.health_type = health_type
        self.product_name = product_name
        self.application_date = application_date
        self.responsible = responsible
        self.dosage = dosage
        self.unit_price = unit_price
        self.notes = notes

        # Relacionamento com Animal
        self.animal_id = animal_id