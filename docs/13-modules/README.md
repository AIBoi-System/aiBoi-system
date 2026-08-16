---
title: "Modulos do AiBoi"
type: governance
status: partial
owner: domain
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Modulos do AiBoi

A documentacao modular agrupa regra de negocio, contrato, dados e testes por capacidade. O estado aqui descreve o repositorio em 2026-07-16.

| Modulo | Estado |
|---|---|
| [Identity](identity/README.md) | Parcial |
| [Owners](owners/README.md) | Parcial |
| [Properties](properties/README.md) | Parcial |
| [Animals](animals/README.md) | Implementado com lacunas de teste |
| [Batches](batches/README.md) | Parcial |
| [Pastures](pastures/README.md) | Parcial |
| [Paddocks](paddocks/README.md) | Parcial |
| [Weighing](weighing/README.md) | Parcial |
| [Health](health/README.md) | Parcial |
| [Reproduction](reproduction/README.md) | Parcial |
| [Activities](activities/README.md) | Planejado |
| [Alerts](alerts/README.md) | Planejado |
| [Dashboard](dashboard/README.md) | Planejado |
| [Reports](reports/README.md) | Planejado |

## Regra transversal

Todo modulo operacional deve receber o contexto de propriedade validado no backend e filtrar consultas, alteracoes e exclusoes por esse contexto.
