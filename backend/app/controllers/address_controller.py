from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.address import Address
from app.schemas.address_schema import AddressCreate, AddressResponse

router = APIRouter()


@router.post("/", response_model=AddressResponse, status_code=201)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    try:
        # Cria a instância do modelo Address com os dados do Schema
        new_address = Address(**address.model_dump())

        db.add(new_address)
        db.commit()
        db.refresh(new_address)

        return new_address
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar endereço: {str(e)}")
