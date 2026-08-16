---
title: "Endpoints de Animals"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/animals_router.py
---

# Endpoints de Animals

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/animals/?property_id={id}` | JWT e propriedade | Cria animal |
| GET | `/animals/?property_id={id}` | JWT e propriedade | Lista animais |
| GET | `/animals/{animal_id}?property_id={id}` | JWT e propriedade | Consulta animal |
| PUT | `/animals/{animal_id}?property_id={id}` | JWT e propriedade | Atualiza animal |
| DELETE | `/animals/{animal_id}?property_id={id}` | JWT e propriedade | Exclui animal |

## Lacuna conhecida

A implementacao filtra por animal e propriedade, mas a suite de API ainda usa o contrato anterior sem autenticacao/property_id.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
