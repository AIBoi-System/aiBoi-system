from datetime import date
from typing import Optional, List

from backend.app.enums.reproduction.reproduction_type import ReproductionType
from backend.app.enums.reproduction.reproduction_status import ReproductionStatus


class Reproduction:

    def __init__(
        self,
        id: int,
        reproduction_type: ReproductionType,
        start_date: date,
        end_date: Optional[date],
        reproduction_status: ReproductionStatus,
        notes: Optional[str] = None,
        protocol_id: Optional[int] = None
    ):
        self.id = id
        self.reproduction_type = reproduction_type
        self.start_date = start_date
        self.end_date = end_date
        self.reproduction_status = reproduction_status
        self.notes = notes

        # Relacionamento com protocolo
        self.protocol_id = protocol_id

        # Relacionamento com execuções de etapas
        self.step_executions: List = []