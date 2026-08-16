---
title: "Authentication"
type: reference
status: active
owner: security
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Authentication

## Objetivo

Validação de identidade por senha e JWT, incluindo expiração, usuários desativados e falhas.

## Especificação vigente

JWT contém subject, papel, identificador de sessão, emissão e expiração. A API
valida assinatura, algoritmo permitido, usuário ativo e sessão não revogada. A
aplicação falha em produção sem chave forte e sem rate limiting Redis alcançável.

## Cadastro e autenticação

- Cadastro exige confirmação de e-mail e telefone por OTP temporário e de uso único.
- CPF e endereço são validados antes da transação de criação.
- A senha só é aceita depois das duas confirmações.
- Login cria sessão revogável; logout e redefinição de senha revogam sessões.
- Login Google exige `email_verified=true` e confirmação telefônica para cadastro.
- Os endpoints públicos de cadastro, login e recuperação possuem rate limit.
- Em desenvolvimento, e-mail e SMS simulado são capturados pelo Mailpit limitado
  ao loopback. Esse modo nunca comprova posse real do telefone e é proibido em
  produção.

## Controles e regras

- Negar por padrão e aplicar menor privilégio.
- Validar autorização no backend e por recurso.
- Nunca registrar ou retornar segredo, senha, token ou CPF completo.
- Falhas entre tenants são bloqueadoras de release.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Postura do ambiente local

O ambiente local está liberado para testar o cadastro completo pela interface,
com score de segurança 9,4/10. O OTP de telefone capturado no Mailpit é apenas
uma simulação funcional: produção permanece bloqueada até a entrega por uma
operadora real. Não há issues críticas ou altas identificadas nesta revisão.

## Referências

- [Security Overview](security-overview.md)
- [Security Checklist](security-checklist.md)
- [Business Rules](../02-mvp/business-rules.md)
