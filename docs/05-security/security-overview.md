---
title: "Visão de segurança"
type: explanation
status: partial
owner: security
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Visão de segurança

## Estado verificado

- **Crítico:** nenhum.
- **Alto:** nenhum identificado.
- **Médio:** o SMS local simula o fluxo no Mailpit, mas não comprova posse de
  um celular real.
- **Baixo:** compatibilidade futura entre Starlette e HTTPX e aviso de
  compatibilidade entre Passlib e versões recentes do bcrypt.
- **Security Score local:** 9,4/10.

O cadastro local está liberado para testes funcionais da interface. Produção
continua bloqueada para confirmação telefônica até a integração e o teste de
entrega com uma operadora real.

## Ativos

Dados pessoais, CPF, endereço, telefone, propriedades, inventário animal,
registros sanitários e reprodutivos, credenciais e sessões.

## Controles existentes

- Cadastro em seis etapas com OTP de e-mail e telefone de uso único e com
  expiração.
- CPF em tabela separada, endereço em tabela separada e validações no domínio.
- Senha aceita somente após confirmação de e-mail e telefone.
- Hash de senha, JWT com sessão persistida, rotação de refresh token, logout e
  revogação por redefinição de senha.
- Rate limiting; Redis obrigatório e alcançável em produção.
- Autorização no backend, isolamento por propriedade e testes BOLA/IDOR.
- OTP, senha, token e CPF completo ausentes de respostas e logs.
- Mailpit restrito ao loopback e recusado quando `ENV=production`.

## Limites do ambiente local

O Mailpit valida o fluxo entre Flutter, API e PostgreSQL sem custo, mas o
“SMS” é uma mensagem local. Ele não valida entrega por operadora nem posse da
linha. Antes da produção, substituir somente o adaptador de telefone por
Twilio, Zenvia, AWS ou equivalente e executar o cenário com uma operadora real.

## Testes faltantes para produção

- Entrega e confirmação por uma operadora de telefonia real.
- Homologação do provedor escolhido, incluindo timeout, indisponibilidade,
  retentativa controlada, expiração e prevenção de abuso.
- Teste de compatibilidade após futura atualização de Starlette/HTTPX e da
  biblioteca de hash de senha.

## Regra

Nenhuma rota operacional é considerada concluída sem autenticação,
autorização, isolamento por propriedade, validação, erro seguro e teste
cross-tenant.

