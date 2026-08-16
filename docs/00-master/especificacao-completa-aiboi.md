---
title: "Especificacao completa do AiBoi"
type: reference
status: partial
owner: documentation
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Especificacao completa do AiBoi

> Versao documental: 2.0  
> Data de consolidacao: 2026-07-16  
> Estado: Em evolucao

## Finalidade

O AiBoi e um sistema mobile e web de apoio a gestao de rebanhos bovinos em propriedades de cria. Centraliza cadastro, inventario animal, lotes, areas de manejo, pesagens, sanidade e reproducao, reduzindo registros dispersos e melhorando a rastreabilidade.

## Publico

- Pecuarista responsavel pela propriedade e pelas decisoes.
- Trabalhador de campo responsavel por registros operacionais.
- Tecnico, veterinario ou zootecnista que acompanha manejo e indicadores.
- Administrador da plataforma, limitado a funcoes operacionais autorizadas.

## Escopo funcional consolidado

| ID | Capacidade | Prioridade | Estado no repositorio |
|---|---|---|---|
| RF001 | Identidade, cadastro, login e recuperacao de conta | Essencial | Parcial |
| RF002 | Gestao de propriedades | Essencial | Parcial |
| RF003 | Cadastro e consulta de animais | Essencial | Implementado com lacunas de teste |
| RF004 | Gestao de lotes | Essencial | Parcial |
| RF005 | Reproducao e protocolos | Essencial | Parcial |
| RF006 | Registros sanitarios | Essencial | Parcial |
| RF008 | Gestao de piquetes | Essencial | Parcial |
| RF009 | Gestao de pastagens | Essencial | Parcial |
| RF011 | Ativacao de modulos | Essencial | Parcial |
| RF022 | Historico cronologico do animal | Importante | Planejado |
| RF007, RF010, RF012-RF021, RF023-RF025 | Nutricao, relatorios, financeiro, estoque, alertas, colaboradores, pagamentos, transferencias, genealogia, balancas e suporte | Pos-MVP | Planejado |

## Requisitos nao funcionais

- RNF001: dados de uma propriedade nao podem ser acessados por usuarios sem vinculo autorizado.
- RNF002: senhas devem ser armazenadas apenas como hash forte.
- RNF003: tokens e segredos nao podem aparecer em respostas, logs ou repositorio.
- RNF004: operacoes de campo devem ter interface simples e adequada a telas pequenas.
- RNF005: erros da API devem ser previsiveis e nao revelar detalhes internos.
- RNF006: operacoes criticas devem possuir testes automatizados.
- RNF007: o aplicativo deve preparar evolucao para conectividade instavel, sem declarar modo offline antes de sua implementacao.

## Regras centrais

- RN001: toda entidade operacional pertence a uma propriedade.
- RN002: o identificador do animal e unico dentro da propriedade.
- RN003: apenas usuarios autorizados podem alterar dados da propriedade.
- RN004: nascimento adiciona um animal ativo e mantem vinculo genealogico quando informado.
- RN005: morte ou saida encerra a participacao ativa sem apagar o historico.
- RN006: registros sanitarios e reprodutivos devem apontar para animal ou lote valido da mesma propriedade.
- RN007: alteracoes financeiras, de assinatura e permissao exigem autorizacao explicita.
- RN008: funcionalidades planejadas nao podem ser apresentadas como disponiveis.

## Arquitetura

Monorepo com API FastAPI/SQLAlchemy e aplicativo Flutter. A arquitetura alvo e monolito modular com DDD e Clean Architecture. O modulo de animais e o mais aderente; modulos legados ainda acessam SQLAlchemy por servicos estaticos.

## Persistencia

O codigo atual usa SQLAlchemy com PostgreSQL e psycopg 3. Alembic e a autoridade
do schema e o startup da API nao cria tabelas. SQLite permanece apenas nos testes
rapidos; a validacao de integracao usa PostgreSQL.

## Qualidade e liberacao

Uma versao somente pode ser liberada quando os requisitos incluidos possuem criterios de aceite, testes verdes, isolamento por propriedade, tratamento de erro e documentacao atualizada.

## Navegacao detalhada

Use o [indice geral](../INDEX.md) para acessar a decomposicao completa desta especificacao.
