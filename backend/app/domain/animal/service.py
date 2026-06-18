from app.domain.animal.repository import AnimalRepository
from app.domain.shared.exceptions import DuplicateEntityError
from app.domain.animal.entity import Animal


class AnimalDomainService:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def validate_new_animal(self, animal: Animal) -> None:
        """Valida regras de negócio que dependem de estado global."""
        existing = self._repository.get_by_identification(animal.identification_number.value)
        if existing and existing.id != animal.id:
            raise DuplicateEntityError(
                "Animal", "identification_number", animal.identification_number.value
            )
