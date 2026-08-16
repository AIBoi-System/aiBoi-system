---
title: "Fluxo de entrega para humanos e agentes de IA"
type: how-to
status: active
owner: engineering
canonical: true
ai_index: true
last_verified: 2026-07-27
---

# Fluxo de entrega para humanos e agentes de IA

## Unidade de trabalho

Prefira uma fatia vertical pequena: regra + API + persistência + interface + teste.
Quando isso não for possível, publique primeiro o contrato e use flags ou estados
planejados; não simule conclusão.

## Etapas

### 1. Descoberta

- localizar requisito, regra, módulo e código existentes;
- confirmar estado: implementado, parcial ou planejado;
- identificar tenant, dados sensíveis e integrações;
- registrar divergências antes de alterar código.

Saída: resumo factual com fontes e riscos.

### 2. Refinamento

Criar um cartão com:

```text
Objetivo:
Usuário/ator:
Requisitos e regras:
Pré-condições:
Fluxo feliz:
Falhas e mensagens:
Autorização/tenant:
Contrato de dados/API:
Critérios de aceite:
Testes:
Fora de escopo:
Dependências:
Documentos afetados:
```

Saída: item que atende à Definition of Ready.

### 3. Contrato

- definir schema de entrada e saída;
- definir invariantes no domínio;
- definir propriedade das transações;
- definir erros estáveis e códigos HTTP;
- definir estados de tela: inicial, carregando, vazio, sucesso, erro e sem acesso.

Saída: contrato revisado por backend, frontend, QA e segurança quando privado.

### 4. Implementação

Backend:

- router apenas adapta HTTP;
- caso de uso orquestra a operação;
- domínio protege invariantes;
- repository sempre recebe o contexto autorizado de propriedade;
- transação fecha a unidade de trabalho;
- schema não expõe modelo persistente acidentalmente.

Frontend:

- feature separa presentation, domain e data;
- Cubit/estado representa todos os estados observáveis;
- datasource trata contrato HTTP;
- erros são traduzidos para mensagens úteis;
- navegação não substitui autorização do servidor.

Dados:

- migração é versionada, revisável e compatível com dados existentes;
- chave estrangeira, unicidade e índice refletem invariantes;
- exclusão histórica usa estado/soft delete quando exigido pela regra.

### 5. Verificação

Executar conforme o risco:

- testes unitários de domínio e casos de uso;
- testes de repository com banco;
- testes de API para sucesso, validação, não encontrado e sem acesso;
- teste cross-tenant com dois usuários/propriedades;
- testes de Cubit, widget e jornada;
- análise estática, formatação e build;
- verificação de migração para frente e estratégia de rollback.

O relato deve indicar comando, resultado e qualquer verificação não executada.

### 6. Revisão

O revisor procura, nesta ordem:

1. violação de segurança e tenant;
2. quebra de regra de negócio;
3. perda/corrupção de dados;
4. incompatibilidade de contrato;
5. ausência de teste;
6. desempenho, legibilidade e documentação.

Comentários devem citar caminho e linha, explicar impacto e propor condição de
correção. Preferências estilísticas não devem bloquear entrega quando o padrão
automático estiver satisfeito.

### 7. Conclusão e release

- critérios de aceite demonstrados;
- suíte relevante verde;
- documentação e changelog atualizados;
- observabilidade suficiente para falhas;
- plano de rollback para mudança de alto risco;
- aceite do PO para capacidade visível ao usuário.

## Paralelismo seguro

Pode ocorrer em paralelo:

- testes e documentação após contrato aprovado;
- Flutter com mock fiel ao contrato versionado;
- endpoints de módulos diferentes sem tabelas compartilhadas;
- threat review durante implementação.

Deve ocorrer em sequência:

- decisão de escopo antes do desenvolvimento;
- migração antes do código que depende do novo schema em produção;
- contrato antes da integração frontend/backend;
- correção de bloqueadores antes do release.

## Formato de relatório do agente

```text
Resultado:
Arquivos alterados:
Requisitos atendidos:
Decisões e hipóteses:
Segurança/tenant:
Testes executados:
Testes não executados:
Riscos restantes:
Próximo item desbloqueado:
```

## Escalonamento

Quando bloqueado, o agente deve apresentar:

- fato confirmado;
- decisão necessária;
- duas ou três opções;
- impacto, risco e recomendação;
- trabalho seguro que pode continuar sem a decisão.

