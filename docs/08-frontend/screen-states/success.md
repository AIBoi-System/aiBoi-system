---
title: "Estado de tela: Success"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Estado de tela: Success

## Comportamento

Confirmar resultado persistido, impedir repetição acidental e oferecer próximo passo claro. Sucesso não é exibido antes da confirmação da API.

## Aceite

- Estado semanticamente diferente de loading, vazio e erro.
- Texto curto, específico e legível em tela pequena.
- Ação disponível somente quando puder produzir resultado.
- Layout não muda de tamanho de forma incoerente.
- Widget test cobre renderização e ação principal.
