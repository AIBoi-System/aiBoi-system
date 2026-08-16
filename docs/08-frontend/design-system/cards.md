---
title: "Design system: Cards"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Design system: Cards

## Especificação

Cards representam itens repetidos ou ferramentas realmente delimitadas, não seções inteiras. Raio máximo preferencial 8, contraste e área de toque preservados.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
