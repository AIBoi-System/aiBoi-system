---
title: "Design system: Spacing"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Design system: Spacing

## Especificação

Adotar múltiplos de 4 com passos preferenciais 4, 8, 12, 16, 24 e 32. Campos usam padding horizontal 16; espaçamento deve manter ritmo sem criar cards aninhados.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
