---
title: "ADR-006: Feature-first no Flutter"
type: governance
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# ADR-006: Feature-first no Flutter

- Estado: Aceita

## Contexto

Organizar todo o aplicativo apenas por tipo técnico espalharia os arquivos de uma jornada e dificultaria evolução paralela.

## Decisão

Organizar código principal por feature. Cada feature pode conter data, domain e presentation. Elementos realmente transversais permanecem em core; inicialização e tema ficam em app/core.

## Regras

Uma feature não importa implementação interna de outra. Compartilhamento frequente e estável pode migrar para core. Widgets de uma única jornada permanecem na feature. Repositories concretos pertencem a data; contratos pertencem a domain.

## Consequências

A navegação e DI conectam features sem eliminar seus limites. Revisões devem impedir core de se tornar depósito genérico.
