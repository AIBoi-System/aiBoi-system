---
title: "Design system: Navigation Components"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Design system: Navigation Components

## Especificação

Navegação deve indicar destino atual, preservar retorno e usar ícones familiares. Rotas de cadastro mantêm o mesmo RegistrationCubit durante as etapas.

## Regras de uso

- Usar tokens e componentes compartilhados antes de criar variação local.
- Preservar contraste, semântica, foco e área de toque.
- Tratar estados normal, foco, pressionado, desabilitado e erro quando aplicável.
- Validar em 320 px e em viewport ampla sem sobreposição.

## Evidência

A referência executável está em `frontend/lib/core/theme` e `frontend/lib/core/widgets`. Mudanças visuais exigem widget test ou verificação visual.
