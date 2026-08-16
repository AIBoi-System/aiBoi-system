---
title: "Design system: Typography"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Design system: Typography

## Especificação

Poppins é usada em títulos e cabeçalhos. Roboto é usada no corpo, labels e
controles, com arquivos locais versionados para manter a mesma métrica no Web e
no mobile. Labels usam 14/500, botões 16/600, texto de corpo 16/400 e cabeçalhos
de etapas 20/600. Títulos devem respeitar hierarquia e não escalar pela largura
da viewport.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
