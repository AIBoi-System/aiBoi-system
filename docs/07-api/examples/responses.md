---
title: "Exemplos de respostas"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplos de respostas

## Token

```json
{"access_token":"<redacted>","token_type":"bearer","role":"owner"}
```

## Coleção

O contrato atual retorna lista JSON simples. O alvo futuro adiciona paginação.

```json
[
  {
    "id_animal": 10,
    "identification_number": 1001,
    "property_id": 42
  }
]
```

## Exclusão

Resposta `204 No Content`, sem body. Schemas reais devem ser confirmados no OpenAPI e não podem incluir hash de senha, token de recuperação ou detalhes internos.
