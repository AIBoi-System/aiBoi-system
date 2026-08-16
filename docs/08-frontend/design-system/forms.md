---
title: "Design system: Forms"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Design system: Forms

## Especificação

Label fica fora do campo; hint não substitui label. `LabeledTextField` possui
altura mínima de 60 px, padding horizontal de 16 px, raio de 12 px, borda
`#C7C5CC`, foco verde e borda de erro. Backend continua autoridade final.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
