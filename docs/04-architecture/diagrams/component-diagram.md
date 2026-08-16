---
title: "Component Diagram"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Diagrama de componentes do backend

```mermaid
flowchart LR
  ROUTER["Router + schemas"] --> AUTH["Auth dependencies"]
  ROUTER --> UC["Use case"]
  AUTH --> USERREPO["User/Property repositories"]
  UC --> SERVICE["Domain service"]
  UC --> REPO["Repository interface"]
  SERVICE --> REPO
  REPO -. implemented by .-> SQLREPO["SQLAlchemy repository"]
  SQLREPO --> MAPPER["Domain/ORM mapper"]
  MAPPER --> MODEL["ORM model"]
  MODEL --> DB[("Database")]
  ERR["Exception handlers"] --> ROUTER
```

O fluxo já aparece no módulo de animais. Lotes, áreas, pesagens e reprodução ainda usam serviços estáticos e devem migrar incrementalmente.
