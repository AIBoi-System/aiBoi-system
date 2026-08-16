---
name: sqlalchemy-repository
description: Implementa e revisa repositories SQLAlchemy com filtros de propriedade, transações, relacionamentos e tipagem segura. Use ao criar ou corrigir persistência no backend do AiBoi. Palavras-chave: orm, sqlalchemy, persistencia, query, join, transaction.
---

# SQLAlchemy Repository

Esta skill foca na camada de dados do backend, garantindo consultas eficientes e seguras.

## Quando usar esta skill

- Ao implementar novos métodos de busca ou salvamento.
- Ao configurar relacionamentos entre tabelas (ex: Animal e Lote).
- Ao realizar migrações de banco de dados com Alembic.

## Quando não usar

- Para mudanças na lógica de UI ou apresentação.
- Quando o foco é apenas a modelagem de domínio (use `ddd-modeling`).

## Contexto obrigatório

- `backend/app/shared/infrastructure/database/connection.py`
- `backend/app/shared/infrastructure/persistence/`

## Processo

1.  **Definir Model**: Mapeie a tabela usando SQLAlchemy.
2.  **Criar Interface**: Declare os métodos necessários na camada de domínio.
3.  **Implementar Repository**: Codifique a lógica SQL, aplicando `property_id` obrigatoriamente.
4.  **Mapper**: Configure a conversão entre o model do banco e a entidade do domínio.

## Convenções

- Use `kw_only=True` em dataclasses para evitar erros de ordem de argumento.
- Sempre filtre por `property_id` em consultas de recursos da fazenda.
- Use exclusão lógica para recursos que possuem histórico.

## Limites

### Sempre
- Gerenciar transações (`commit`/`rollback`) corretamente nos serviços.
- Usar `joinedload` para evitar o problema de N+1 consultas.

### Perguntar primeiro
- Executar SQL puro (`text()`).
- Mudar nomes de colunas em tabelas existentes.

### Nunca
- Deletar dados físicos sem confirmação de que o histórico não é necessário.
- Esquecer de fechar sessões de banco de dados.

## Autoverificação

- Todas as queries filtram por `property_id`?
- Os relacionamentos estão configurados com `cascade` adequado?
- Existe uma migração Alembic para mudanças estruturais?
