---
title: "Tela: Onboarding"
type: reference
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Tela: Onboarding

## Objetivo e estado

Cadastro em etapas: escolha do método, e-mail, verificação de e-mail, telefone,
verificação de telefone, CPF/endereço, senha e conclusão. O
`RegistrationCubit` preserva o rascunho entre as telas. O cabeçalho mantém o
contador funcional de seis etapas mesmo quando a referência visual apresenta
um exemplo reduzido de três etapas.

## Estados obrigatórios

Loading, conteúdo, vazio quando aplicável, validação, erro recuperável, permissão negada e sucesso confirmado pela API.

## Segurança e dados

A tela não concede autorização. Recursos operacionais usam a propriedade ativa e o backend valida ownership. Não exibir token, senha, CPF completo ou erro interno.

## Responsividade e testes

Conteúdo deve funcionar em 320 px, com teclado aberto e texto ampliado. Testar navegação, ação principal, erro da API e ausência de dados.
