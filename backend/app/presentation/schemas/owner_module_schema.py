from pydantic import BaseModel

from app.enums.module.system_module import SystemModule


class OwnerModuleCreate(BaseModel):
    owner_id: int
    module_name: SystemModule
    is_active: bool = True


class OwnerModuleResponse(OwnerModuleCreate):
    id: int

    class Config:
        from_attributes = True









































