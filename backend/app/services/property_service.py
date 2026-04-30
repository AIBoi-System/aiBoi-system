from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.property_repository import PropertyRepository
from app.schemas.property_schema import PropertyCreateSchema, PropertyUpdateSchema
from app.models.property import Property
from app.models.user import User
from app.models.address import Address


class PropertyService:

    @staticmethod
    def create_property(db: Session, data: PropertyCreateSchema):
        # Regra 1: Validar se o Usuário existe
        owner = db.query(User).filter(User.id_user == data.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com ID {data.owner_id} não encontrado.",
            )

        # Regra 2: Validar se Address existe
        address = (
            db.query(Address).filter(Address.id_address == data.address_id).first()
        )
        if not address:
            raise HTTPException(
                status_code=404,
                detail="Endereço não encontrado. Crie um endereço antes!",
            )

        new_property = Property(
            name=data.name,
            area=data.size,  # Mapeando 'size' do schema para 'area' do banco
            property_type=data.property_type.value,
            owner_id=data.owner_id,
            address_id=data.address_id,
        )

        return PropertyRepository.create(db, new_property)

    @staticmethod
    def get_property_by_id(db: Session, property_id: int):
        property_item = (
            db.query(Property).filter(Property.id_property == property_id).first()
        )
        if not property_item:
            raise HTTPException(status_code=404, detail="Propriedade não encontrada.")
        return property_item

    @staticmethod
    def update_property(db: Session, property_id: int, data: PropertyUpdateSchema):
        # 1. Busca a propriedade no banco
        db_property = (
            db.query(Property).filter(Property.id_property == property_id).first()
        )
        if not db_property:
            raise HTTPException(
                status_code=404, detail="Propriedade não encontrada para atualização."
            )

        # Transformamos o schema em um dicionário contendo APENAS o que foi enviado no JSON
        update_data = data.model_dump(exclude_unset=True)

        # 2. Se mudar o dono, valida se o novo User existe
        if "owner_id" in update_data:
            owner = (
                db.query(User).filter(User.id_user == update_data["owner_id"]).first()
            )
            if not owner:
                raise HTTPException(
                    status_code=404, detail="Novo proprietário não encontrado."
                )
            db_property.owner_id = update_data["owner_id"]

        # 3. Se mudar o endereço, valida se existe
        if "address_id" in update_data:
            address = (
                db.query(Address)
                .filter(Address.id_address == update_data["address_id"])
                .first()
            )
            if not address:
                raise HTTPException(
                    status_code=404, detail="Novo endereço não encontrado."
                )
            db_property.address_id = update_data["address_id"]

        # 4. Atualiza os campos básicos se estiverem no dicionário
        if "name" in update_data:
            db_property.name = update_data["name"]

        if "size" in update_data:
            db_property.area = update_data[
                "size"
            ]  # Traduz 'size' do schema para 'area' do banco

        if "property_type" in update_data:
            # Pega o .value caso seja um Enum
            db_property.property_type = (
                update_data["property_type"].value
                if hasattr(update_data["property_type"], "value")
                else update_data["property_type"]
            )

        db.commit()
        db.refresh(db_property)
        return db_property

    @staticmethod
    def delete_property(db: Session, property_id: int):
        db_property = (
            db.query(Property).filter(Property.id_property == property_id).first()
        )
        if not db_property:
            raise HTTPException(
                status_code=404, detail="Propriedade não encontrada para exclusão."
            )

        db.delete(db_property)
        db.commit()
        return {"message": "Propriedade removida com sucesso"}
