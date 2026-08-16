---
title: "Exemplos de erros"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplos de erros

## Autenticação

```json
{"detail":"Invalid token."}
```

## Validação

```json
{
  "detail": [
    {"loc":["body","birth_date"],"msg":"Invalid date format","type":"value_error"}
  ]
}
```

## Recurso ausente ou de outro tenant

```json
{"detail":"Resource not found."}
```

A API deve usar 401 para autenticação, 404 para ausência/tenant, 409 para conflito, 422 para schema e 500 genérico. SQL, stack trace, host e credenciais nunca aparecem.
