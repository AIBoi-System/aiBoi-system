---
title: "Exemplos de requisições"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplos de requisições

## Login

```http
POST /auth/login
Content-Type: application/json

{"email":"usuario@exemplo.com","password":"frase-secreta"}
```

## Listar animais

```http
GET /animals/?property_id=42
Authorization: Bearer <token>
Accept: application/json
```

## Criar animal

```http
POST /animals/?property_id=42
Authorization: Bearer <token>
Content-Type: application/json

{
  "identification_number": 1001,
  "sex": "M",
  "animal_size": "MEDIUM_SIZE",
  "animal_life_status": "ACTIVE",
  "animal_category": "BULL",
  "birth_date": "2024-01-15",
  "origin": "PURCHASE"
}
```

Valores de enum devem ser confirmados no OpenAPI da versão executada. Nunca usar token ou dado pessoal real em documentação.
