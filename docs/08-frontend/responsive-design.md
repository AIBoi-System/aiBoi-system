---
title: "Responsive Design"
type: reference
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Responsive Design

## Objetivo

Adaptação de layout por restrições, não por escalonamento arbitrário de fonte.

## Especificação

O documento especifica responsabilidades, limites, fluxo esperado, estados de falha e evidências necessárias para responsive design.

## Estado atual

O app usa largura fluida até 412 px. Em navegadores maiores, o viewport do app
é centralizado sobre fundo neutro, preservando as proporções dos frames móveis
de 400×844 sem esticar cartões, inputs ou botões. Em celulares menores, a
largura continua sendo determinada pelas restrições reais do dispositivo.

## Regras

- Toda tela assíncrona trata loading, vazio, erro e sucesso.
- Validação visual não substitui backend.
- Layouts funcionam em 320 px sem sobreposição.
- Autorização não depende de esconder controles.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Frontend Overview](frontend-overview.md)
- [Authorization](../05-security/authorization.md)
- [Frontend Tests](../10-quality/frontend-tests.md)
