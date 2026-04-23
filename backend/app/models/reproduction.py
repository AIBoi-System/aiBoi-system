from datetime import date
from typing import List, Optional

from sqlalchemy import Column, Integer, Date, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.reproduction.reproduction_type import ReproductionType
from app.enums.reproduction.reproduction_status import ReproductionStatus


class Reproduction(Base):
    """
    Representa o ciclo reprodutivo de uma matriz no sistema AiBoi.
    Vincula animais a protocolos (como IATF) e monitora o status da prenhez.
    """
    __tablename__ = "reproductions"

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    
    # Dados do Ciclo
    reproduction_type = Column(Enum(ReproductionType), nullable=False)
    reproduction_status = Column(Enum(ReproductionStatus), nullable=False)
    start_date = Column(Date, default=date.today, nullable=False)
    end_date = Column(Date, nullable=True)
    
    notes = Column(Text, nullable=True)

    # Chaves Estrangeiras
    animal_id = Column(Integer, ForeignKey("animals.id_animal"), nullable=False)
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=True)

    # Relacionamentos
    animal = relationship("Animal", back_populates="reproductions")
    protocol = relationship("Protocol")
    
    # Execuções das etapas do protocolo (D0, D7, etc.)
    step_executions = relationship(
        "StepExecution", 
        back_populates="reproduction", 
        cascade="all, delete-orphan"
    )