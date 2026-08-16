---
title: "Comece aqui: execução do AiBoi por agentes de IA"
type: governance
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-08-14
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
  - RNF001
  - RNF002
  - RNF003
  - RNF004
---

# Comece aqui: execução do AiBoi por agentes de IA

Este é o ponto de entrada obrigatório para qualquer pessoa ou agente de IA que vá
planejar, implementar, revisar ou testar o AiBoi.

## Resultado esperado do MVP

Entregar um aplicativo Android e uma API que permitam ao pecuarista:

1. criar e recuperar uma conta;
2. cadastrar e selecionar uma propriedade;
3. manter o inventário de animais e lotes dessa propriedade;
4. cadastrar pastagens e piquetes;
5. registrar pesagens, sanidade, reprodução e nascimento;
6. consultar os dados sem atravessar os limites de outra propriedade.

O MVP não inclui modo offline, Bluetooth, pagamentos, financeiro, estoque,
colaboradores com permissões granulares, auditoria completa, alertas automáticos
ou relatórios avançados. Esses itens aparecem na fonte histórica, mas estão
classificados como pós-MVP até decisão humana que altere o escopo canônico.

## Ordem de leitura obrigatória

| Ordem | Documento | Pergunta respondida |
|---|---|---|
| 1 | [Contexto para IA](AI-CONTEXT.md) | Como distinguir fato, plano e fonte histórica? |
| 2 | [Escopo do MVP](02-mvp/mvp-scope.md) | O que entra e o que não entra? |
| 3 | [Requisitos](02-mvp/mvp-requirements.md) | Qual comportamento precisa existir? |
| 4 | [Regras de negócio](02-mvp/business-rules.md) | Quais invariantes nunca podem ser quebradas? |
| 5 | [Arquitetura](04-architecture/README.md) | Onde cada mudança deve ficar? |
| 6 | [Segurança](05-security/README.md) | Quais controles são bloqueadores? |
| 7 | [Módulo afetado](13-modules/README.md) | Qual é o contrato vertical da capacidade? |
| 8 | [Plano de execução](14-roadmap/mvp-execution-plan.md) | Em que ordem o trabalho deve acontecer? |
| 9 | [Equipe de IA](12-engineering/ai-development-team.md) | Quem implementa, revisa e aprova? |
| 10 | [Fluxo de entrega](12-engineering/ai-delivery-workflow.md) | Quais evidências tornam a tarefa concluída? |

Depois da leitura, o agente deve inspecionar o código e os testes do módulo. A
documentação não autoriza declarar uma capacidade como implementada sem evidência
executável.

## Fontes e precedência

Em caso de conflito, aplicar esta ordem:

1. decisão humana aprovada e registrada;
2. regra canônica em `docs/02-mvp` ou `docs/03-domain`;
3. comportamento confirmado pelo código e por teste verde;
4. contrato técnico canônico;
5. especificação histórica.

Conflitos não devem ser resolvidos por preferência do agente. Registre o conflito
como decisão pendente, informe impacto e proponha opções.

## Contrato mínimo de toda tarefa

Uma tarefa só pode entrar em desenvolvimento quando contém:

- requisito e regra de negócio relacionados;
- propriedade/tenant afetado;
- fluxo feliz, erros esperados e permissões;
- campos de entrada e saída;
- critérios de aceite verificáveis;
- testes necessários;
- módulos e documentos afetados;
- dependências e itens explicitamente fora de escopo.

Toda entrega deve incluir:

- código no módulo correto;
- migração quando houver alteração persistente;
- testes de domínio, API e/ou widget proporcionais ao risco;
- teste cross-tenant para acesso a recurso operacional;
- erros seguros e estáveis;
- documentação e changelog atualizados;
- comandos de verificação executados e respectivos resultados.

## Regras que bloqueiam merge

- consulta, atualização ou exclusão de recurso sem filtro por propriedade;
- autorização baseada apenas em ID fornecido pelo cliente;
- segredo, token, senha, CPF real ou credencial em código, log ou exemplo;
- alteração de tabela sem migração versionada;
- endpoint sem autenticação quando manipula dados privados;
- funcionalidade planejada apresentada como disponível;
- teste removido ou afrouxado apenas para fazer a suíte passar;
- mudança no escopo do MVP ou em termo central sem decisão humana.

## Mapa técnico atual

| Área | Tecnologia e direção |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, API REST versionada |
| Organização backend | Monólito modular, DDD e Clean Architecture como alvo |
| Frontend | Flutter organizado por feature, Cubit para estado |
| Banco atual | PostgreSQL com psycopg 3 e schema versionado por Alembic; SQLite apenas em testes rápidos |
| Plataforma prioritária | Android |
| Contrato | OpenAPI executável mais documentos em `docs/07-api` |
| Isolamento | Todo dado operacional pertence a uma propriedade |

## Sequência curta para iniciar hoje

1. Executar a suíte atual e registrar a linha de base.
2. Fechar segredos, autenticação e recuperação de conta.
3. Padronizar migrações e o contexto de propriedade.
4. Cobrir isolamento de todos os endpoints privados.
5. estabilizar, nessa ordem: propriedade, animais, lotes, áreas, pesagem,
   sanidade e reprodução;
6. integrar os fluxos Flutter aos contratos validados;
7. executar jornada ponta a ponta e checklist de release Android.

## Decisões pendentes que exigem responsável humano

- definir o ambiente PostgreSQL gerenciado de produção, backups e janela de implantação;
- definir provedor de e-mail transacional e política de entrega;
- definir hospedagem, ambientes e orçamento operacional;
- escolher métricas-alvo de produto e grupo piloto;
- priorizar, após o MVP, offline, Bluetooth, pagamentos e relatórios;
- aprovar textos legais, política de privacidade e termos de uso.

Nenhuma dessas decisões impede corrigir segurança, testes, isolamento ou concluir
os fluxos essenciais já aprovados.
