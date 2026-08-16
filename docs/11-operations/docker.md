---
title: "Docker"
type: reference
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Docker

## Objetivo

Construção e execução da imagem backend.

## Estado atual

A imagem `agrofence-api:local` é construída a partir de `backend/Dockerfile`.
Ela usa `python:3.11-slim`, instala dependências sem cache e executa com usuário
sem privilégios. O contexto de build exclui `.env`, ambientes virtuais, testes e
caches por `backend/.dockerignore`.

## Regras

- A imagem não contém credenciais, migrations aplicadas nem banco de dados.
- A API é exposta apenas pelo Compose, em `127.0.0.1:8000`.
- O banco local é externo ao contêiner e continua sendo autoridade dos dados.
- Alterações de schema são feitas exclusivamente por Alembic.

## Referências

- [Environment Setup](environment-setup.md)
- [Secrets Management](../05-security/secrets-management.md)
- [Api Unavailable](runbooks/api-unavailable.md)
