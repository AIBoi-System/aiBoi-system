from fastapi import APIRouter

from app.presentation.api.v1 import (
    address_router,
    animal_router,
    auth_router,
    batch_router,
    health_router,
    owner_router,
    owner_module_router,
    paddock_router,
    pasture_router,
    property_router,
    reproduction_router,
    user_router,
    weighing_router,
)

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router.router)
api_v1_router.include_router(user_router.router)
api_v1_router.include_router(batch_router.router)
api_v1_router.include_router(property_router.router)
api_v1_router.include_router(reproduction_router.router)
api_v1_router.include_router(health_router.router)
api_v1_router.include_router(owner_router.router)
api_v1_router.include_router(owner_module_router.router)
api_v1_router.include_router(animal_router.router)
api_v1_router.include_router(weighing_router.router)
api_v1_router.include_router(
    address_router.router, prefix="/addresses", tags=["Endereços"]
)
api_v1_router.include_router(pasture_router.router)
api_v1_router.include_router(paddock_router.router)














































