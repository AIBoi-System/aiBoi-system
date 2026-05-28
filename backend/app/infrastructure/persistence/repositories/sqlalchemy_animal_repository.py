from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.animal.entity import Animal
from app.domain.animal.repository import AnimalRepository
from app.infrastructure.persistence.mappers.animal_mapper import to_domain, to_model
from app.infrastructure.persistence.models.animal import AnimalModel


class SqlAlchemyAnimalRepository(AnimalRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, animal_id: int) -> Optional[Animal]:
        model = (
            self._session.query(AnimalModel)
            .filter(AnimalModel.id_animal == animal_id)
            .first()
        )
        return to_domain(model) if model else None

    def get_by_identification(self, identification_number: int) -> Optional[Animal]:
        model = (
            self._session.query(AnimalModel)
            .filter(AnimalModel.identification_number == identification_number)
            .first()
        )
        return to_domain(model) if model else None

    def list_all(self) -> List[Animal]:
        models = self._session.query(AnimalModel).all()
        return [to_domain(m) for m in models]

    def save(self, animal: Animal) -> Animal:
        model = to_model(animal)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return to_domain(model)

    def update(self, animal_id: int, data: dict) -> Optional[Animal]:
        model = (
            self._session.query(AnimalModel)
            .filter(AnimalModel.id_animal == animal_id)
            .first()
        )
        if not model:
            return None
        for key, value in data.items():
            setattr(model, key, value)
        self._session.commit()
        self._session.refresh(model)
        return to_domain(model)

