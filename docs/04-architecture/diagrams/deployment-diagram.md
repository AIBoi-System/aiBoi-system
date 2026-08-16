---
title: "Deployment Diagram"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Diagrama de implantação

```mermaid
flowchart LR
  PHONE["Android device"] -->|HTTPS| EDGE["TLS / reverse proxy"]
  WEB["Flutter Web, se homologado"] -->|HTTPS| EDGE
  EDGE --> API["Uvicorn + FastAPI container"]
  API -->|TLS| DB[("PostgreSQL")]
  API -->|HTTPS| MAIL["E-mail provider"]
  CI["GitHub Actions"] --> TEST["Tests and docs audit"]
  CI -. future release .-> API
```

Produção requer HTTPS, segredo externo ao repositório, banco não público, backup e observabilidade. O pipeline de implantação ainda é planejado.
