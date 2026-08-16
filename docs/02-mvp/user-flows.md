---
title: "User Flows"
type: reference
status: active
owner: product
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# User Flows

## Objetivo

Sequências ponta a ponta para cadastro, propriedade, animais e manejo.

## Especificação

Todo fluxo documenta gatilho, pré-condições, passos, decisões, estados de erro, resultado e dados persistidos.

## Estado no AiBoi

Esta página define a direção vigente e deve ser confirmada contra código, testes e decisões aprovadas antes de cada release.

## Cadastro de usuário

1. Usuário escolhe cadastro por e-mail ou Google.
2. No fluxo por e-mail, informa o endereço de e-mail; a API envia o OTP e o
   usuário confirma o código. No fluxo Google, a API exige a claim verificada.
3. Usuário informa telefone brasileiro e confirma o OTP telefônico.
4. Usuário informa nome, CPF e endereço brasileiro válidos.
5. Somente então a interface habilita a definição da senha.
6. API revalida todas as confirmações, persiste usuário/CPF/endereço em uma única
   transação e retorna access/refresh tokens.
7. A partir desse ponto, qualquer criação ou alteração exige sessão autenticada e
   autorização do recurso/propriedade.

Falhas não revelam se e-mail, telefone ou conta existem; códigos expirados,
reutilizados ou incorretos são recusados.

## Login

1. Usuário escolhe e-mail ou Google na tela de acesso.
2. E-mail abre o formulário de e-mail/senha; Google usa o provedor configurado.
3. API valida identidade, usuário ativo e sessão, retornando access/refresh
   tokens somente após sucesso.

## Regras

- Não ampliar o MVP sem decisão explícita.
- Todo item incluído precisa de critério de aceite e teste.
- Segurança multi-tenant é requisito bloqueador.

## Critérios de aceite documental

- O conceito possui limites e termos inequívocos.
- Estado atual e estado desejado estão separados.
- Exceções e cenários de falha estão registrados.
- Requisitos, testes e fontes relacionadas podem ser localizados.

## Referências

- [Mvp Scope](mvp-scope.md)
- [Business Rules](business-rules.md)
- [Test Scenarios](test-scenarios.md)
