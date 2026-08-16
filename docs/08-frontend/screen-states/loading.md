---
title: "Estado de tela: Loading"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Estado de tela: Loading

## Comportamento

Exibir progresso sem apagar contexto ou permitir envio duplicado. Em listas, preservar dimensões; em botões, manter largura e substituir conteúdo de forma estável.

## Aceite

- Estado semanticamente diferente de loading, vazio e erro.
- Texto curto, específico e legível em tela pequena.
- Ação disponível somente quando puder produzir resultado.
- Layout não muda de tamanho de forma incoerente.
- Widget test cobre renderização e ação principal.
