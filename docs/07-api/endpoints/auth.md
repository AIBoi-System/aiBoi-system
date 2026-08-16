---
title: "Endpoints de Auth"
type: reference
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-08-14
source_paths:
  - backend/app/presentation/api/v1/auth_router.py
---

# Endpoints de Auth

| Metodo | Caminho | Protecao atual | Finalidade |
|---|---|---|---|
| POST | `/auth/signup/send-code` | Pública com rate limit | Envia OTP de e-mail fora da resposta |
| POST | `/auth/signup/verify-code` | Pública com rate limit | Confirma e-mail com OTP de uso único |
| POST | `/auth/signup/send-phone-code` | Pública com rate limit | Envia OTP telefônico fora da resposta |
| POST | `/auth/signup/verify-phone-code` | Pública com rate limit | Confirma telefone com OTP de uso único |
| POST | `/auth/signup/register` | Pública com contatos confirmados | Valida CPF/endereço, cria usuário e sessão |
| POST | `/auth/login` | Pública com rate limit | Cria sessão e emite access/refresh tokens |
| POST | `/auth/refresh` | Refresh token | Rotaciona refresh token e sessão |
| POST | `/auth/logout` | JWT e sessão ativa | Revoga a sessão; retorna 204 |
| GET | `/auth/me` | JWT e sessão ativa | Retorna usuário atual |
| POST | `/auth/forgot-password` | Pública com resposta genérica | Envia token somente pelo canal externo |
| POST | `/auth/reset-password` | Token de recuperação | Atualiza senha, consome token e revoga sessões |

## Ordem obrigatória do cadastro

1. Solicitar e confirmar o e-mail.
2. Solicitar e confirmar o telefone.
3. Informar CPF e endereço válidos.
4. Definir a senha somente após as duas confirmações.
5. Persistir usuário, CPF e endereço atomicamente e iniciar a sessão.

OTP, senha, token de recuperação e CPF completo não aparecem em logs nem em
respostas indevidas. Com `AUTH_DELIVERY_MODE=mailpit`, e-mails e SMS simulados são
capturados somente em `127.0.0.1:8025`; esse modo é exclusivo de desenvolvimento
e falha fechado em produção até que um provedor real seja configurado.

## Regras de contrato

Rotas privadas exigem JWT associado a uma sessão ativa, autorização e isolamento
por propriedade. Refresh tokens são armazenados somente como hash, rotacionados a
cada uso e rejeitados quando reutilizados.
