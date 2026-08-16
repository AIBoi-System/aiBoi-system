---
title: "Plano executável do MVP"
type: governance
status: active
owner: product
canonical: true
ai_index: true
last_verified: 2026-07-27
requirements:
  - RF001
  - RF002
  - RF003
  - RF004
  - RF005
  - RF006
  - RF008
  - RF009
  - RF011
---

# Plano executável do MVP

Este plano transforma o escopo canônico em ondas dependentes. Datas devem ser
estimadas pela equipe após executar a linha de base; a sequência não depende de
uma estimativa otimista.

## Princípios de priorização

1. remover risco de vazamento e perda de dados;
2. estabilizar capacidades das quais as demais dependem;
3. entregar fatias verticais demonstráveis;
4. limitar trabalho em andamento;
5. liberar apenas com evidência de aceite.

## Onda 0 — linha de base

Objetivo: saber com precisão o que funciona.

- executar testes backend e análise/testes Flutter;
- inventariar endpoints e telas reais;
- comparar banco, OpenAPI e documentação;
- classificar falhas por severidade;
- confirmar que nenhum segredo rastreado permanece válido;
- criar quadro com uma tarefa por lacuna verificável.

Saída: relatório de baseline e backlog ordenado.

## Onda 1 — fundação segura

Objetivo: tornar seguro continuar desenvolvendo.

- externalizar/rotacionar segredos;
- estabilizar JWT, sessão, verificação de e-mail e recuperação de senha;
- introduzir ou validar migrações versionadas;
- padronizar dependência de usuário e propriedade autenticados;
- padronizar erros e correlação de logs sem dados sensíveis;
- configurar CI para testes, análise estática e detecção de segredos.

Gate: nenhum endpoint privado relevante sem autenticação e nenhum bloqueador de
credenciais.

## Onda 2 — propriedade e isolamento

Objetivo: estabelecer a fronteira multi-tenant.

- concluir RF002;
- criar política única de autorização por propriedade;
- aplicar filtro em leitura, escrita e exclusão;
- cobrir BOLA/IDOR em properties, animals, batches, pastures, paddocks, weighing,
  health e reproduction;
- impedir vínculos entre entidades de propriedades diferentes.

Gate: suíte cross-tenant verde em todos os módulos operacionais existentes.

## Onda 3 — inventário operacional

Objetivo: entregar o núcleo de campo.

1. RF003 — animais e estados de vida;
2. RF004 — lotes e pertencimento;
3. RF009/RF008 — pastagens e piquetes;
4. pesagem como registro histórico;
5. integração Flutter dos fluxos e estados de erro.

Gate: usuário cria propriedade, animal, lote e área, registra peso e consulta os
dados apenas no tenant correto.

## Onda 4 — sanidade e reprodução

Objetivo: completar o manejo essencial.

- RF006 — registro sanitário individual ou por lote válido;
- RF005 — cobertura/inseminação, diagnóstico, protocolo e nascimento;
- validar sexo, datas, estado de vida e genealogia disponível;
- garantir histórico imutável ou auditável dos eventos;
- concluir telas, Cubits e testes das jornadas.

Gate: cenários principais e exceções possuem testes de domínio, API e jornada.

## Onda 5 — módulos, dashboard mínimo e acabamento

Objetivo: tornar o produto coerente e demonstrável.

- RF011 — ativação/listagem de módulos com autorização;
- dashboard apenas com indicadores derivados de dados confiáveis;
- estados vazios, carregamento, erro e acessibilidade;
- desempenho das consultas críticas;
- documentação de operação, backup e restauração.

Gate: nenhuma tela anuncia capacidade pós-MVP como disponível.

## Onda 6 — release piloto

Objetivo: entregar a um grupo controlado.

- suíte completa e regressão;
- teste E2E da criação de conta ao manejo;
- teste em dispositivos Android suportados;
- revisão de segurança e LGPD;
- backup, restauração, monitoramento e rollback ensaiados;
- política de privacidade e termos aprovados por responsável humano;
- aceite do Product Owner.

Saída: build Android reproduzível e release piloto observável.

## Backlog pós-MVP vindo da fonte histórica

| Capacidade | Ordem sugerida | Pré-condição |
|---|---|---|
| Offline e sincronização | primeira avaliação pós-MVP | conflitos, idempotência e armazenamento local definidos |
| Relatórios e histórico avançado | pós-MVP próximo | dados e indicadores estáveis |
| Alertas automáticos | pós-MVP próximo | regras, agenda e canal definidos |
| Colaboradores/permissões | pós-MVP | modelo RBAC e convite aprovados |
| Bluetooth/balanças | posterior | protocolos e hardware-alvo validados |
| Assinaturas/pagamentos | posterior | modelo comercial, fiscal e gateway aprovados |
| Financeiro/estoque | versão futura | regras contábeis e fiscais especializadas |
| GTA/SISBOV | longo prazo | integrações oficiais e conformidade |
| IA preditiva | longo prazo | volume, qualidade e governança de dados |

## Matriz de dependência

| Capacidade | Depende de |
|---|---|
| Propriedade | identidade |
| Animais | propriedade e autorização |
| Lotes | propriedade e animais |
| Pastagens | propriedade |
| Piquetes | propriedade e pastagem |
| Pesagem | propriedade e animal |
| Sanidade | propriedade e animal/lote |
| Reprodução | propriedade, animal e regras de sexo/estado |
| Nascimento | reprodução e criação de animal |
| Dashboard | consultas estáveis dos módulos |
| Offline futuro | contratos idempotentes e estratégia de conflito |

## Critério de sucesso do plano

O MVP termina quando os requisitos incluídos estão rastreados até testes, as
jornadas críticas funcionam em Android, o isolamento por propriedade foi
demonstrado e a operação possui mecanismos de backup, monitoramento e rollback.

