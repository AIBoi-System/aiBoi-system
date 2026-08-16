---
name: documentation-update
description: Atualiza a documentação modular do AiBoi após mudanças de requisitos, regras, API, banco, arquitetura ou interface. Use quando uma alteração de código ou decisão modificar o comportamento documentado. Palavras-chave: doc, roadmap, srs, changelog, adr.
---

# Documentation Update

Esta skill mantém os documentos de produto e processo sincronizados com a realidade do código do AiBoi.

## Quando usar esta skill

- Sempre que o escopo do MVP mudar.
- Ao adicionar uma nova Regra de Negócio que precise ser registrada.
- Após decisões arquiteturais importantes (criar ADR).

## Quando não usar

- Para documentação interna de código (Docstrings).
- Para arquivos README de pastas técnicas que não descrevem comportamento.

## Contexto obrigatório

- `docs/product/`
- `docs/mvp/`
- `docs/mvp/README.md` (Prioridades)

## Processo

1.  **Identificar Impacto**: Veja quais documentos são afetados (Scope, Requirements, Rules).
2.  **Atualizar Texto**: Reflita a mudança de forma objetiva e sem duplicidade.
3.  **Cross-Reference**: Garanta que as referências entre documentos continuem válidas.
4.  **Registrar Decisão**: Se for uma mudança estrutural, use o formato de ADR (Architectural Decision Record).

## Convenções

- Mantenha a distinção clara entre MVP e Futuro.
- Use linguagem de negócio da pecuária.
- Não copie e cole o mesmo conteúdo em vários arquivos.

## Limites

### Sempre
- Manter o Glossário atualizado com novos termos.
- Seguir as prioridades definidas no `docs/mvp/README.md`.

### Perguntar primeiro
- Alterar o escopo do MVP (remover ou adicionar RFs).
- Mudar a nomenclatura de termos centrais do negócio.

### Nunca
- Deixar documentação obsoleta sem nota de depreciação.
- Incluir detalhes de implementação técnica em documentos de produto.

## Autoverificação

- O documento alterado segue o formato padrão?
- A mudança foi refletida em todos os arquivos relacionados?
- O texto está em português do Brasil correto e profissional?
