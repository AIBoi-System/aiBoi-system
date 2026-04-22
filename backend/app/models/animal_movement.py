from datetime import date
from typing import Optional


class AnimalMovement:

    def __init__(
        self,
        id_movement: int,
        animal_id: int,
        origin_batch: int,
        destination_batch: int,
        movement_date: date,
        notes: Optional[str] = None
    ):
        self.id_movement = id_movement
        self.animal_id = animal_id
        self.origin_batch_id = origin_batch
        self.destination_batch_id = destination_batch
        self.movement_date = movement_date
        self.notes = notes