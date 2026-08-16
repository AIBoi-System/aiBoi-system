---
title: "Endpoints de Owners"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
source_paths:
  - backend/app/presentation/api/v1/owner_router.py
---

# Endpoints de Owners

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/owners/` | Nao comprovada | Cria perfil de proprietario |
| POST | `/owners/upgrade/{id_user}` | Nao comprovada | Converte usuario em proprietario |
| GET | `/owners/` | Nao comprovada | Lista proprietarios |
| GET | `/owners/{id_user}` | Nao comprovada | Consulta proprietario |
| PUT | `/owners/{id_user}` | Nao comprovada | Atualiza proprietario |
| DELETE | `/owners/{id_user}` | Nao comprovada | Exclui proprietario |

## Lacuna conhecida

As rotas precisam de autorizacao administrativa ou autoconsulta explicita; listagem global nao deve ser publica.

## Regras de contrato

Rotas privadas exigem JWT, autorizacao e isolamento por propriedade. Testes devem cobrir token ausente, entrada invalida, recurso inexistente e tentativa entre tenants.
