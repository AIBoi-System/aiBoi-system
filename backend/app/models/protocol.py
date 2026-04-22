from typing import List

from app.models.step import Step
from backend.app.enums.reproduction.reproduction_type import ReproductionType

class Protocol:

    def __init__(
        self,
        id: int,
        name: str,
        type: ReproductionType
    ):
        self.id = id
        self.name = name
        self.type = type

        # Etapas do protocolo
        self.steps: List["Step"] = []