---
title: "Tabelas"
type: reference
status: active
owner: data
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Tabelas

O inventario abaixo e derivado dos modelos SQLAlchemy atuais.

| Grupo | Tabelas principais |
|---|---|
| Identidade | users, cpfs, owners, addresses, email_verification_codes, phone_verification_codes, password_reset_tokens, auth_sessions |
| Propriedade | properties, owner_modules |
| Inventario | animals, batches, animal_events, animal_movements, batch_movements, death_records |
| Area | pastures, paddocks |
| Manejo | weighings, health_records |
| Reproducao | reproductions, protocols, steps, step_executions |

## Regras

Chaves estrangeiras devem preservar consistencia. Tabelas operacionais precisam de `property_id` direto ou de uma cadeia de relacionamento impossivel de atravessar entre tenants. A restricao de identificacao animal deve ser composta por propriedade; unicidade global nao corresponde a RN003.

`cpfs` usa `user_id` simultaneamente como PK/FK, garantindo relação one-to-one e
remoção em cascata. `auth_sessions` guarda somente o hash do refresh token e dados
de expiração/revogação. A migration vigente é `7b9d2c4e6f81`.
