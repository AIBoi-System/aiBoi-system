from sqlalchemy import Column, Integer, String, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.enums.pasture.pasture_management import PastureManagement


class Pasture(Base):
    __tablename__ = "pastures"

    id_pasture = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    grazing_management = Column(Enum(PastureManagement), nullable=False)
    notes = Column(Text, nullable=True)

    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False)

    # Relacionamentos
    property = relationship("Property", back_populates="pastures")
    # CONECTADO AO PADDOCK
    paddocks = relationship(
        "Paddock", back_populates="pasture", cascade="all, delete-orphan"
    )
