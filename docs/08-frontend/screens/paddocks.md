---
title: "Tela: Paddocks"
type: reference
status: planned
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Tela: Paddocks

## Objetivo e estado

Tela de piquetes planejada; depende de pastagem da mesma propriedade.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
