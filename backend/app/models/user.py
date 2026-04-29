from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    phone = Column(String(20), nullable=True)
    account_status = Column(String(50), default="Ativo")

    cpf = Column(String(14), unique=True, nullable=False)

    address_id = Column(Integer, ForeignKey("addresses.id_address"), nullable=True)
    address = relationship("Address")

    type = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type
    }