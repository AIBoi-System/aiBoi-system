---
title: "Estrategia de testes"
type: explanation
status: active
owner: quality
canonical: true
ai_index: true
last_verified: 2026-07-16
---
# Estrategia de testes

## Piramide

1. Dominio: invariantes e objetos de valor.
2. Aplicacao: casos de uso com repositories simulados.
3. Integracao: SQLAlchemy e transacoes.
4. API: contrato, autenticacao e isolamento.
5. Flutter: Cubits, widgets e fluxos criticos.
6. Ponta a ponta: cadastro, propriedade e animal.

## Politica

Toda correcao recebe teste de regressao. Toda rota de propriedade recebe teste cross-tenant. Testes nao podem depender de ordem ou estado externo.

## Estado em 2026-07-16

A suite backend executada localmente apresentou 8 testes aprovados, 7 falhas e 3 erros. As causas incluem testes anteriores a autenticacao/property_id e defeitos reais em lote e recuperacao. Nao ha diretorio de testes Flutter.
