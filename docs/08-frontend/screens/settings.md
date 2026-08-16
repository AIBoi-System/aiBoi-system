---
title: "Tela: Configurações"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Configurações

## Objetivo e estado

Centraliza preferências de notificações, aparência, idioma, fazendas e conta.
Os controles locais já apresentam seus estados de interação; persistência de
preferências depende de contrato futuro da API e não é afirmada pela interface.

## Segurança e dados

Alteração de senha e PIN deve encaminhar para fluxo autenticado específico. A
tela não recebe nem mantém senha, token ou CPF em controles visuais.

## Responsividade e testes

Implementação baseada no frame Figma `3303:680`, com grupos em cartões,
switches acessíveis e navegação para propriedades.
