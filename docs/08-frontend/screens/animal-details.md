---
title: "Tela: Animal Details"
type: reference
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Tela: Animal Details

## Objetivo e estado

Resumo cadastral e futuro histórico de pesagem, sanidade, reprodução e movimentações do animal.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
