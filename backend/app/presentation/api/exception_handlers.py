from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.shared.domain.exceptions import (
    DomainException,
    DuplicateEntityError,
    EntityNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EntityNotFoundError)
    async def not_found_handler(_request: Request, exc: EntityNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(DuplicateEntityError)
    async def duplicate_handler(_request: Request, exc: DuplicateEntityError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(DomainException)
    async def domain_handler(_request: Request, exc: DomainException):
        return JSONResponse(status_code=400, content={"detail": str(exc)})









































