from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import address_repository


class AddressService:
    @staticmethod
    def create_address(db: Session, address_data):
        try:
            # Transformamos o schema em dicionário para o repositório
            return address_repository.create_address(db, address_data.model_dump())
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar endereço: {str(e)}",
            )

    @staticmethod
    def get_all_addresses(db: Session):
        return address_repository.get_all_addresses(db)

    @staticmethod
    def get_address_by_id(db: Session, address_id: int):
        address = address_repository.get_address_by_id(db, address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado."
            )
        return address

    @staticmethod
    def update_address(db: Session, address_id: int, address_data):
        # model_dump(exclude_unset=True) garante que só vamos atualizar
        # os campos que o usuário realmente enviou no JSON
        update_data = address_data.model_dump(exclude_unset=True)

        updated = address_repository.update_address(db, address_id, update_data)

        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endereço não encontrado para atualização.",
            )
        return updated

    @staticmethod
    def delete_address(db: Session, address_id: int):
        deleted = address_repository.delete_address(db, address_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endereço não encontrado para exclusão.",
            )
        return {"detail": "Endereço removido com sucesso."}
