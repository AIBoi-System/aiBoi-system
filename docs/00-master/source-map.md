---
title: "Mapa de fontes"
type: reference
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Mapa de fontes

| Fonte | Uso | Precedencia |
|---|---|---|
| [`source-original-agrofence-v1.2.md`](source-original-agrofence-v1.2.md) recebido em 2026-07-16 | Requisitos, casos de uso e modelos historicos | Historica |
| `docs/product/` e `docs/mvp/` | Refinamento recente de produto e MVP | Alta para escopo |
| `backend/app` | Comportamento executavel da API e persistencia | Alta para estado atual |
| `frontend/lib` | Fluxos e telas executaveis | Alta para estado atual |
| `backend/tests` | Evidencia automatizada | Alta quando o teste passa |
| `docs/00-master` a `docs/18-archive` | Documentacao normalizada | Oficial |

Quando fontes divergem, registrar a diferenca em `known-inconsistencies.md` em vez de ocultar a divergencia.
