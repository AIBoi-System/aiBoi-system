---
title: "Tela: Activities"
type: reference
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Activities

## Objetivo e estado

Catálogo Flutter organizado nos grupos Manejo, Reprodução, Sanidade, Pesagem,
Financeiro, Pastagem e Cercas Virtuais. Cada grupo usa rolagem horizontal e
mantém quatro ações visíveis no viewport de referência.

Destinos com API pronta preservam a navegação para animais, saúde, reprodução,
pesagem e pastagens. Ações sem endpoint continuam identificadas por uma tela de
evolução e não simulam gravação bem-sucedida.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
