---
title: "Arquitetura atual"
type: explanation
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Arquitetura atual

## Visao

O repositorio e um monorepo com `backend` FastAPI/SQLAlchemy e `frontend` Flutter. O backend declara Clean Architecture e DDD, mas esta em migracao.

## Backend

- `presentation`: routers FastAPI e schemas Pydantic.
- `application`: casos de uso novos e servicos estaticos legados.
- `domain`: entidades, objetos de valor e portas, mais maduros em animais e sanidade.
- `infrastructure`: modelos SQLAlchemy, repositorios, autenticacao e e-mail.
- `shared`: componentes transversais e persistencia ainda acoplada a modulos.

O modulo de animais percorre router, use case, dominio e repository. Lotes,
pastagens, piquetes, pesagens e partes de reproducao ainda acessam ORM por
servicos. O dashboard de propriedade e orquestrado pela camada application;
routers nao devem adicionar consultas SQL diretas.

Guardrails executados pelo Pytest congelam as excecoes legadas e impedem novas
dependencias invertidas. A especificacao esta em
[Dependency Rules](dependency-rules.md).

## Frontend

Organizacao feature-first com `presentation`, `domain` e `data`. Cubits controlam login e cadastro; outras telas usam estado local ou acesso direto a repositories.

## Riscos

Acoplamento legado, transacoes por repository, falta de unidade de trabalho e
fluxos de autenticacao ainda concentrados no router. As migrations PostgreSQL
sao versionadas por Alembic; novos schemas nao devem usar `create_all` no
startup.
