from typing import List

from app.domain.animal.entity import Animal
from app.domain.animal.repository import AnimalRepository
from app.domain.shared.exceptions import EntityNotFoundError


class CreateAnimalUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, animal: Animal) -> Animal:
        existing = self._repository.get_by_identification(animal.identification_number)
        animal.ensure_unique_identification(existing is not None)
        return self._repository.save(animal)


class ListAnimalsUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self) -> List[Animal]:
        return self._repository.list_all()


class GetAnimalUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, animal_id: int) -> Animal:
        animal = self._repository.get_by_id(animal_id)
        if not animal:
            raise EntityNotFoundError("Animal", animal_id)
        return animal


class UpdateAnimalUseCase:
    def __init__(self, repository: AnimalRepository):
        self._repository = repository

    def execute(self, animal_id: int, data: dict) -> Animal:
        if not self._repository.get_by_id(animal_id):
            raise EntityNotFoundError("Animal", animal_id)
        updated = self._repository.update(animal_id, data)
        if not updated:
            raise EntityNotFoundError("Animal", animal_id)
        return updated

