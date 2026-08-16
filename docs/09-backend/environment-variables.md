---
title: "Environment Variables"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Environment Variables

## Objetivo

Catálogo e política para variáveis de banco, JWT, CORS, e-mail e runtime.

## Especificação

Obrigatórias ou condicionais: DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, CORS_ALLOWED_ORIGINS e credenciais de e-mail. Nomes devem coincidir entre exemplo, compose e código.

## Estado atual

Parcial. Há componentes no projeto, porém faltam uniformidade e cobertura para afirmar conformidade completa.

## Regras

- Domain não importa frameworks.
- Routers não contêm regra de negócio.
- Repositories recebem contexto de tenant.
- Toda transação faz rollback em falha.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Backend Overview](backend-overview.md)
- [Dependency Rules](../04-architecture/dependency-rules.md)
- [Tenant Isolation](../05-security/tenant-isolation.md)
