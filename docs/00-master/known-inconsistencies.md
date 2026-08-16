---
title: "Inconsistencias conhecidas"
type: reference
status: active
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Inconsistencias conhecidas

| ID | Divergencia | Decisao atual |
|---|---|---|
| INC-001 | Fonte historica usa AGROFENCE/SGB; repositorio usa AiBoi | AiBoi e o nome oficial |
| INC-002 | Fonte cita apenas Android; Flutter possui alvos adicionais | Android e prioridade do MVP; outros alvos nao implicam suporte |
| INC-003 | Resolvida: codigo antigo e ADR-004 mantinham MySQL como banco atual | PostgreSQL/psycopg 3 e Alembic sao vigentes conforme ADR-007; ADR-004 permanece historica |
| INC-004 | Arquitetura alvo e DDD/Clean, mas varios modulos sao legados | Manter estado como migracao parcial |
| INC-005 | Parte das rotas nao possui isolamento por propriedade | Tratar como debito critico, nao como comportamento aceito |
| INC-006 | Suite backend atual nao esta verde | Liberacao bloqueada ate atualizacao de codigo/testes |
| INC-007 | Documentacao antiga separa MVP e futuro de forma diferente | `02-mvp` governa a classificacao vigente |
