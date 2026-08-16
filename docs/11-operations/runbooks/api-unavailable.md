---
title: "Runbook: Api Unavailable"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Runbook: Api Unavailable

## Detectar

Aplicativo recebe timeout, conexão recusada ou taxa elevada de 5xx; health check falha.

## Conter e diagnosticar

1. Confirmar ambiente, horário, versão e alcance do impacto.
2. Verificar processo/container da API, porta, proxy, certificado e configuração.
3. Consultar logs pelo correlation_id sem exibir corpos sensíveis.
4. Testar dependência de banco e e-mail separadamente.
5. Se a última implantação causou o incidente, executar rollback aprovado.

## Verificar recuperação

Raiz e fluxo autenticado respondem, latência normaliza e erros deixam de crescer.

## Escalonar

Escalonar imediatamente em caso de vazamento entre propriedades, perda de dados, credencial exposta, indisponibilidade prolongada ou recuperação sem procedimento seguro. Registrar linha do tempo, impacto, causa confirmada e ação preventiva.
