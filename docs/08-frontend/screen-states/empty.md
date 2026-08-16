---
title: "Estado de tela: Empty"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Estado de tela: Empty

## Comportamento

Explicar qual coleção está vazia e oferecer a ação primária apropriada, como cadastrar animal. Não apresentar vazio quando ocorreu erro ou falta de permissão.

## Aceite

- Estado semanticamente diferente de loading, vazio e erro.
- Texto curto, específico e legível em tela pequena.
- Ação disponível somente quando puder produzir resultado.
- Layout não muda de tamanho de forma incoerente.
- Widget test cobre renderização e ação principal.
