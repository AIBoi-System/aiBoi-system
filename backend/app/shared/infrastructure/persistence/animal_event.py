from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.shared.infrastructure.database.connection import Base #
from datetime import date
from typing import Optional

class AnimalEvent(Base):
    """
    Modelo de banco de dados para o histórico de eventos de um animal.
    Consolida eventos de pesagem, sanidade, reprodução e movimentação de lotes.
    """
    __tablename__ = "animal_events"

    id_event = Column(Integer, primary_key=True, index=True)
    event_date = Column(Date, default=date.today, nullable=False)
    event_type = Column(String(50), nullable=False)  # Ex: 'PESAGEM', 'SANIDADE', 'REPRODUCAO', 'LOTE'
    description = Column(Text, nullable=True)

    # Chave Estrangeira obrigatória para o Animal
    animal_id = Column(Integer, ForeignKey("animals.id_animal"), nullable=False)
    
    # Chaves Estrangeiras opcionais para rastreabilidade
    weighing_id = Column(Integer, ForeignKey("weighings.id"), nullable=True) 
    health_id = Column(Integer, ForeignKey("health_records.id_health_record"), nullable=True) 
    reproduction_id = Column(Integer, ForeignKey("reproductions.id"), nullable=True) 
    batch_id = Column(Integer, ForeignKey("batches.id_batch"), nullable=True) 

    # Relacionamento para facilitar consultas
    animal = relationship("AnimalModel", back_populates="events")

    def __init__(
        self,
        id_event: int,
        event_date: date,
        event_type: str,
        animal_id: int,
        description: Optional[str] = None,
        weighing_id: Optional[int] = None,
        health_id: Optional[int] = None,
        reproduction_id: Optional[int] = None,
        batch_id: Optional[int] = None
    ):
        self.id_event = id_event
        self.event_date = event_date
        self.event_type = event_type
        self.animal_id = animal_id
        self.description = description
        self.weighing_id = weighing_id
        self.health_id = health_id
        self.reproduction_id = reproduction_id
        self.batch_id = batch_id









































