from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.health.entity import HealthRecord
from app.domain.health.repository import HealthRepository
from app.infrastructure.persistence.mappers.health_mapper import to_domain, to_model
from app.infrastructure.persistence.models.health import HealthModel


class SqlAlchemyHealthRepository(HealthRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, health_id: int) -> Optional[HealthRecord]:
        model = (
            self._session.query(HealthModel)
            .filter(HealthModel.id_health_record == health_id)
            .first()
        )
        return to_domain(model) if model else None

    def list_all(self) -> List[HealthRecord]:
        return [to_domain(m) for m in self._session.query(HealthModel).all()]

    def save(self, record: HealthRecord) -> HealthRecord:
        model = to_model(record)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return to_domain(model)

    def update(self, health_id: int, data: dict) -> Optional[HealthRecord]:
        model = (
            self._session.query(HealthModel)
            .filter(HealthModel.id_health_record == health_id)
            .first()
        )
        if not model:
            return None
        for key, value in data.items():
            setattr(model, key, value)
        self._session.commit()
        self._session.refresh(model)
        return to_domain(model)

    def delete(self, health_id: int) -> bool:
        model = (
            self._session.query(HealthModel)
            .filter(HealthModel.id_health_record == health_id)
            .first()
        )
        if not model:
            return False
        self._session.delete(model)
        self._session.commit()
        return True

