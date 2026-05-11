from sqlalchemy.orm import Session


from app.models.health import Health
from app.schemas.health.health_create import HealthCreate
from app.schemas.health.health_update import HealthUpdate


class HealthRepository:

    @staticmethod
    def create(db: Session, data: HealthCreate):
        health = Health(**data.model_dump())

        db.add(health)
        db.commit()
        db.refresh(health)

        return health

    @staticmethod
    def get_by_id(db: Session, health_id: int):
        return db.query(Health).filter(
            Health.id_health_record == health_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Health).all()

    @staticmethod
    def update(db: Session, health_id: int, data: HealthUpdate):
        health = db.query(Health).filter(
            Health.id_health_record == health_id
        ).first()

        if not health:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(health, field, value)

        db.commit()
        db.refresh(health)

        return health

    @staticmethod
    def delete(db: Session, health_id: int):
        health = db.query(Health).filter(
            Health.id_health_record == health_id
        ).first()

        if not health:
            return None

        db.delete(health)
        db.commit()

        return health

