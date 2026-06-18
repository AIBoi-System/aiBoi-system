from app.modules.inventory.domain.repository import AnimalRepository
from app.shared.domain.exceptions import DuplicateEntityError
from app.modules.inventory.domain.entity import Animal


class AnimalDomainService:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def validate_new_animal(self, animal: Animal) -> None:
        """Valida regras de negócio que dependem de estado global e contexto de propriedade."""
        existing = self._repository.get_by_identification(
            animal.identification_number.value,
            property_id=animal.property_id
        )
        if existing and existing.id != animal.id:
            raise DuplicateEntityError(
                "Animal", "identification_number", animal.identification_number.value
            )









































