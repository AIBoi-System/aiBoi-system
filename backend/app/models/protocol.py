from typing import List

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.reproduction.reproduction_type import ReproductionType
from app.enums.protocol.protocol_status import ProtocolStatus  # <-- IMPORTADO


class Protocol(Base):
    """
    Representa um protocolo reprodutivo (ex: IATF) no sistema AiBoi.
    Define o conjunto de regras e etapas que um animal deve seguir.
    """

    __tablename__ = "protocols"

    # Identificação do Protocolo
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Tipo de Reprodução (Usa o Enum fornecido)
    type = Column(Enum(ReproductionType), nullable=False)

    # Status do Protocolo (Adicionado do seu Diagrama de Classes)
    status = Column(
        Enum(ProtocolStatus), nullable=False, default=ProtocolStatus.IN_PROGRESS
    )

    # Relacionamentos
    # Um protocolo possui várias etapas (Steps) organizadas
    steps = relationship(
        "Step",
        back_populates="protocol",
        cascade="all, delete-orphan",
        order_by="Step.day",  # Agora isso vai funcionar perfeitamente!
    )
