from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.presentation.schemas.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
)
from app.shared.infrastructure.persistence import address_repository
from app.shared.infrastructure.persistence.property import Property
from app.shared.infrastructure.persistence.property_repository import PropertyRepository
from app.shared.infrastructure.persistence.user import User
from app.modules.health.infrastructure.persistence.health import HealthModel
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.modules.inventory.infrastructure.persistence.batch import Batch
from app.modules.inventory.infrastructure.persistence.weighing import Weighing
from app.shared.infrastructure.persistence.paddock import Paddock
from app.shared.infrastructure.persistence.pasture import Pasture


class PropertyService:
    @staticmethod
    def _get_owner(db: Session, owner_id: int):
        owner = db.query(User).filter(User.id_user == owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found.")
        return owner

    @staticmethod
    def _ensure_address_assignable(
        db: Session,
        address_id: int,
        owner_id: int,
        exclude_property_id: int | None = None,
    ) -> None:
        if not address_repository.is_address_assignable_to_owner(
            db, address_id, owner_id, exclude_property_id=exclude_property_id
        ):
            raise HTTPException(status_code=404, detail="Address not found.")

    @staticmethod
    def create_property(
        db: Session,
        data: PropertyCreateSchema,
        actor_id: int,
        is_admin: bool = False,
    ):
        owner_id = data.owner_id if is_admin else actor_id
        PropertyService._get_owner(db, owner_id)
        PropertyService._ensure_address_assignable(db, data.address_id, owner_id)
        return PropertyRepository.create(
            db,
            Property(
                name=data.name,
                area=data.size,
                property_type=data.property_type.value,
                owner_id=owner_id,
                address_id=data.address_id,
            ),
        )

    @staticmethod
    def get_property_by_id(
        db: Session, property_id: int, owner_id: int | None = None
    ):
        property_item = PropertyRepository.get_by_id(db, property_id, owner_id=owner_id)
        if not property_item:
            raise HTTPException(status_code=404, detail="Property not found.")
        return property_item

    @staticmethod
    def get_all_properties(db: Session, owner_id: int | None = None):
        return PropertyRepository.get_all(db, owner_id=owner_id)

    @staticmethod
    def update_property(
        db: Session,
        property_id: int,
        data: PropertyUpdateSchema,
        actor_id: int,
        is_admin: bool = False,
    ):
        db_property = PropertyService.get_property_by_id(
            db, property_id, owner_id=None if is_admin else actor_id
        )
        update_data = data.model_dump(exclude_unset=True)
        requested_owner_id = update_data.pop("owner_id", None)
        if not is_admin and requested_owner_id not in (None, db_property.owner_id):
            raise HTTPException(
                status_code=400,
                detail="Moving a property between owners is not allowed.",
            )

        target_owner_id = (
            requested_owner_id
            if is_admin and requested_owner_id is not None
            else db_property.owner_id
        )
        if target_owner_id != db_property.owner_id:
            PropertyService._get_owner(db, target_owner_id)

        target_address_id = update_data.pop("address_id", db_property.address_id)
        if target_address_id is not None and (
            target_address_id != db_property.address_id
            or target_owner_id != db_property.owner_id
        ):
            PropertyService._ensure_address_assignable(
                db,
                target_address_id,
                target_owner_id,
                exclude_property_id=property_id,
            )

        db_property.owner_id = target_owner_id
        db_property.address_id = target_address_id
        if "name" in update_data:
            db_property.name = update_data["name"]
        if "size" in update_data:
            db_property.area = update_data["size"]
        if "property_type" in update_data:
            property_type = update_data["property_type"]
            db_property.property_type = getattr(property_type, "value", property_type)
        return PropertyRepository.update(db, db_property)

    @staticmethod
    def delete_property(
        db: Session,
        property_id: int,
        actor_id: int,
        is_admin: bool = False,
    ):
        db_property = PropertyService.get_property_by_id(
            db, property_id, owner_id=None if is_admin else actor_id
        )
        PropertyRepository.delete(db, db_property)
        return {"message": "Property deleted successfully."}

    @staticmethod
    def get_dashboard(
        db: Session,
        property_id: int,
        actor_id: int,
        is_admin: bool = False,
    ) -> dict:
        property_item = PropertyService.get_property_by_id(
            db, property_id, owner_id=None if is_admin else actor_id
        )
        recent_weighings = (
            db.query(Weighing, AnimalModel.identification_number)
            .join(AnimalModel, Weighing.animal_id == AnimalModel.id_animal)
            .filter(AnimalModel.property_id == property_id)
            .order_by(Weighing.weigh_date.desc())
            .limit(5)
            .all()
        )
        recent_health = (
            db.query(HealthModel)
            .filter(HealthModel.property_id == property_id)
            .order_by(HealthModel.application_date.desc())
            .limit(5)
            .all()
        )
        return {
            "property_id": property_id,
            "property_name": property_item.name,
            "total_animals": db.query(AnimalModel)
            .filter(AnimalModel.property_id == property_id)
            .count(),
            "total_pastures": db.query(Pasture)
            .filter(Pasture.property_id == property_id)
            .count(),
            "total_paddocks": db.query(Paddock)
            .filter(Paddock.property_id == property_id)
            .count(),
            "total_batches": db.query(Batch)
            .filter(Batch.property_id == property_id)
            .count(),
            "recent_weighings": [
                {
                    "id": weighing.id,
                    "weight": weighing.weight,
                    "weigh_date": weighing.weigh_date,
                    "animal_id": weighing.animal_id,
                    "animal_identification": identification,
                }
                for weighing, identification in recent_weighings
            ],
            "recent_health_records": [
                {
                    "id_health_record": record.id_health_record,
                    "health_type": getattr(
                        record.health_type, "value", record.health_type
                    ),
                    "product_name": record.product_name,
                    "application_date": record.application_date,
                    "responsible": record.responsible,
                    "animal_id": record.animal_id,
                }
                for record in recent_health
            ],
        }
