from datetime import date
from typing import Optional


class BatchMovement:

    def __init__(
        self,
        id_movement: int,
        batch_id: int,
        origin_paddock: int,
        destination_paddock: int,
        movement_date: date,
        notes: Optional[str] = None
    ):
        self.id_movement = id_movement
        self.batch_id = batch_id
        self.origin_paddock_id = origin_paddock
        self.destination_paddock_id = destination_paddock
        self.movement_date = movement_date
        self.notes = notes