from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.inventory.domain.entity import Animal
from app.modules.inventory.domain.repository import AnimalRepository
from app.shared.infrastructure.persistence.mappers.animal_mapper import to_domain, to_model
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel


class SqlAlchemyAnimalRepository(AnimalRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, animal_id: int, property_id: int) -> Optional[Animal]:
        model = (
            self._session.query(AnimalModel)
            .filter(
                AnimalModel.id_animal == animal_id,
                AnimalModel.property_id == property_id
            )
            .first()
        )
        return to_domain(model) if model else None

    def get_by_identification(self, identification_number: int, property_id: int) -> Optional[Animal]:
        model = (
            self._session.query(AnimalModel)
            .filter(
                AnimalModel.identification_number == identification_number,
                AnimalModel.property_id == property_id
            )
            .first()
        )
        return to_domain(model) if model else None

    def list_all(self, property_id: int) -> List[Animal]:
        models = (
            self._session.query(AnimalModel)
            .filter(AnimalModel.property_id == property_id)
            .all()
        )
        return [to_domain(m) for m in models]

    def save(self, animal: Animal) -> Animal:
        if animal.id:
            # Update existing
            model = (
                self._session.query(AnimalModel)
                .filter(
                    AnimalModel.id_animal == animal.id,
                    AnimalModel.property_id == animal.property_id
                )
                .first()
            )
            if model:
                # Update attributes from entity to model
                entity_model = to_model(animal)
                for column in AnimalModel.__table__.columns:
                    if column.name not in ["id_animal", "property_id"]:
                        setattr(model, column.name, getattr(entity_model, column.name))
            else:
                model = to_model(animal)
                self._session.add(model)
        else:
            # Create new
            model = to_model(animal)
            self._session.add(model)

        self._session.commit()
        self._session.refresh(model)
        return to_domain(model)

    def delete(self, animal: Animal) -> None:
        if animal.id:
            model = (
                self._session.query(AnimalModel)
                .filter(
                    AnimalModel.id_animal == animal.id,
                    AnimalModel.property_id == animal.property_id
                )
                .first()
            )
            if model:
                self._session.delete(model)
                self._session.commit()









































