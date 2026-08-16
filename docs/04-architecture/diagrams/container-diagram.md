---
title: "Container Diagram"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Diagrama de contêineres

```mermaid
flowchart TB
  subgraph Client["Flutter"]
    UI["Pages e widgets"] --> STATE["Cubits/estado"]
    STATE --> FREPO["Repository contracts"]
    FREPO --> HTTP["Datasources HTTP"]
  end
  HTTP --> REST["FastAPI REST"]
  subgraph Backend["Backend"]
    REST --> APP["Casos de uso"]
    APP --> DOM["Domínio"]
    APP --> PORT["Portas de repository"]
    PORT --> SQL["Repositories SQLAlchemy"]
    SQL --> ORM["Modelos ORM"]
  end
  ORM --> DB[("PostgreSQL / SQLite em testes rápidos")]
  APP --> EMAIL["Adapter de e-mail"]
```

Dependências apontam para o domínio. O estado atual ainda possui services legados que atravessam os limites mostrados.
