---
title: "Runbook: Login Failure"
type: how-to
status: planned
owner: operations
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Runbook: Login Failure

## Detectar

Usuários válidos recebem 401, tokens são recusados ou taxa de falha cresce.

## Conter e diagnosticar

1. Confirmar se falha afeta uma conta, papel, ambiente ou todos.
2. Verificar nomes e presença das variáveis JWT sem revelar valores.
3. Comparar relógio, algoritmo e expiração entre emissão e validação.
4. Verificar banco de usuários, status da conta e compatibilidade bcrypt/passlib.
5. Não desabilitar autenticação nem usar chave padrão para restaurar serviço.

## Verificar recuperação

Login válido emite token, inválido permanece 401, /auth/me funciona e logs não contêm credenciais.

## Escalonar

Escalonar imediatamente em caso de vazamento entre propriedades, perda de dados, credencial exposta, indisponibilidade prolongada ou recuperação sem procedimento seguro. Registrar linha do tempo, impacto, causa confirmada e ação preventiva.
