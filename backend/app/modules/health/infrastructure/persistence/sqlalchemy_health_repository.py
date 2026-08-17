from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.health.domain.entity import HealthRecord
from app.modules.health.domain.repository import HealthRepository
from app.shared.infrastructure.persistence.mappers.health_mapper import to_domain, to_model
from app.modules.health.infrastructure.persistence.health import HealthModel


class SqlAlchemyHealthRepository(HealthRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, health_id: int, property_id: int) -> Optional[HealthRecord]:
        model = (
            self._session.query(HealthModel)
            .filter(
                HealthModel.id_health_record == health_id,
                HealthModel.property_id == property_id
            )
            .first()
        )
        return to_domain(model) if model else None

    def list_all(self, property_id: int) -> List[HealthRecord]:
        return [
            to_domain(m)
            for m in self._session.query(HealthModel)
            .filter(HealthModel.property_id == property_id)
            .all()
        ]

    def save(self, record: HealthRecord) -> HealthRecord:
        model = to_model(record)
        try:
            self._session.add(model)
            self._session.commit()
            self._session.refresh(model)
        except Exception:
            self._session.rollback()
            raise
        return to_domain(model)

    def update(self, health_id: int, property_id: int, data: dict) -> Optional[HealthRecord]:
        model = (
            self._session.query(HealthModel)
            .filter(
                HealthModel.id_health_record == health_id,
                HealthModel.property_id == property_id
            )
            .first()
        )
        if not model:
            return None
        for key, value in data.items():
            if key == "property_id":
                continue
            setattr(model, key, value)
        try:
            self._session.commit()
            self._session.refresh(model)
        except Exception:
            self._session.rollback()
            raise
        return to_domain(model)

    def delete(self, health_id: int, property_id: int) -> bool:
        model = (
            self._session.query(HealthModel)
            .filter(
                HealthModel.id_health_record == health_id,
                HealthModel.property_id == property_id
            )
            .first()
        )
        if not model:
            return False
        try:
            self._session.delete(model)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        return True










































