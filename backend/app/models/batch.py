from datetime import date
from typing import Optional, List

from app.enums.batch.batch_purpose import BatchPurpose


class Batch:

    def __init__(
        self,
        id_batch: int,
        name: str,
        batch_purpose: BatchPurpose,
        check_in: date,
        check_out: Optional[date],
        status: str,
        category: str
    ):
        self.id_batch = id_batch
        self.name = name
        self.batch_purpose = batch_purpose
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.category = category

        # Relacionamento com animais
        self.animals: List = []