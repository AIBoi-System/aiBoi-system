---
title: "Configuracao do ambiente"
type: how-to
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Configuracao do ambiente

## Backend

1. Instalar Python compatível.
2. Criar ambiente virtual.
3. Instalar `backend/requirements.txt`.
4. Criar configuracao local a partir de `backend/.env.example`.
5. Definir chave JWT forte e URL de banco.
6. Executar a API pelo Uvicorn.

Em desenvolvimento e testes, o rate limiting pode usar memória local quando
`REDIS_URL` não estiver definida. Em `ENV=production`, configure uma `REDIS_URL`
alcançável antes do startup; a API deve recusar inicialização se o Redis não
responder, pois memória local não protege uma implantação com múltiplas instâncias.

## Frontend

1. Instalar Flutter compativel com o SDK do `pubspec.yaml`.
2. Executar `flutter pub get`.
3. Configurar o endpoint por ambiente.
4. Executar em emulador Android ou dispositivo.

## Docker

`docker compose up --build` inicia API e Mailpit. O Compose lê apenas
`backend/.env`, conecta ao PostgreSQL local por `host.docker.internal` e nunca
mantém credenciais no YAML versionado. Acesse a API em `127.0.0.1:8000` e o
Mailpit em `127.0.0.1:8025`.

## Verificacao

API raiz, OpenAPI, conexao de banco sem detalhes sensiveis, testes backend, `flutter analyze` e testes Flutter.
