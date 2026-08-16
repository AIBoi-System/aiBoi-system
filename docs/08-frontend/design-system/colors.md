---
title: "Design system: Colors"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Design system: Colors

## Especificação

Paleta atual: `primaryGreen/primaryButton #14473D`, hover `#1C6153`, verde
secundário `#376E45`, progresso `#81AF0F`, fundo `#F8FAF8`, fundo verde suave
`#EBF3E5`, texto primário `#27252E`, texto secundário `#605D67`, borda
`#C7C5CC`, desabilitado `#96ABA6` e branco para cards.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
