from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.animal.entity import Animal


class AnimalRepository(ABC):
    @abstractmethod
    def get_by_id(self, animal_id: int) -> Optional[Animal]:
        pass

    @abstractmethod
    def get_by_identification(self, identification_number: int) -> Optional[Animal]:
        pass

    @abstractmethod
    def list_all(self) -> List[Animal]:
        pass

    @abstractmethod
    def save(self, animal: Animal) -> Animal:
        pass

    @abstractmethod
    def update(self, animal_id: int, data: dict) -> Optional[Animal]:
        pass
