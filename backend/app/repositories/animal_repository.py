from sqlalchemy.orm import Session
from app.models.animal import Animal
from app.models.animal_event import AnimalEvent
from app.models.animal_movement import AnimalMovement
from app.models.owner import Owner
def get_animal_by_id(db: Session, id_animal: int):
    return db.query(Animal).filter(Animal.id_animal == id_animal).first()

def get_animal_by_identification(db: Session, ident_number: int):
    return db.query(Animal).filter(Animal.identification_number == ident_number).first()

def get_all_animals(db: Session):
    return db.query(Animal).all()

def create_animal(db: Session, animal_data: dict):
    db_animal = Animal(**animal_data)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def update_animal(db: Session, id_animal: int, data: dict):
    db_animal = get_animal_by_id(db, id_animal)
    if db_animal:
        for key, value in data.items():
            setattr(db_animal, key, value)
        db.commit()
        db.refresh(db_animal)
    return db_animal