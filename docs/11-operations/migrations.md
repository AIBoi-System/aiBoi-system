---
title: "Migrations"
type: reference
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Migrations

## Objetivo

Execução operacional de upgrades e downgrades Alembic no PostgreSQL/Supabase.

## Especificação

1. Fazer backup e testar restauração.
2. Executar migration em branch/staging.
3. Rodar testes e advisors.
4. Revisar SQL e locks esperados.
5. Aplicar uma única vez com `python -m alembic -c alembic.ini upgrade head`.
6. Verificar versão, saúde da API e métricas.

## Estado atual

Alembic configurado e migration inicial validada offline. A aplicação no
PostgreSQL local e os testes de integração permanecem pendentes. Uma implantação
gerenciada futura exige inventário, backup e aprovação próprios.

## Regras

- Produção não usa segredo versionado.
- Mudança possui rollback e verificação.
- Operação é repetível e observável.
- Backup só é válido após teste de restauração.

## Transferência de uma origem legada

Não há transferência de dados ativa nesta etapa: o banco PostgreSQL local foi
inventariado vazio. Se uma origem legada for identificada posteriormente, a
transferência deve ser tratada em plano separado, com ferramenta oficialmente
suportada para a origem e o destino escolhidos.

Ordem operacional:

1. inventariar a origem e fazer backup verificável;
2. aplicar a migration Alembic em branch/staging vazia;
3. migrar dados preservando os IDs;
4. ajustar sequences PostgreSQL;
5. comparar contagens e invariantes por tabela;
6. executar suíte PostgreSQL e advisors;
7. ensaiar cutover e rollback;
8. somente então repetir em produção.

O MCP não substitui backup nem transferência controlada de dados. Não executar
importação remota antes de confirmar tamanho, origem, destino e janela.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Environment Setup](environment-setup.md)
- [Secrets Management](../05-security/secrets-management.md)
- [Api Unavailable](runbooks/api-unavailable.md)
