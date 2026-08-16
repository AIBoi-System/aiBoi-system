---
title: "Design system: Buttons"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Design system: Buttons

## Especificação

`PrimaryButton` ocupa a largura disponível, possui 60 px de altura, raio de
12 px e texto Roboto 16/600. O estado normal usa `#14473D`, hover usa `#1C6153`
e o estado desabilitado usa `#96ABA6`. Loading mantém as mesmas dimensões e
exibe indicador de 20 px. A ação deve ser idempotente contra toques repetidos.

Botões sociais possuem 60 px, raio de 12 px, borda `#C7C5CC`, ícone de 20 px e
texto Roboto 14/500.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
