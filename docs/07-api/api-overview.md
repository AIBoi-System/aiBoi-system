---
title: "Visao da API"
type: explanation
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Visao da API

API REST em FastAPI, exposta atualmente sem prefixo global de versao apesar do pacote `v1`.

## Grupos implementados

`auth`, `users`, `owners`, `owner-modules`, `properties`, `animals`, `batches`, `pastures`, `paddocks`, `weighings`, `health`, `reproductions` e enderecos.

## Convencoes alvo

- JSON UTF-8 e datas ISO 8601.
- Bearer JWT para rotas privadas.
- `property_id` validado contra o usuario autenticado.
- 201 para criacao, 204 para exclusao, 400 para regra invalida, 401 para autenticacao, 404 para ausencia ou tenant diferente, 409 para conflito e 422 para schema.
- Lista paginada em contratos novos.
- OpenAPI como contrato executavel, complementado pela documentacao por endpoint.

## Compatibilidade

Mudanca incompatível exige prefixo de versao, changelog e janela de migracao para o aplicativo.
