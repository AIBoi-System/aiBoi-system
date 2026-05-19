from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from app.core.database import get_db
from app.schemas.pasture_schema import PastureCreate, PastureUpdate, PastureResponse
from app.services.pasture_service import pasture_service

router = APIRouter(prefix="/pastures", tags=["Pastures"])


@router.post("/", response_model=PastureResponse, status_code=status.HTTP_201_CREATED)
def create_pasture(pasture: PastureCreate, db: Session = Depends(get_db)):
    return pasture_service.create_pasture(db, pasture)


@router.get("/", response_model=List[PastureResponse])
def get_pastures(
    skip: int = 0,
    limit: int = 100,
    property_id: int = None,
    db: Session = Depends(get_db),
):
    return pasture_service.get_pastures(
        db, skip=skip, limit=limit, property_id=property_id
    )


@router.get("/{pasture_id}", response_model=PastureResponse)
def get_pasture(pasture_id: int, db: Session = Depends(get_db)):
    return pasture_service.get_pasture(db, pasture_id)


@router.put("/{pasture_id}", response_model=PastureResponse)
def update_pasture(
    pasture_id: int, pasture_update: PastureUpdate, db: Session = Depends(get_db)
):
    return pasture_service.update_pasture(db, pasture_id, pasture_update)


@router.delete("/{pasture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pasture(pasture_id: int, db: Session = Depends(get_db)):
    pasture_service.delete_pasture(db, pasture_id)
    return None
