---
title: "Sequência de implementação das telas"
type: governance
status: active
owner: frontend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Sequência de implementação das telas

## Objetivo

Ordenar as entregas Flutter em fatias verticais que atravessem tela, estado,
caso de uso, API e PostgreSQL, sem criar dependências circulares entre features.
Este documento detalha a execução visual das ondas definidas no
[plano executável do MVP](../14-roadmap/mvp-execution-plan.md).

## Gate comum de cada tela

Uma tela só está concluída quando:

- possui estados de carregamento, vazio, sucesso e erro;
- funciona em largura de 320 px e possui semântica de acessibilidade;
- usa DTOs tipados e o cliente HTTP central;
- envia `property_id` da propriedade ativa quando o recurso é operacional;
- trata 401, 404, 409/422 e indisponibilidade de rede sem expor erro interno;
- possui teste de Cubit/widget e teste do contrato da API correspondente;
- não usa visibilidade de botão como mecanismo de autorização.

## Ordem de implementação

| Ordem | Fatia vertical | Telas | Contratos principais | Gate específico |
|---:|---|---|---|---|
| 1 | Sessão | boas-vindas, login, recuperação e cadastro | `/auth/*` | token, expiração e usuário inativo testados |
| 2 | Tenant ativo | cadastro, seleção e detalhe da propriedade | `/properties/`, `/addresses/` | troca de propriedade limpa estado da feature anterior |
| 3 | Visão inicial | home e dashboard | `/properties/{id}/dashboard` | indicadores pertencem somente ao tenant ativo |
| 4 | Inventário | lista, cadastro e detalhe do animal | `/animals/` | identificação única por propriedade e CRUD completo |
| 5 | Organização do rebanho | lotes, pastagens e piquetes | `/batches/`, `/pastures/`, `/paddocks/` | vínculos cruzados entre propriedades são rejeitados |
| 6 | Pesagem | histórico e nova pesagem | `/weighings/` | peso/data validados e histórico atualizado |
| 7 | Sanidade | lista e registro sanitário | `/health/` | animal ou lote pertence ao tenant ativo |
| 8 | Reprodução | ciclos, protocolos, etapas e nascimento | `/reproductions/` | regras de sexo, datas, catálogo e nascimento testadas |
| 9 | Encerramentos | morte, venda e histórico | contratos de inventário/eventos | histórico preservado e listas ativas atualizadas |
| 10 | Acabamento | perfil, permissões, estados offline e acessibilidade | contratos compartilhados | regressão E2E da jornada principal verde |

## Estrutura padrão por feature

```text
feature/
├── data/
│   ├── datasources/
│   ├── models/
│   └── repositories/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
└── presentation/
    ├── cubits/
    ├── pages/
    └── widgets/
```

Dependências apontam para dentro: apresentação usa casos de uso; casos de uso
dependem de contratos do domínio; `data` implementa esses contratos. Uma feature
não importa a camada `data` de outra feature.

## Evidência atual da fundação

Em 2026-08-14, a API gerou 44 paths e 78 operações OpenAPI sem `operationId`
duplicado, respondeu ao endpoint de banco e executou CRUD real transacional no
PostgreSQL local. Cada fatia ainda precisa do próprio teste de jornada Flutter
antes de ser considerada concluída.

## Referências

- [Feature Architecture](feature-architecture.md)
- [API Integration](api-integration.md)
- [Loading](screen-states/loading.md), [Empty](screen-states/empty.md) e
  [Error](screen-states/error.md)
- [Tenant Isolation](../05-security/tenant-isolation.md)
- [API Standards](../07-api/api-standards.md)
