from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.persistence.models.owner_module import OwnerModule


class OwnerModuleService:
    @staticmethod
    def assign_module(db: Session, data):
        existing = (
            db.query(OwnerModule)
            .filter(
                OwnerModule.owner_id == data.owner_id,
                OwnerModule.module_name == data.module_name,
            )
            .first()
        )
        if existing:
            existing.is_active = data.is_active
            db.commit()
            db.refresh(existing)
            return existing

        record = OwnerModule(**data.model_dump())
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list_owner_modules(db: Session, owner_id: int):
        return db.query(OwnerModule).filter(OwnerModule.owner_id == owner_id).all()

    @staticmethod
    def ensure_owner_has_module(db: Session, owner_id: int, module_name):
        module = (
            db.query(OwnerModule)
            .filter(
                OwnerModule.owner_id == owner_id,
                OwnerModule.module_name == module_name,
                OwnerModule.is_active.is_(True),
            )
            .first()
        )
        if not module:
            raise HTTPException(
                status_code=403,
                detail=f"Module {module_name.value} is not active for this owner.",
            )
