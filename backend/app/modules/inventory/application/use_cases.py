from typing import List

from app.modules.inventory.domain.entity import Animal
from app.modules.inventory.domain.repository import AnimalRepository
from app.modules.inventory.domain.animal_domain_service import AnimalDomainService
from app.shared.domain.exceptions import EntityNotFoundError


class CreateAnimalUseCase:
    def __init__(self, repository: AnimalRepository, domain_service: AnimalDomainService):
        self._repository = repository
        self._domain_service = domain_service

    def execute(self, animal: Animal) -> Animal:
        self._domain_service.validate_new_animal(animal)
        return self._repository.save(animal)


class ListAnimalsUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, property_id: int) -> List[Animal]:
        return self._repository.list_all(property_id=property_id)


class GetAnimalUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, animal_id: int, property_id: int) -> Animal:
        animal = self._repository.get_by_id(animal_id, property_id=property_id)
        if not animal:
            raise EntityNotFoundError("Animal", animal_id)
        return animal


class UpdateAnimalUseCase:
    def __init__(self, repository: AnimalRepository, domain_service: AnimalDomainService):
        self._repository = repository
        self._domain_service = domain_service

    def execute(self, animal_id: int, property_id: int, data: dict) -> Animal:
        animal = self._repository.get_by_id(animal_id, property_id=property_id)
        if not animal:
            raise EntityNotFoundError("Animal", animal_id)

        for key, value in data.items():
            if hasattr(animal, key) and key != "property_id":
                if key == "identification_number":
                    from app.modules.inventory.domain.value_objects import IdentificationNumber
                    setattr(animal, key, IdentificationNumber(value))
                elif key in ["weaning_weight", "birth_weight"]:
                    from app.modules.inventory.domain.value_objects import Weight
                    setattr(animal, key, Weight(value) if value is not None else None)
                else:
                    setattr(animal, key, value)

        self._domain_service.validate_new_animal(animal)
        return self._repository.save(animal)


class DeleteAnimalUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, animal_id: int, property_id: int) -> None:
        animal = self._repository.get_by_id(animal_id, property_id=property_id)
        if not animal:
            raise EntityNotFoundError("Animal", animal_id)
        self._repository.delete(animal)









































