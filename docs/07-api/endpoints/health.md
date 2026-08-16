---
title: "Endpoints de Health"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/health_router.py
---

# Endpoints de Health

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/health/` | Ausente | Cria registro sanitario |
| GET | `/health/` | Ausente | Lista registros |
| GET | `/health/{health_id}` | Ausente | Consulta registro |
| PUT | `/health/{health_id}` | Ausente | Atualiza registro |
| DELETE | `/health/{health_id}` | Ausente | Exclui registro |

## Lacuna conhecida

Repository consulta por ID global e precisa receber property_id em todas as operacoes.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
