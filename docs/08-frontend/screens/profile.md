---
title: "Tela: Profile"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Tela: Profile

## Objetivo e estado

Perfil implementado em quatro abas: Minha Conta, Notificações, Assinatura e
Configurações. Minha Conta oferece acesso a dados pessoais, propriedades,
segurança e logout; as demais abas apresentam alertas, plano e preferências.

Dados financeiros e pessoais mostrados no frame são demonstrações de interface
até que seus contratos de API sejam implementados. Alterações sensíveis devem
continuar exigindo sessão válida e confirmação no backend.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
