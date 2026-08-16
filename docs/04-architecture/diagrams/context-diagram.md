---
title: "Context Diagram"
type: explanation
status: partial
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Diagrama de contexto

```mermaid
flowchart LR
  P["Pecuarista"] --> APP["Aplicativo Flutter"]
  C["Equipe de campo"] --> APP
  T["Técnico autorizado"] --> APP
  APP --> API["API AiBoi"]
  API --> DB["Banco relacional"]
  API --> MAIL["Serviço de e-mail"]
  API -. futuro .-> PAY["Gateway de pagamento"]
  APP -. futuro .-> SCALE["Balança Bluetooth"]
```

O aplicativo é o canal principal. API é a autoridade para autenticação, regras e tenant. E-mail atende verificação e recuperação. Pagamento e balança são futuros.
