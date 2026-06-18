from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.shared.infrastructure.persistence.user import User
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus


class Owner(User):
    """
    Representa um Proprietário no sistema AiBoi.
    Herda atributos básicos de User e adiciona dados de assinatura e propriedades.
    """
    __tablename__ = "owners"

    # Chave primária que também é chave estrangeira para a tabela de usuários
    id_owner = Column(
        Integer, 
        ForeignKey("users.id_user"), 
        primary_key=True
    )
    
    # Status da assinatura (Usa o Enum fornecido)
    subscription_status = Column(
        Enum(OwnerSubscriptionStatus), 
        nullable=False,
        default=OwnerSubscriptionStatus.FREE
    )

    # Relacionamentos
    # Um proprietário pode ter várias fazendas/propriedades
    properties = relationship(
        "Property", 
        back_populates="owner", 
        cascade="all, delete-orphan"
    )

    # Configuração para Herança do SQLAlchemy
    __mapper_args__ = {
        "polymorphic_identity": "owner",
    }









































