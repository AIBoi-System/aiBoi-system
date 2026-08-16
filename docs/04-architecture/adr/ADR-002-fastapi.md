---
title: "ADR-002: FastAPI"
type: governance
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# ADR-002: FastAPI

- Estado: Aceita

## Contexto

A API precisa de validação tipada, OpenAPI, injeção de dependência e bom suporte ao ecossistema Python/SQLAlchemy.

## Decisão

Usar FastAPI na camada de apresentação, Pydantic para contratos e Uvicorn como servidor ASGI. Routers validam HTTP e delegam a casos de uso; não concentram regra de negócio ou consultas.

## Alternativas

Django REST Framework ofereceria ecossistema integrado, mas imporia estrutura e ORM diferentes. Flask teria menor convenção e exigiria compor validação e OpenAPI.

## Consequências

Schemas e type hints tornam o contrato executável. Dependencies devem construir autenticação, session e casos de uso. Código de domínio permanece independente do FastAPI. Atualizações de FastAPI, Starlette, Pydantic e HTTPX precisam ser testadas em conjunto.
