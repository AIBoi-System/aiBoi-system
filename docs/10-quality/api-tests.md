---
title: "Api Tests"
type: reference
status: active
owner: quality
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Api Tests

## Objetivo

Testes HTTP de contrato, autenticação, tenant, validação e erro.

## Especificação

Cada recurso de propriedade testa usuário A contra recurso de B em GET, list, update e delete. Testes atuais de animais precisam autenticar e fornecer property_id.

## Estado atual

Norma vigente para novas alterações e releases.

## Regras

- Teste demonstra comportamento, não implementação interna.
- Defeito corrigido recebe regressão.
- Tenant exige teste cruzado.
- Suite instável bloqueia release.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Testing Strategy](testing-strategy.md)
- [Test Scenarios](../02-mvp/test-scenarios.md)
- [Traceability Matrix](traceability-matrix.md)
