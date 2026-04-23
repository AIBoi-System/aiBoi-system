from sqlalchemy import Column, Integer, String, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.enums.pasture.pasture_management import PastureManagement


class Pasture(Base):
    """
    Representa uma área de pastagem no sistema AiBoi.
    Define o tipo de manejo (rotacionado, contínuo, etc.) e a capacidade produtiva.
    """
    __tablename__ = "pastures"

    # Identificação
    id_pasture = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Atributos de Área e Capacidade
    area = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False) # Capacidade em UA (Unidade Animal) ou cabeças
    
    # Manejo (Usa o Enum fornecido)
    grazing_management = Column(Enum(PastureManagement), nullable=False)
    
    notes = Column(Text, nullable=True)

    # Relacionamento com a Propriedade (Fazenda)
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False)

    # Relacionamentos
    property = relationship("Property", back_populates="pastures")
    
    # Caso sua lógica vincule Piquetes a Pastagens
    paddocks = relationship("Paddock", backref="pasture", cascade="all, delete-orphan")