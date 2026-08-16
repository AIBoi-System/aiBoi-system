---
title: "Equipe de desenvolvimento orientada por agentes de IA"
type: governance
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-27
---

# Equipe de desenvolvimento orientada por agentes de IA

## Modelo de equipe

O AiBoi deve operar com uma equipe enxuta, organizada por responsabilidades. Um
mesmo humano pode acumular papéis, mas o agente que implementa uma mudança de alto
risco não deve ser o único a revisá-la.

| Papel | Responsabilidade principal | Entregáveis | Autoridade |
|---|---|---|---|
| Product Owner humano | Prioridade, escopo e aceite de negócio | decisões, backlog ordenado, aceite | decide escopo e termos centrais |
| Tech Lead humano | direção técnica e riscos | ADRs, padrões, aprovação de mudanças críticas | decide arquitetura e exceções |
| Agente Product Analyst | refinar necessidade em requisito testável | RF/RN, casos de uso, aceite | propõe; não muda escopo |
| Agente Domain/DDD | proteger linguagem e invariantes pecuárias | modelo, políticas, eventos | bloqueia inconsistência de domínio |
| Agente Backend | implementar FastAPI e casos de uso | routers, schemas, use cases, serviços | altera backend dentro do requisito |
| Agente Data | persistência e evolução de esquema | modelos, repositories, migrações, índices | altera dados com revisão |
| Agente Frontend | implementar experiência Flutter | telas, Cubits, estados, integração | altera frontend dentro do contrato |
| Agente Security/Tenant | autenticação, autorização e isolamento | threat review e testes BOLA/IDOR | bloqueia merge inseguro |
| Agente QA | estratégia e automação de testes | matriz, fixtures, regressão, E2E | bloqueia entrega sem evidência |
| Agente DevOps/SRE | ambientes, CI/CD e observabilidade | pipeline, deploy, rollback, runbooks | controla release técnico |
| Agente Documentation | sincronizar fontes canônicas | docs, links, changelog, ADR | bloqueia documentação contraditória |
| Revisor independente | revisar correção e manutenibilidade | parecer com severidade e evidências | aprova ou solicita mudanças |

## RACI por tipo de mudança

Legenda: **R** executa, **A** responde/aprova, **C** é consultado, **I** é informado.

| Mudança | PO | Tech Lead | Backend/Data | Frontend | Security | QA | Docs |
|---|---|---|---|---|---|---|---|
| Novo requisito de MVP | A | C | C | C | C | C | R |
| Regra de negócio | A | C | C | C | C | R | R |
| Endpoint privado | I | A | R | C | C | R | C |
| Tabela ou migração | I | A | R | I | C | C | C |
| Tela/fluxo Flutter | C | A | C | R | C | R | C |
| Autenticação/autorização | I | A | R | C | R | R | C |
| Correção crítica | I | A | R | R | C | R | I |
| Release | A | A | C | C | C | R | C |

## Limites dos agentes

Agentes podem implementar e revisar itens cujo escopo já esteja aprovado. Devem
parar e pedir decisão humana quando a mudança:

- adiciona ou remove requisito do MVP;
- altera `Propriedade`, `Animal`, `Lote`, `Piquete` ou outro termo central;
- escolhe fornecedor pago ou cria compromisso financeiro;
- muda banco, arquitetura macro ou estratégia de autenticação;
- reduz controle de segurança, cobertura ou retenção;
- trata questão legal, fiscal, contábil ou clínica como decisão definitiva.

## Formação recomendada por frente

Cada tarefa deve ter um trio mínimo:

1. **executor**: Backend, Data ou Frontend;
2. **especialista de risco**: Security/Tenant ou Domain;
3. **verificador**: QA ou revisor independente.

Para tarefas de baixo risco, a revisão pode ser assíncrona. Para autenticação,
isolamento, exclusão, migração, reprodução e sanidade, a revisão independente é
obrigatória.

## Handoffs obrigatórios

### Produto para engenharia

- problema, usuário e resultado;
- requisito e regra relacionados;
- aceite e fora de escopo;
- decisão humana pendente, se houver.

### Backend para frontend

- método, rota e autenticação;
- request, response e erros;
- paginação/filtros;
- exemplos sem dados pessoais;
- versão do contrato.

### Engenharia para QA

- risco da mudança;
- caminhos alterados;
- testes criados;
- dados e ambiente;
- efeitos colaterais esperados.

### Engenharia para documentação

- comportamento anterior e novo;
- requisito/regra afetado;
- evidência no código e testes;
- decisão arquitetural, quando aplicável.

## Indicadores da equipe

| Indicador | Meta inicial |
|---|---|
| Itens iniciados com Definition of Ready completa | 100% |
| Endpoints operacionais com teste cross-tenant | 100% |
| Regressões críticas abertas no release | 0 |
| Mudanças de banco com migração e rollback documentado | 100% |
| Requisitos MVP rastreados até testes | 100% |
| Documentação atualizada no mesmo PR | 100% |
| Lead time e retrabalho | medir por marco; definir meta após 2 ciclos |

Velocidade não deve ser otimizada contando tarefas geradas por IA. O indicador
útil é capacidade aceita, segura e sem regressão.

