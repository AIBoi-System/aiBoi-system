---
title: "Confirmações locais com Mailpit"
type: runbook
status: active
owner: backend
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Confirmações locais com Mailpit

## Objetivo

Testar gratuitamente o cadastro por e-mail e celular sem expor OTP na resposta
HTTP ou nos logs e sem depender de um fornecedor externo.

## Funcionamento

- Interface local: `http://127.0.0.1:8025/`.
- SMTP local: `127.0.0.1:1025`.
- E-mail aparece com o destinatário informado no cadastro.
- SMS simulado aparece como `sms-<últimos 4 dígitos>@agrofence.local`.
- O número completo não é colocado na mensagem simulada.
- `ENV=production` recusa o adaptador Mailpit.

Esse fluxo valida telas, API, expiração, uso único e persistência. Ele não comprova
entrega por operadora nem posse real do telefone e, portanto, não libera produção.

## Iniciar

```powershell
.\scripts\start_mailpit.ps1
```

Depois, mantenha no `backend/.env` protegido:

```dotenv
ENV=development
AUTH_DELIVERY_MODE=mailpit
MAILPIT_SMTP_HOST=127.0.0.1
MAILPIT_SMTP_PORT=1025
MAILPIT_FROM_EMAIL=no-reply@agrofence.local
```

Nunca publique a porta 8025, a porta 1025 ou a pasta `.local-data` na rede.

## Testar pela interface gráfica

Com PostgreSQL, API e Mailpit ativos, gere e inicie o Flutter Web apontando para
a API local:

```powershell
cd frontend
flutter build web --dart-define=API_BASE_URL=http://127.0.0.1:8000
python -m http.server 8080 --bind 127.0.0.1 --directory build/web
```

Abra `http://127.0.0.1:8080/`, escolha **Criar conta** e siga as seis etapas.
Consulte em `http://127.0.0.1:8025/` primeiro o código do e-mail e depois a
mensagem de telefone simulada. Nunca use uma senha real neste ambiente de
desenvolvimento.
