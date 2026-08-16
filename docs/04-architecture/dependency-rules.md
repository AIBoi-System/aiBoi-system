---
title: "Regras de dependência do backend"
type: specification
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Regras de dependência do backend

## Objetivo

Preservar DDD, SOLID e isolamento entre camadas durante a migração incremental
do monólito modular. Este documento é a fonte canônica para dependências Python
do backend.

## Estrutura real

Os contextos delimitados existentes são `inventory` e `health`. Não se deve
criar outro contexto nem mudar uma raiz de agregado sem decisão arquitetural
explícita. A única raiz de agregado declarada atualmente é `Animal`.

Cada contexto pode conter:

- `domain`: entidades, objetos de valor, invariantes e portas;
- `application`: casos de uso e orquestração;
- `infrastructure`: adapters SQLAlchemy e implementações de portas.

`shared/domain` contém apenas primitivas de domínio. `shared/application` e
`shared/infrastructure` hospedam capacidades transversais e componentes legados
que ainda não foram movidos para adapters próprios.

## Direção permitida

```text
presentation -> application -> domain
                         ^
                         |
                 infrastructure
```

- `domain` não importa FastAPI, Pydantic, SQLAlchemy, presentation,
  application ou infrastructure.
- Um domínio não importa o domínio de outro contexto. Colaboração entre
  agregados ocorre por contrato de aplicação, identificadores ou eventos.
- `application` coordena o fluxo e depende de portas do domínio. Não contém
  detalhes HTTP nem deve criar novas dependências em schemas de presentation.
- `infrastructure` implementa portas e conhece ORM, banco, e-mail e provedores.
  Não deve criar novas dependências em presentation.
- Routers validam transporte, autenticação e autorização, chamam application e
  formatam a resposta. Não executam consultas ORM nem importam models.
- A composição de dependências ocorre em `presentation/api/dependencies.py` ou
  no bootstrap; esse ponto pode conhecer implementações concretas.

## DDD e SOLID

- Entidades protegem invariantes; routers e models ORM não são entidades.
- Interfaces de repository pertencem ao domínio que as consome (DIP).
- Casos de uso têm uma razão de mudança e uma operação principal (SRP).
- Novos adapters implementam portas existentes em vez de adicionar condições
  de fornecedor aos casos de uso (OCP e DIP).
- Portas pequenas por capacidade são preferíveis a repositories genéricos
  extensos (ISP).
- Implementações devem preservar o contrato de suas portas, inclusive 404
  entre tenants e rollback em falhas (LSP).

## Isolamento multi-tenant

Recursos de fazenda são consultados por `id + property_id`. O `property_id`
deve ter sido autorizado para o usuário atual antes de chegar ao repository.
Criações recebem o tenant validado; joins incluem a condição de tenant; não há
transferência implícita entre propriedades.

## Exceções legadas congeladas

Os testes arquiteturais mantêm uma lista explícita das violações atuais. A lista
não é permissão para repetir o padrão; ela impede novas ocorrências e deve
diminuir quando cada fluxo for migrado.

Exceções atuais:

- serviços de health, pasture, paddock, property e auth ainda recebem schemas
  de presentation;
- repositories de pasture e paddock ainda recebem schemas Pydantic;
- `auth_router.py` ainda acessa persistência diretamente no password reset;
- alguns application services legados ainda usam models ORM sem portas.

O dashboard de propriedade deixou de executar SQL no router em 2026-08-14. A
consulta permanece temporariamente no application service e deve migrar para
uma porta de leitura dedicada quando esse fluxo for modularizado.

## Guardrails automatizados

`backend/tests/architecture/test_layer_dependencies.py` é executado pelo Pytest
da CI e verifica:

- pureza do domínio;
- ausência de dependência entre domínios de contextos diferentes;
- conjunto explícito de contextos e raízes de agregado;
- ausência de novas dependências application/infrastructure -> presentation;
- ausência de novos imports de persistência e SQL direto em routers.

Uma exceção nova exige decisão documentada e teste atualizado na mesma mudança.
Remover dívida exige remover também sua entrada da lista permitida.

## PEP 8

Código arquitetural novo segue PEP 8, tipagem explícita nas fronteiras e imports
agrupados. Formatação não justifica refatorar comportamento estável fora do
escopo da mudança.

## Referências

- [Arquitetura atual](current-architecture.md)
- [Limites dos módulos](module-boundaries.md)
- [Isolamento de tenants](../05-security/tenant-isolation.md)
- [Visão do backend](../09-backend/backend-overview.md)
