from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.property.property_type import PropertyType


class Property(Base):
    """
    Representa uma propriedade rural (fazenda) no sistema AiBoi.
    Centraliza a gestão de áreas e serve como base para pastagens e piquetes.
    """
    __tablename__ = "properties"

    # Identificação da Propriedade
    id_property = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    
    # Atributos de Negócio
    property_type = Column(Enum(PropertyType), nullable=False)
    area = Column(Float, nullable=False) # Área total da propriedade em hectares

    # Chave Estrangeira para o Proprietário (Owner)
    owner_id = Column(Integer, ForeignKey("owners.id_owner"), nullable=False)

    # Relacionamentos
    owner = relationship("Owner", back_populates="properties")
    
    # Uma propriedade contém vários piquetes e pastagens
    paddocks = relationship(
        "Paddock", 
        back_populates="property", 
        cascade="all, delete-orphan"
    )
    pastures = relationship(
        "Pasture", 
        back_populates="property", 
        cascade="all, delete-orphan"
    )