---
name: ddd-modeling
description: Analisa e modela domínios usando DDD, incluindo entidades, agregados, objetos de valor, invariantes, serviços e eventos de domínio. Use ao criar ou revisar regras de negócio e limites de módulos. Palavras-chave: entidade, agregado, valor, invariante, limites, ubiqua.
---

# DDD Modeling

Esta skill guia a modelagem do domínio do AiBoi garantindo que as regras de negócio da pecuária estejam isoladas e bem representadas.

## Quando usar esta skill

- Ao definir novos conceitos de negócio (ex: novos tipos de reprodução).
- Ao revisar limites de módulos (Bounded Contexts) para evitar acoplamento.
- Ao identificar invariantes que precisam ser protegidas no código.

## Quando não usar

- Para tarefas puramente técnicas de banco de dados ou UI.
- Ao lidar com infraestrutura que não impacta a lógica de negócio.

## Contexto obrigatório

- `docs/product/glossary.md`
- `docs/mvp/business-rules.md`
- `backend/app/shared/domain/`

## Processo

1.  **Identificar Linguagem Ubíqua**: Use termos do `glossary.md` (ex: Matriz, Brinco).
2.  **Definir Agregados**: Agrupe entidades relacionadas sob uma raiz (Aggregate Root).
3.  **Encapsular Invariantes**: Garanta que validações básicas (ex: peso positivo) ocorram dentro do domínio.
4.  **Separar de Models**: Certifique-se de que as entidades de domínio não dependam do SQLAlchemy.

## Convenções

- Use `AggregateRoot` da `shared/domain/entity.py`.
- Regras que cruzam múltiplos agregados devem ir para um `DomainService`.

## Limites

### Sempre
- Manter lógica de negócio dentro das pastas `domain`.
- Usar nomes em inglês no código e termos de negócio corretos em Docstrings.

### Perguntar primeiro
- Criar novos módulos (Contextos Delimitados).
- Mudar a raiz de um agregado existente.

### Nunca
- Colocar lógica de persistência (SQL) dentro de entidades de domínio.
- Criar entidades anêmicas (apenas com campos, sem comportamento).

## Autoverificação

- A linguagem está alinhada com o glossário?
- As regras de negócio estão protegidas por invariantes?
- Existe dependência de bibliotecas externas no domínio?
