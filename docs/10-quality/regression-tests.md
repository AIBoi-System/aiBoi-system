---
title: "Regression Tests"
type: reference
status: active
owner: quality
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Regression Tests

## Objetivo

Política de teste obrigatório para todo defeito corrigido.

## Especificação

O documento especifica responsabilidades, limites, fluxo esperado, estados de falha e evidências necessárias para regression tests.

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
