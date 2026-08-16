---
name: testing-pytest
description: Cria e revisa testes backend com Pytest para domínio, casos de uso, repositories e API. Use ao adicionar funcionalidades, corrigir bugs ou validar regras de negócio. Palavras-chave: pytest, fixture, mock, assertion, cobertura, integration-test.
---

# Testing Pytest

Esta skill foca na garantia de qualidade técnica e funcional do backend do AiBoi.

## Quando usar esta skill

- Ao implementar uma nova regra de negócio (criar o teste junto).
- Após uma refatoração para garantir que não houve regressão.
- Ao corrigir um bug (criar o teste que reproduz o erro).

## Quando não usar

- Para testes manuais via Swagger UI.
- Para testes de interface no Flutter.

## Contexto obrigatório

- `backend/tests/conftest.py`
- `backend/tests/api/`

## Processo

1.  **Definir Escopo**: Escolha entre teste unitário (domínio) ou integração (API).
2.  **Preparar Fixtures**: Use as fixtures do `conftest.py` para criar usuários e propriedades de teste.
3.  **Executar Ação**: Realize a chamada ao método ou endpoint.
4.  **Validar**: Verifique o status code, o JSON de retorno e o estado no banco de dados.

## Convenções

- Nomeie arquivos de teste começando com `test_`.
- Use `TestClient` para testes de API.
- Teste o isolamento (Multi-Tenancy) tentando acessar dados com o usuário errado.

## Limites

### Sempre
- Limpar o banco de dados de teste após cada execução (usando fixtures de teardown).
- Testar caminhos de erro (exceções) e não apenas o "fluxo feliz".

### Perguntar primeiro
- Adicionar novas dependências de teste (ex: `factory-boy`).
- Ignorar testes que estão falhando na CI.

### Nunca
- Usar o banco de dados de produção para rodar testes.
- Comitar testes que dependem de ordem de execução.

## Autoverificação

- O teste passa localmente com `python -m pytest`?
- As asserções são específicas e não apenas genéricas?
- O banco de dados fica limpo após o teste?
