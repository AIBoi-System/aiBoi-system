---
name: tenant-isolation
description: Garante o isolamento de dados entre usuários e propriedades do AiBoi. Use ao implementar ou revisar consultas, endpoints, repositories e permissões que acessam dados de uma fazenda. Palavras-chave: multi-tenant, isolamento, property_id, seguranca, acesso.
---

# Tenant Isolation

Esta skill é o coração do sistema de segurança do AiBoi, garantindo que as fazendas sejam universos paralelos e isolados.

## Quando usar esta skill

- Ao implementar qualquer consulta ao banco de dados.
- Ao revisar rotas que recebem `property_id` como parâmetro.
- Ao criar novos recursos que pertençam a uma propriedade.

## Quando não usar

- Para recursos globais do sistema que não pertencem a propriedades (ex: logs de erro do sistema).
- Ao lidar apenas com a interface visual sem dados reais.

## Contexto obrigatório

- `docs/mvp/data_isolation_plan.md` (Referência do plano de isolamento)
- `backend/app/shared/infrastructure/persistence/property_repository.py`

## Processo

1.  **Validar Propriedade**: Verifique se o `property_id` passado pertence ao `current_user`.
2.  **Injetar Filtro**: Garanta que o repository sempre receba o `property_id`.
3.  **Proteger Criacao**: Ao criar recursos, vincule-os automaticamente à propriedade validada.
4.  **Impedir Vazamento**: Certifique-se de que nenhum Join SQL traga dados de outras propriedades.

## Convenções

- Não confie no `property_id` vindo do frontend sem validá-lo no backend.
- Use o helper `_verify_property_access` nos routers.

## Limites

### Sempre
- Bloquear operações de escrita se o usuário não for o dono (ou tiver permissão).
- Retornar 404 em vez de 403 ao tentar acessar recursos de outros tenants (evita descoberta de IDs).

### Perguntar primeiro
- Implementar compartilhamento de recursos entre propriedades diferentes.
- Alterar a lógica global de verificação de acesso.

### Nunca
- Consultar animais ou lotes usando apenas o ID primário sem o `property_id` no `filter`.

## Autoverificação

- Se eu mudar o ID na URL para o de outro usuário, eu consigo ver o dado?
- O recurso criado foi salvo com o `property_id` correto?
- O usuário logado realmente tem acesso a essa fazenda?
