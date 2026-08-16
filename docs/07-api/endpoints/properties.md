---
title: "Endpoints de Properties"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/properties_router.py
---

# Endpoints de Properties

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/properties/` | JWT | Cria propriedade para o usuario atual |
| GET | `/properties/` | JWT | Lista propriedades proprias |
| GET | `/properties/{property_id}` | JWT e ownership | Consulta propriedade propria |
| PUT | `/properties/{property_id}` | Ausente | Atualiza propriedade |
| DELETE | `/properties/{property_id}` | Ausente | Exclui propriedade |

## Lacuna conhecida

PUT e DELETE nao validam usuario atual nem ownership e devem ser bloqueados antes de uso.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
