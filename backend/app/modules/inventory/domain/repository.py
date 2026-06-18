from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.inventory.domain.entity import Animal


class AnimalRepository(ABC):
    @abstractmethod
    def get_by_id(self, animal_id: int, property_id: int) -> Optional[Animal]:
        pass

    @abstractmethod
    def get_by_identification(self, identification_number: int, property_id: int) -> Optional[Animal]:
        pass

    @abstractmethod
    def list_all(self, property_id: int) -> List[Animal]:
        pass

    @abstractmethod
    def save(self, animal: Animal) -> Animal:
        """Salva ou atualiza um animal."""
        pass

    @abstractmethod
    def delete(self, animal: Animal) -> None:
        """Remove um animal."""
        pass









































