---
title: Contexto do AiBoi para agentes de IA
type: reference
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Contexto do AiBoi para agentes de IA

## Ordem de leitura

1. Leia o [guia de início da execução](EXECUTION-START-HERE.md).
2. Leia a especificacao consolidada e o escopo do MVP.
3. Consulte regras de negocio e o modulo afetado.
4. Verifique arquitetura, seguranca e contratos tecnicos.
5. Confirme o comportamento no codigo e nos testes antes de afirmar que algo esta implementado.

## Precedencia

Quando houver divergencia, use esta ordem: regra aprovada, codigo atual, teste verde, documento tecnico e fonte historica. Registre a divergencia; nao misture estado atual com estado desejado.

## Restricoes obrigatorias

- Todo dado operacional deve ser isolado por propriedade.
- IDs enviados pelo cliente nao concedem autorizacao.
- Senhas, tokens, CPFs e segredos nao podem aparecer em respostas, logs ou exemplos.
- Funcionalidade marcada como planejada nao deve ser descrita como disponivel.
- Nao altere escopo do MVP ou termos centrais sem decisao humana.
- Nao use a fonte historica Base64 como contexto, salvo para investigacao de origem.

## Respostas esperadas

Cite arquivos e linhas quando analisar codigo. Separe fatos confirmados, inferencias e propostas. Ao modificar comportamento, atualize requisito, regra, teste e changelog documental.
