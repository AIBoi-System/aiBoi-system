---
title: "Endpoints de Batches"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/batches_router.py
---

# Endpoints de Batches

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/batches/` | Ausente | Cria lote |
| GET | `/batches/` | Ausente | Lista lotes globalmente |
| GET | `/batches/{batch_id}` | Ausente | Consulta por ID global |
| PUT | `/batches/{batch_id}` | Ausente | Atualiza por ID global |
| DELETE | `/batches/{batch_id}` | Ausente | Exclui por ID global |

## Lacuna conhecida

O schema/servico nao injeta property_id corretamente e as consultas nao possuem isolamento.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
