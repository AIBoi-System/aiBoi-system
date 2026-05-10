from sqlalchemy.orm import Session
from app.models.health import Health


def create_health_record(db: Session, health_data: dict):
    """
    Cria um registro de saúde (vacina, medicamento, tratamento) no banco de dados.
    health_data: dicionário já validado e formatado pelo Service.
    """
    health = Health(**health_data)
    
    db.add(health)
    db.commit()
    db.refresh(health)
    return health


def get_health_record_by_id(db: Session, health_id: int):
    """Busca um registro de saúde por ID."""
    return db.query(Health).filter(Health.id_health_record == health_id).first()


def get_health_records_by_animal(db: Session, animal_id: int):
    """Busca todos os registros de saúde de um animal específico."""
    return db.query(Health).filter(Health.animal_id == animal_id).all()


def get_health_records_by_batch(db: Session, batch_id: int):
    """Busca todos os registros de saúde de um lote específico."""
    return db.query(Health).filter(Health.batch_id == batch_id).all()


def get_all_health_records(db: Session):
    """Retorna todos os registros de saúde."""
    return db.query(Health).all()


def update_health_record(db: Session, health_id: int, health_data: dict):
    """
    Atualiza um registro de saúde.
    health_data: dicionário com os campos que devem ser alterados.
    """
    health = get_health_record_by_id(db, health_id)

    if not health:
        return None

    # Itera sobre o dicionário já tratado pelo Service
    for key, value in health_data.items():
        setattr(health, key, value)

    db.commit()
    db.refresh(health)
    return health


def delete_health_record(db: Session, health_id: int):
    """Deleta um registro de saúde."""
    health = get_health_record_by_id(db, health_id)

    if health:
        db.delete(health)
        db.commit()
        return True
    
    return False
