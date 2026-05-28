from datetime import date
from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database.connection import Base


class DeathRecord(Base):
    """
    Representa o registro de óbito de um animal no sistema AiBoi.
    Mapeamento direto para o RDS.
    """
    __tablename__ = "death_records"

    # Identificação do Registro
    id = Column(Integer, primary_key=True, index=True)
    
    # Detalhes da Morte
    cause = Column(Text, nullable=False)
    death_date = Column(Date, default=date.today, nullable=False)
    
    # Chave Estrangeira Única (Um animal morre apenas uma vez)
    animal_id = Column(
        Integer, 
        ForeignKey("animals.id_animal"), 
        nullable=False, 
        unique=True
    )

    # Relacionamento
    # uselist=False garante a relação 1:1 (um registro para um animal)
    animal = relationship("AnimalModel", back_populates="death_record")