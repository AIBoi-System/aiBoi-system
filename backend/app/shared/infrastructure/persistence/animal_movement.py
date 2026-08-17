from sqlalchemy import Column, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.infrastructure.database.connection import Base #
from datetime import date
from typing import Optional

class AnimalMovement(Base):
    """
    Modelo de base de dados para o histórico de movimentação de animais entre lotes.
    """
    __tablename__ = "animal_movements"

    id_movement = Column(Integer, primary_key=True, index=True)
    movement_date = Column(Date, default=date.today, nullable=False)
    notes = Column(Text, nullable=True)

    # Chaves Estrangeiras para Animal e Lotes
    animal_id = Column(
        Integer,
        ForeignKey("animals.id_animal"),
        nullable=False,
        index=True,
    )
    origin_batch_id = Column(
        Integer,
        ForeignKey("batches.id_batch"),
        nullable=False,
        index=True,
    )
    destination_batch_id = Column(
        Integer,
        ForeignKey("batches.id_batch"),
        nullable=False,
        index=True,
    )

    # Relacionamentos para facilitar consultas no sistema 
    animal = relationship("AnimalModel", back_populates="movements")
    origin_batch = relationship("Batch", foreign_keys=[origin_batch_id])
    destination_batch = relationship("Batch", foreign_keys=[destination_batch_id])

    def __init__(
        self,
        animal_id: int,
        origin_batch: int,
        destination_batch: int,
        movement_date: date,
        id_movement: Optional[int] = None,
        notes: Optional[str] = None
    ):
        self.id_movement = id_movement
        self.animal_id = animal_id
        self.origin_batch_id = origin_batch
        self.destination_batch_id = destination_batch
        self.movement_date = movement_date
        self.notes = notes









































