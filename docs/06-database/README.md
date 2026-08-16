---
title: "Banco de dados"
type: governance
status: active
owner: data
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Banco de dados

> Estado: documento indice.

Esta secao organiza as decisoes e especificacoes de banco de dados do AiBoi. A fonte de verdade deve ser interpretada junto do [indice geral](../INDEX.md), da [especificacao mestra](../00-master/especificacao-completa-aiboi.md) e do codigo atual.

## Principios

- Distinguir claramente comportamento implementado, parcial e planejado.
- Evitar duplicar regras; referenciar o documento proprietario.
- Registrar mudancas relevantes no changelog e, quando necessario, em ADR.

## Conteudo

- [Database Overview](database-overview.md)
- [Conceptual Model](conceptual-model.md)
- [Logical Model](logical-model.md)
- [Physical Model](physical-model.md)
- [Erd](erd.md)
- [Data Dictionary](data-dictionary.md)
- [Tables](tables.md)
- [Relationships](relationships.md)
- [Constraints](constraints.md)
- [Indexes](indexes.md)
- [Enums](enums.md)
- [Naming Conventions](naming-conventions.md)
- [Migrations](migrations.md)
- [Seeds](seeds.md)
- [Transactions](transactions.md)
- [Soft Delete](soft-delete.md)
- [Audit Fields](audit-fields.md)
- [Multi Tenancy](multi-tenancy.md)
- [Backup And Restore](backup-and-restore.md)
- [Data Retention](data-retention.md)
- [Performance Guidelines](performance-guidelines.md)
