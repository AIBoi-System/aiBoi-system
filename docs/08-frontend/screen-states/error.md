---
title: "Estado de tela: Error"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Estado de tela: Error

## Comportamento

Informar o que não foi concluído e oferecer tentar novamente quando seguro. Mensagem técnica e stack trace não aparecem.

## Aceite

- Estado semanticamente diferente de loading, vazio e erro.
- Texto curto, específico e legível em tela pequena.
- Ação disponível somente quando puder produzir resultado.
- Layout não muda de tamanho de forma incoerente.
- Widget test cobre renderização e ação principal.
