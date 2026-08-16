---
title: "Sequence Diagrams"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Diagramas de sequência

## Consultar animal

```mermaid
sequenceDiagram
  actor U as Usuário
  participant F as Flutter
  participant A as FastAPI
  participant P as PropertyService
  participant C as GetAnimalUseCase
  participant R as AnimalRepository
  U->>F: Abre detalhe
  F->>A: GET animal + property_id + JWT
  A->>A: Valida JWT
  A->>P: Verifica propriedade do usuário
  P-->>A: Acesso válido
  A->>C: execute(animal_id, property_id)
  C->>R: get_by_id(animal_id, property_id)
  R-->>C: Animal ou vazio
  C-->>A: Animal
  A-->>F: 200 AnimalResponse
```

## Recuperar senha

```mermaid
sequenceDiagram
  actor U as Usuário
  participant A as API
  participant D as Database
  participant E as E-mail
  U->>A: Solicita recuperação
  A->>D: Localiza conta sem revelar resultado
  A->>D: Persiste hash do token e expiração
  A->>E: Envia token bruto
  A-->>U: Resposta genérica
  U->>A: Token + nova senha
  A->>D: Valida hash, expiração e uso
  A->>D: Atualiza hash de senha e invalida token
```

O segundo fluxo é o alvo seguro; o código atual ainda retorna o token bruto na primeira resposta.
