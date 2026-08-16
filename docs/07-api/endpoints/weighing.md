---
title: "Endpoints de Weighing"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/weighing_router.py
---

# Endpoints de Weighing

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/weighings/` | Ausente | Registra pesagem |
| GET | `/weighings/animal/{animal_id}` | Ausente | Lista historico |
| PUT | `/weighings/{id}` | Ausente | Atualiza pesagem |
| DELETE | `/weighings/{id}` | Ausente | Exclui pesagem |

## Lacuna conhecida

Acesso por animal ou pesagem nao verifica propriedade do usuario.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
