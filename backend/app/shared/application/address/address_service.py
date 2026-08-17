from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.shared.infrastructure.persistence import address_repository


class AddressService:
    @staticmethod
    def create_address(db: Session, address_data):
        try:
            return address_repository.create_address(db, address_data.model_dump())
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create address.",
            ) from exc

    @staticmethod
    def get_all_addresses(db: Session):
        return address_repository.get_all_addresses(db)

    @staticmethod
    def get_address_by_id(
        db: Session, address_id: int, owner_id: int | None = None
    ):
        address = address_repository.get_address_by_id(
            db, address_id, owner_id=owner_id
        )
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found.",
            )
        return address

    @staticmethod
    def update_address(
        db: Session,
        address_id: int,
        address_data,
        owner_id: int | None = None,
    ):
        updated = address_repository.update_address(
            db,
            address_id,
            address_data.model_dump(exclude_unset=True),
            owner_id=owner_id,
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found.",
            )
        return updated

    @staticmethod
    def delete_address(db: Session, address_id: int):
        deleted = address_repository.delete_address(db, address_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found.",
            )
        return {"detail": "Address deleted successfully."}
