---
title: "Tela: Home"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Home

## Objetivo e estado

Painel inicial da propriedade ativa, com seletor de fazenda, notificações,
carrossel de resumo, indicadores operacionais e saúde do rebanho. A seleção e o
cadastro de fazendas ficam na rota própria de propriedades.

O cabeçalho e o menu lateral são compartilhados com as demais telas
autenticadas. “Detalhes” preserva o acesso ao dashboard conectado à API.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
