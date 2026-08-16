---
title: "Navigation"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Navigation

## Objetivo

Rotas, argumentos, redirecionamento de autenticação e retorno entre fluxos.

## Especificação

O documento especifica responsabilidades, limites, fluxo esperado, estados de falha e evidências necessárias para navigation.

## Estado atual

O shell autenticado possui rotas distintas para Home (`/home`), propriedades
(`/properties`), atividades (`/activities`), configurações (`/settings`) e
perfil (`/profile`). O menu lateral compartilhado permite transitar entre esses
destinos e encerra a sessão pelo repositório de autenticação.

O fluxo de propriedade mantém `/property/create` e `/property/success`. Após o
sucesso, “Entrar na Propriedade” seleciona a propriedade no Home e “Ver minhas
Propriedades” retorna à lista.

## Regras

- Toda tela assíncrona trata loading, vazio, erro e sucesso.
- Validação visual não substitui backend.
- Layouts funcionam em 320 px sem sobreposição.
- Autorização não depende de esconder controles.
- Rotas operacionais continuam protegidas pelo token e pelo ownership validado
  na API; abrir uma URL diretamente não concede acesso aos dados.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Frontend Overview](frontend-overview.md)
- [Authorization](../05-security/authorization.md)
- [Frontend Tests](../10-quality/frontend-tests.md)
