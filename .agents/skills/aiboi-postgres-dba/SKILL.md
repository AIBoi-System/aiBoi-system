---
name: aiboi-postgres-dba
description: Migra, configura, revisa e opera a persistência PostgreSQL/Supabase do AiBoi com SQLAlchemy e Alembic. Use ao trocar MySQL por PostgreSQL, alterar modelos ou migrations, diagnosticar conexão/pool, revisar índices e constraints, aplicar RLS, transferir dados, executar advisors ou validar isolamento por propriedade.
---

# AiBoi PostgreSQL DBA

Conduzir mudanças de banco com evidência, rollback e isolamento multi-tenant.
Tratar o banco remoto como dado real: inspecionar antes de modificar.

## Contexto obrigatório

- `backend/app/shared/infrastructure/database/connection.py`
- `backend/app/infrastructure/persistence/models/__init__.py`
- `backend/alembic/`
- `docs/06-database/`
- `docs/05-security/tenant-isolation.md`
- [Checklist de migração](references/migration-checklist.md)

Para trabalho Supabase, carregar também as skills `supabase`,
`supabase-postgres-best-practices` e `tenant-isolation`.

## Fluxo obrigatório

1. Classificar a operação como leitura, mudança reversível ou mudança destrutiva.
2. Inventariar schema, versão, tamanho, extensões, migrations e advisors.
3. Comparar o banco com `Base.metadata` e com a migration vigente.
4. Criar migration pequena, revisável e idempotente quando aplicável.
5. Validar upgrade em banco vazio e em cópia representativa.
6. Validar downgrade ou documentar restauração quando downgrade for inseguro.
7. Testar constraints, transações, enums, timezone e isolamento por propriedade.
8. Executar advisors e revisar planos das consultas críticas.
9. Aplicar primeiro em branch/staging; produção exige backup e janela aprovada.
10. Atualizar documentação e registrar comandos/resultados sem segredos.

## Conexões

- Usar URL direta para migrations, `pg_dump`, `pg_restore` e administração.
- Usar Supavisor em modo de sessão para backend persistente sem IPv6.
- Usar modo de transação somente para workloads serverless.
- Manter credenciais somente em variáveis de ambiente ou secret manager.
- Nunca imprimir URL completa, senha, token, service role ou conteúdo de `.env`.

## SQLAlchemy e Alembic

- Usar `postgresql+psycopg://` com psycopg 3.
- Manter `pool_pre_ping`; dimensionar pools por ambiente.
- Não executar `Base.metadata.create_all` no startup da API.
- Não editar migration já aplicada; criar uma nova revisão.
- Nomear enums explicitamente e revisar criação/remoção no PostgreSQL.
- Preferir `Numeric` para dinheiro e `JSONB` quando houver consulta/indexação.
- Criar índices compostos iniciando por `property_id` em consultas multi-tenant.
- Aplicar unicidade do animal por `(property_id, identification_number)`.
- Garantir rollback da sessão em qualquer falha de escrita.

## Supabase e RLS

- Usar MCP `search_docs` antes de depender de comportamento recente.
- Inventariar tabelas antes de aplicar qualquer migration.
- Usar `apply_migration` apenas para migration final revisada no banco remoto.
- Executar advisors após alterações de schema ou políticas.
- Habilitar RLS em toda tabela exposta pela Data API.
- Não considerar `TO authenticated` autorização suficiente; incluir ownership.
- Não usar `user_metadata` para autorização.
- Não expor `service_role` ao Flutter.
- Manter filtro ORM por propriedade mesmo quando RLS existir.

## Migração MySQL para PostgreSQL

1. Congelar mudanças de schema.
2. Fazer backup verificável do MySQL.
3. Mapear tipos, enums, FKs, índices, defaults e collations.
4. Aplicar schema vazio via Alembic no PostgreSQL.
5. Migrar dados preservando IDs e ordem das FKs.
6. Reposicionar sequences com `setval`.
7. Comparar contagens, nulos, somas e amostras por tabela.
8. Executar testes de API e cross-tenant contra PostgreSQL.
9. Fazer cutover somente após ensaio e plano de retorno.
10. Manter MySQL somente leitura durante a janela de retorno.

## Aprovação obrigatória

- DROP/TRUNCATE, exclusão física ou downgrade destrutivo.
- Aplicação em produção ou alteração de RLS existente.
- Renomear/remover coluna, tabela ou enum usado.
- Importar dados no projeto remoto.
- Alterar estratégia de tenant ou autenticação.

## Evidência de conclusão

- revisão Alembic identificada;
- upgrade validado em banco vazio;
- teste PostgreSQL e suíte principal verdes;
- contagens/checksums registrados na migração de dados;
- advisors sem achado bloqueador;
- backup e rollback documentados;
- nenhum segredo em código, log ou documentação.
