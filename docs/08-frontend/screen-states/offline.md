---
title: "Estado de tela: Offline"
type: reference
status: planned
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Estado de tela: Offline

## Comportamento

Estado planejado. Diferenciar ausência de internet de indisponibilidade da API; não prometer salvamento offline enquanto sincronização não existir.

## Aceite

- Estado semanticamente diferente de loading, vazio e erro.
- Texto curto, específico e legível em tela pequena.
- Ação disponível somente quando puder produzir resultado.
- Layout não muda de tamanho de forma incoerente.
- Widget test cobre renderização e ação principal.
