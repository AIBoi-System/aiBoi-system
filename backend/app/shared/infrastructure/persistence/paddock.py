from sqlalchemy import Column, Integer, String, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.shared.infrastructure.database.connection import Base
from app.enums.paddock.paddocke_status import PaddockeStatus


class Paddock(Base):
    __tablename__ = "paddocks"

    id_paddock = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    area_ha = Column(Float, nullable=False)
    grass_type = Column(String(100), nullable=True)
    forage_quality = Column(String(100), nullable=True)
    animal_capacity = Column(Integer, nullable=False)
    paddock_status = Column(Enum(PaddockeStatus), nullable=False)
    notes = Column(Text, nullable=True)

    # --- CHAVES ESTRANGEIRAS ---
    property_id = Column(Integer, ForeignKey("properties.id_property"), nullable=False)
    # LIGAÇÃO COM O PASTO (Resolvendo o NoForeignKeysError)
    pasture_id = Column(Integer, ForeignKey("pastures.id_pasture"), nullable=True)

    # --- RELACIONAMENTOS ---
    property = relationship("Property", back_populates="paddocks")
    pasture = relationship("Pasture", back_populates="paddocks")

    movements_as_origin = relationship(
        "BatchMovement",
        foreign_keys="[BatchMovement.origin_paddock_id]",
        back_populates="origin_paddock",
    )
    movements_as_destination = relationship(
        "BatchMovement",
        foreign_keys="[BatchMovement.destination_paddock_id]",
        back_populates="destination_paddock",
    )










































