---
title: "Authentication"
type: reference
status: partial
owner: backend
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Authentication

## Objetivo

Uso do Bearer JWT e tratamento de tokens ausentes, inválidos e expirados.

## Especificação

JWT deve conter subject, papel, emissão e expiração; a API valida assinatura e algoritmo permitido. A aplicação deve falhar ao iniciar sem chave forte. O código atual procura JWT_SECRET_KEY enquanto o ambiente legado usa outro nome, criando risco de default conhecido.

## Estado atual

Parcial. Existem componentes relacionados, mas a revisão do repositório encontrou lacunas que impedem considerar o tema concluído.

## Controles e regras

- Schemas validam toda entrada e saída.
- Rotas privadas exigem autenticação, autorização e tenant.
- Erros não expõem implementação.
- Coleções usam paginação quando crescerem.

## Verificação

- Testar caminho válido, entrada inválida e falha de dependência.
- Testar acesso sem credencial, com papel insuficiente e entre propriedades quando aplicável.
- Verificar rollback e ausência de dados sensíveis em resposta e log.
- Comparar documentação, schema executável e comportamento observado.

## Referências

- [Api Overview](api-overview.md)
- [Animals](endpoints/animals.md)
- [Api Security](../05-security/api-security.md)
