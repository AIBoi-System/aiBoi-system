---
title: "State Management"
type: reference
status: partial
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# State Management

## Objetivo

Uso de Cubit/Bloc, estados imutáveis e efeitos de interface.

## Especificação

Estados de Cubit devem ser imutáveis e representar initial, loading, success e failure. Efeitos de navegação ou snackbar não ficam ocultos em build sem controle. O projeto usa Cubits em login e cadastro, mas outras features ainda precisam uniformização.

## Estado atual

Parcial. Há componentes no projeto, porém faltam uniformidade e cobertura para afirmar conformidade completa.

## Regras

- Toda tela assíncrona trata loading, vazio, erro e sucesso.
- Validação visual não substitui backend.
- Layouts funcionam em 320 px sem sobreposição.
- Autorização não depende de esconder controles.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Frontend Overview](frontend-overview.md)
- [Authorization](../05-security/authorization.md)
- [Frontend Tests](../10-quality/frontend-tests.md)
