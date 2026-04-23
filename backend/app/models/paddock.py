from sqlalchemy import Column, Integer, String, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.paddock.paddocke_status import PaddockeStatus


class Paddock(Base):
    """
    Representa um piquete ou divisão de pasto dentro de uma propriedade.
    Essencial para o manejo rotacionado e controle de capacidade de carga.
    """
    __tablename__ = "paddocks"

    # Identificação
    id_paddock = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Atributos Físicos e Produtivos
    area_ha = Column(Float, nullable=False)
    grass_type = Column(String(100), nullable=True)
    forage_quality = Column(String(100), nullable=True)
    animal_capacity = Column(Integer, nullable=False)
    
    # Status (Usa o Enum fornecido)
    paddock_status = Column(Enum(PaddockeStatus), nullable=False)
    
    notes = Column(Text, nullable=True)

    # Relacionamento com a Propriedade (Fazenda)
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False)

    # Relacionamentos
    property = relationship("Property", back_populates="paddocks")
    
    # Movimentações de lotes associadas a este piquete
    # (Relacionado ao origin_paddock_id e destination_paddock_id do BatchMovement)
    movements_as_origin = relationship(
        "BatchMovement", 
        foreign_keys="[BatchMovement.origin_paddock_id]",
        back_populates="origin_paddock"
    )
    movements_as_destination = relationship(
        "BatchMovement", 
        foreign_keys="[BatchMovement.destination_paddock_id]",
        back_populates="destination_paddock"
    )