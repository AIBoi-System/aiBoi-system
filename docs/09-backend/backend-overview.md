---
title: "Visao do backend"
type: explanation
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Visao do backend

API Python 3.10+ com FastAPI, Pydantic 2, SQLAlchemy 2 e Uvicorn.

## Entrada

`app/main.py` cria a aplicacao, registra handlers, routers, CORS e headers. A criacao de tabelas com `create_all` e provisoria e deve ser substituida por migracoes.

## Fluxo alvo

`Router -> Use case -> Domain -> Repository interface -> SQLAlchemy repository`.

## Configuracao

Banco, JWT, CORS, e-mail e ambiente devem vir de configuracao validada. Nao sao permitidos defaults inseguros para producao.

## Estado

Animais seguem o fluxo alvo. Outros modulos ainda usam services estaticos e modelos ORM diretamente. A migracao deve ser incremental e acompanhada de testes.
