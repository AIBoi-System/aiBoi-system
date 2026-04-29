from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.property_repository import PropertyRepository
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema
from app.models.property import Property
from app.models.owner import Owner
from app.models.address import Address


class PropertyService:

    @staticmethod
    def create_property(db: Session, data: PropertyCreateSchema):
        # Regra 1: Validar se Owner existe
        owner = db.query(Owner).filter(Owner.id_user == data.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=404,
                detail="Owner (Proprietário) não encontrado no banco de dados.",
            )

        # Regra 2: validar se Address existe
        address = (
            db.query(Address).filter(Address.id_address == data.address_id).first()
        )
        if not address:
            raise HTTPException(
                status_code=404,
                detail="Address (Endereço) não encontrado no banco de dados.",
            )

        # Transformação (DTO): Pegamos os dados do schema e montamos o modelo do banco
        new_property = Property(
            name=data.name,
            total_area=data.size,  # Mapeando o 'size' da API para o 'total_area' do banco
            property_type=data.property_type.value,
            id_owner=data.owner_id,
            id_address=data.address_id,
        )

        return PropertyRepository.create(db, new_property)

    @staticmethod
    def get_property(db: Session, property_id: int):
        prop = PropertyRepository.get_by_id(db, property_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Propriedade não encontrada.")
        return prop

    @staticmethod
    def get_all_properties(db: Session):
        return PropertyRepository.get_all(db)

    @staticmethod
    def update_property(db: Session, property_id: int, data: PropertyUpdateSchema):
        prop = PropertyService.get_property(
            db, property_id
        )  # aproveita a validação acima

        if data.name:
            prop.name = data.name
        if data.size:
            prop.total_area = data.size
        if data.property_type:
            prop.property_type = data.property_type.value

        return PropertyRepository.update(db, prop)

    @staticmethod
    def delete_property(db: Session, property_id: int):
        prop = PropertyService.get_property(db, property_id)
        PropertyRepository.delete(db, prop)
        return {"message": "Propriedade deletada com sucesso!"}
