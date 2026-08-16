---
name: code-review
description: Revisa alterações do AiBoi quanto a correção, arquitetura, segurança, testes, desempenho e aderência às convenções do projeto. Use ao revisar commits, branches, pull requests ou mudanças locais. Palavras-chave: review, refatoracao, padrao, arquitetura, qualidade.
---

# Code Review

Esta skill atua como um portão de qualidade final para garantir que o AiBoi mantenha sua integridade técnica.

## Quando usar esta skill

- Ao finalizar uma tarefa de desenvolvimento.
- Antes de submeter uma mudança para o repositório principal.
- Ao analisar código de terceiros ou gerado por outros agentes.

## Quando não usar

- Durante o rascunho inicial de uma funcionalidade.
- Para tarefas de infraestrutura pura (ex: mudar porta do Docker).

## Contexto obrigatório

- `backend/ARCHITECTURE.md` (Se existir)
- `.agents/skills/` (Todas as outras competências)

## Processo

1.  **Analise Funcional**: O código faz o que foi pedido no Requisito do MVP?
2.  **Verificar Arquitetura**: Respeita DDD e Clean Architecture? Existem imports proibidos?
3.  **Checar Isolamento**: O `property_id` está sendo usado corretamente?
4.  **Revisar Testes**: Existem testes para os novos fluxos? Eles cobrem erros?
5.  **Legibilidade**: Nomes de variáveis e arquivos seguem o padrão do projeto?

## Convenções

- Priorize a manutenibilidade sobre a "esperteza" do código.
- Aplique os princípios de design do AiBoi (ex: baixa carga cognitiva).

## Limites

### Sempre
- Bloquear códigos que ignoram o isolamento por propriedade.
- Exigir tratamento de loading e erro no frontend.

### Perguntar primeiro
- Sugerir refatorações em módulos estáveis que não foram tocados.
- Recomendar padrões de design novos (ex: Visitor, Command) não usados no projeto.

### Nunca
- Aprovar código com segredos ou chaves em texto claro.
- Deixar passar variáveis `dynamic` ou sem tipagem no Python.

## Autoverificação

- O código é autoexplicativo?
- Existe duplicação desnecessária?
- O impacto em outros módulos foi considerado?
