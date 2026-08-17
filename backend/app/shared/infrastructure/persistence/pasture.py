from sqlalchemy import (
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.shared.infrastructure.database.connection import Base
from app.enums.pasture.pasture_management import PastureManagement


class Pasture(Base):
    __tablename__ = "pastures"
    __table_args__ = (
        UniqueConstraint(
            "id_pasture",
            "property_id",
            name="uq_pastures_id_property",
        ),
    )

    id_pasture = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    area = Column(Float, nullable=False)
    capacity = Column(Integer, nullable=False)
    grazing_management = Column(Enum(PastureManagement), nullable=False)
    notes = Column(Text, nullable=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id_property"),
        nullable=False,
        index=True,
    )

    # Relacionamentos
    property = relationship("Property", back_populates="pastures")
    # CONECTADO AO PADDOCK
    paddocks = relationship(
        "Paddock",
        back_populates="pasture",
        cascade="all, delete-orphan",
        overlaps="property",
    )










































