from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.infrastructure.database.connection import Base
from app.enums.property.property_type import PropertyType


class Property(Base):
    __tablename__ = "properties"

    id_property = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False)
    area = Column(Float, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id_address"), nullable=True)

    # Relacionamentos
    owner = relationship("User", back_populates="properties")

    address = relationship("Address")

    paddocks = relationship(
        "Paddock",
        back_populates="property",
        cascade="all, delete-orphan",
        overlaps="paddocks,pasture",
    )
    pastures = relationship(
        "Pasture", back_populates="property", cascade="all, delete-orphan"
    )










































