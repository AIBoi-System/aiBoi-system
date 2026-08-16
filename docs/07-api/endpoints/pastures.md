---
title: "Endpoints de Pastures"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/pastures_router.py
---

# Endpoints de Pastures

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/pastures/` | Ausente | Cria pastagem |
| GET | `/pastures/` | Ausente | Lista com filtro opcional |
| GET | `/pastures/{pasture_id}` | Ausente | Consulta por ID |
| PUT | `/pastures/{pasture_id}` | Ausente | Atualiza |
| DELETE | `/pastures/{pasture_id}` | Ausente | Exclui |

## Lacuna conhecida

Filtro opcional informado pelo cliente nao substitui validacao de propriedade.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
