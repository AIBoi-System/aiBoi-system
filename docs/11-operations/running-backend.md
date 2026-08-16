---
title: "Running Backend"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Running Backend

## Objetivo

Comandos, variáveis e verificações para iniciar a API.

## Especificação

No diretório backend, instalar requirements e executar uvicorn app.main:app --reload. Configurar banco e JWT antes. Não usar /test-db em produção enquanto ele retornar detalhes internos.

## Estado atual

Norma vigente para novas alterações e releases.

## Regras

- Produção não usa segredo versionado.
- Mudança possui rollback e verificação.
- Operação é repetível e observável.
- Backup só é válido após teste de restauração.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Environment Setup](environment-setup.md)
- [Secrets Management](../05-security/secrets-management.md)
- [Api Unavailable](runbooks/api-unavailable.md)
