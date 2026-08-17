# Checklist MySQL → Supabase PostgreSQL

## Antes

- [ ] Confirmar origem, destino e ambiente.
- [ ] Registrar versões de banco, ORM, Alembic e drivers.
- [ ] Medir tamanho e contagem por tabela.
- [ ] Exportar schema e dados da origem.
- [ ] Testar restauração do backup.
- [ ] Inventariar FKs, índices, uniques, enums, defaults e timezone.
- [ ] Confirmar janela, responsável e critério de abortar.

## Schema

- [ ] Migration Alembic aplica em banco vazio.
- [ ] Enums, tabelas, FKs e índices têm ordem correta.
- [ ] `property_id` existe ou é derivável nas tabelas operacionais.
- [ ] Uniques multi-tenant incluem `property_id`.
- [ ] Dinheiro usa `numeric`, não `float`.
- [ ] Tabelas expostas no Supabase possuem RLS antes de grants.

## Dados

- [ ] Importar tabelas pai antes das filhas.
- [ ] Preservar IDs e ajustar sequences.
- [ ] Comparar contagens, nulos, mínimos, máximos e somas relevantes.
- [ ] Não registrar CPF, e-mail ou outro dado pessoal em relatórios.
- [ ] Registrar linhas rejeitadas sem dados pessoais.

## Aplicação

- [ ] Runtime usa `postgresql+psycopg`.
- [ ] Migration usa conexão direta ou Supavisor sessão.
- [ ] Pool respeita limites do projeto.
- [ ] Startup não usa `create_all`.
- [ ] Health check não expõe erro interno.
- [ ] Suite API passa contra PostgreSQL.
- [ ] Testes cross-tenant passam.

## Cutover

- [ ] MySQL em somente leitura.
- [ ] Delta final migrado e validado.
- [ ] Segredos atualizados no ambiente.
- [ ] API reiniciada e smoke test aprovado.
- [ ] Métricas, erros e conexões monitorados.
- [ ] Critério de rollback não foi atingido.
