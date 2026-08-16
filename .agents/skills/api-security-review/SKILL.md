---
name: api-security-review
description: Revisa APIs do AiBoi contra falhas de autenticação, autorização, validação, exposição de dados e riscos OWASP. Use ao revisar endpoints, login, uploads ou operações sensíveis. Palavras-chave: owasp, seguranca, jwt, idor, vulnerabilidade.
---

# API Security Review

Esta skill garante que o AiBoi proteja os dados sensíveis dos produtores rurais seguindo padrões OWASP.

## Quando usar esta skill

- Antes de finalizar um novo conjunto de endpoints.
- Ao revisar o fluxo de login ou cadastro.
- Quando houver manipulação de dados pessoais (CPF, e-mail).

## Quando não usar

- Para mudanças puramente estéticas no frontend.
- Ao lidar apenas com a lógica matemática de cálculos de peso.

## Contexto obrigatório

- `backend/app/shared/infrastructure/auth/`
- `backend/app/presentation/api/auth_dependencies.py`
- `backend/app/core/security_validators.py`

## Processo

1.  **Validar Autenticação**: Verifique se o token JWT é exigido e validado.
2.  **Verificar Autorização**: Garanta que o usuário tem a role necessária.
3.  **Checar IDOR**: Certifique-se de que um ID passado na URL pertence ao usuário.
4.  **Sanitização**: Valide se inputs de texto passam pelos validadores de segurança.

## Convenções

- Use `get_current_user` para proteger rotas.
- Senhas devem ser salvas apenas como hash (Bcrypt).
- Mensagens de erro de login não devem revelar qual campo está errado (email ou senha).

## Limites

### Sempre
- Bloquear acesso anônimo a dados de propriedades.
- Aplicar rate limiting em endpoints de autenticação.

### Perguntar primeiro
- Alterar o tempo de expiração dos tokens.
- Introduzir novos métodos de autenticação (ex: Social Login).

### Nunca
- Versar arquivos `.env` ou segredos no Git.
- Logar dados sensíveis (senhas, CPFs completos) em texto claro.

## Autoverificação

- Os tokens JWT expiram em tempo razoável?
- É possível acessar dados de outro proprietário mudando o ID na URL?
- Os campos sensíveis estão protegidos contra SQL Injection?
