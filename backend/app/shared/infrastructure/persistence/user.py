from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    phone = Column(String(20), nullable=True)
    account_status = Column(String(50), default="Ativo")

    cpf_record = relationship(
        "CPF",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )
    cpf = association_proxy(
        "cpf_record",
        "number",
        creator=lambda value: _create_cpf_record(value),
    )

    auth_sessions = relationship(
        "AuthSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Endereço
    address_id = Column(Integer, ForeignKey("addresses.id_address"), nullable=True)
    # Ajustado para back_populates se o seu model de Address permitir
    address = relationship("Address")

    # --- O PONTO CHAVE ---
    # Adicionamos esta linha para que o User reconheça suas fazendas
    properties = relationship(
        "Property", back_populates="owner", cascade="all, delete-orphan"
    )

    # Configuração de Polimorfismo (Herança)
    type = Column(String(50))
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": type}


def _create_cpf_record(value: str):
    from app.shared.infrastructure.persistence.cpf import CPF

    return CPF(number=value)










































