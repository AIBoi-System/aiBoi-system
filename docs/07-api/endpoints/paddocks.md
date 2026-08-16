---
title: "Endpoints de Paddocks"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/paddocks_router.py
---

# Endpoints de Paddocks

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/paddocks/` | Ausente | Cria piquete |
| GET | `/paddocks/` | Ausente | Lista com filtros opcionais |
| GET | `/paddocks/{paddock_id}` | Ausente | Consulta por ID |
| PUT | `/paddocks/{paddock_id}` | Ausente | Atualiza |
| DELETE | `/paddocks/{paddock_id}` | Ausente | Exclui |

## Lacuna conhecida

Deve validar a cadeia piquete, pastagem e propriedade em todas as operacoes.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
