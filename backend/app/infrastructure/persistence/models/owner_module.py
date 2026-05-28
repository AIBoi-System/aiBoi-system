from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.domain.enums.module.system_module import SystemModule
from app.infrastructure.database.connection import Base


class OwnerModule(Base):
    __tablename__ = "owner_modules"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id_user"), nullable=False, index=True)
    module_name = Column(Enum(SystemModule), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    owner = relationship("User")
