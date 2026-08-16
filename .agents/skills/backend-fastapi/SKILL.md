---
name: backend-fastapi
description: Implementa e revisa funcionalidades backend em FastAPI seguindo as camadas e convenções do AiBoi. Use ao criar routers, casos de uso, schemas, serviços e integrações da API. Palavras-chave: router, endpoint, pydantic, usecase, di, fastapi.
---

# Backend FastAPI

Esta skill padroniza o desenvolvimento da API do AiBoi, focando na separação entre apresentação (FastAPI) e aplicação.

## Quando usar esta skill

- Ao criar novos endpoints ou roteadores.
- Ao implementar lógica de orquestração nos Use Cases.
- Ao atualizar esquemas de validação Pydantic.

## Quando não usar

- Para mudanças puramente visuais no frontend Flutter.
- Ao lidar apenas com a modelagem do domínio (use `ddd-modeling`).

## Contexto obrigatório

- `backend/app/presentation/api/v1/router.py`
- `backend/app/presentation/api/dependencies.py`
- `backend/app/main.py`

## Processo

1.  **Definir Schemas**: Crie DTOs de entrada e resposta usando Pydantic.
2.  **Implementar Use Case**: Desenvolva a lógica de orquestração na camada `application`.
3.  **Configurar Router**: Exponha o endpoint injetando as dependências necessárias.
4.  **Tratar Erros**: Use o padrão de exceções globais definido no projeto.

## Convenções

- Não acessar o banco de dados (`Session`) diretamente no Router.
- Usar `Depends()` para injeção de dependência.
- Padronizar respostas usando os Schemas do projeto.

## Limites

### Sempre
- Manter tipagem completa em funções e parâmetros.
- Atualizar a documentação OpenAPI (Swagger).

### Perguntar primeiro
- Alterar middlewares globais no `main.py`.
- Adicionar novas bibliotecas ao `requirements.txt`.

### Nunca
- Colocar lógica de negócio complexa dentro do roteador (arquivo de rota).
- Retornar modelos do banco de dados (ORM) diretamente na resposta da API.

## Autoverificação

- O endpoint está protegido por autenticação se necessário?
- Existe injeção de dependência sendo usada corretamente?
- O erro é retornado em formato JSON amigável?
