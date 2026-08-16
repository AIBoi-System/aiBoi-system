---
title: "Documentação Executiva do MVP - AiBoi"
type: governance
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Documentação Executiva do MVP - AiBoi

Este diretório contém a especificação detalhada e os guias operacionais para o desenvolvimento e validação do **MVP (Minimum Viable Product)** do AiBoi. Esta documentação traduz a visão estratégica em requisitos executáveis.

## Objetivo
O objetivo desta pasta é fornecer um roteiro claro para a equipe de desenvolvimento e stakeholders sobre o que deve ser entregue na primeira fase do produto, focando exclusivamente na gestão bovina básica para produtores de cria.

## Responsabilidade dos Documentos

| Documento | Responsabilidade |
| :--- | :--- |
| [mvp-scope.md](mvp-scope.md) | Define os limites do que o sistema faz hoje. |
| [included-features.md](included-features.md) | Detalha as funcionalidades que serão entregues. |
| [excluded-features.md](excluded-features.md) | Lista o que foi removido do escopo para garantir agilidade. |
| [mvp-requirements.md](mvp-requirements.md) | Requisitos funcionais e não funcionais numerados. |
| [mvp-use-cases.md](mvp-use-cases.md) | Descrição dos fluxos de interação usuário-sistema. |
| [business-rules.md](business-rules.md) | Regras lógicas e restrições de negócio da pecuária. |
| [user-flows.md](user-flows.md) | Jornada do usuário de ponta a ponta. |
| [acceptance-criteria.md](acceptance-criteria.md) | Critérios para validação de cada funcionalidade (Gherkin). |
| [definition-of-ready.md](definition-of-ready.md) | Requisitos para que uma tarefa entre em desenvolvimento. |
| [definition-of-done.md](definition-of-done.md) | Critérios para considerar uma funcionalidade concluída. |
| [dependencies.md](dependencies.md) | Mapeamento de relações entre módulos e ordem de execução. |
| [risks-and-assumptions.md](risks-and-assumptions.md) | Incertezas, riscos técnicos e hipóteses de mercado. |
| [release-criteria.md](release-criteria.md) | Condições mínimas para o lançamento público do MVP. |
| [test-scenarios.md](test-scenarios.md) | Roteiros de teste para garantia de qualidade. |
| [future-backlog.md](future-backlog.md) | Itens pendentes para versões posteriores (V1, V2). |

## Ordem de Consulta e Prioridade
Em caso de divergência entre documentos ou entre a documentação e o código, a ordem de prioridade para resolução de conflitos é:

1.  **mvp-scope.md** (O que estamos fazendo?)
2.  **mvp-requirements.md** (O que o sistema deve fazer?)
3.  **business-rules.md** (Quais as travas de negócio?)
4.  **acceptance-criteria.md** (Como validar?)
5.  **Documentação Mestre** (Visão geral histórica)

## MVP vs Roadmap
Esta pasta foca no **agora**. Qualquer funcionalidade que não esteja listada em `included-features.md` deve ser tratada como parte do `future-backlog.md`, independentemente de sua importância estratégica a longo prazo.
