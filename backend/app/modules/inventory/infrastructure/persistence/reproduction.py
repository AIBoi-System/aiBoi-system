from datetime import date
from sqlalchemy import Column, Integer, Date, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base
from app.enums.reproduction.reproduction_type import ReproductionType
from app.enums.reproduction.reproduction_status import ReproductionStatus
from app.enums.reproduction.reproduction_result import (
    ReproductionResult,
)  # <-- ADICIONADO


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

    # <-- ADICIONADOS DO SEU DIAGRAMA DE CLASSES -->
    diagnosis_date = Column(Date, nullable=True)
    result = Column(Enum(ReproductionResult), nullable=True)

    notes = Column(
        Text, nullable=True
    )  # O Sandro usou 'notes' em vez de 'observation', mantivemos o dele para não quebrar o banco

    # Chaves Estrangeiras
    animal_id = Column(
        Integer,
        ForeignKey("animals.id_animal"),
        nullable=False,
        index=True,
    )
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=True, index=True)

    # Relacionamentos
    animal = relationship("AnimalModel", back_populates="reproductions")
    protocol = relationship("Protocol", back_populates="reproductions")

    # Execuções das etapas do protocolo (D0, D7, etc.)
    step_executions = relationship(
        "StepExecution", back_populates="reproduction", cascade="all, delete-orphan"
    )










































