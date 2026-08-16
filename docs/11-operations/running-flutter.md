---
title: "Running Flutter"
type: how-to
status: active
owner: operations
canonical: true
ai_index: true
last_verified: 2026-08-14
---

# Running Flutter

## Objetivo

Dependências, seleção de dispositivo e execução do aplicativo.

## Especificação

No diretório frontend, executar `flutter pub get`, `flutter analyze`,
`flutter test` e `flutter run`. A URL da API deve ser adequada ao emulador ou
dispositivo.

Para o navegador local:

```powershell
flutter run -d web-server --web-hostname 127.0.0.1 --web-port 8080 `
  --dart-define=API_BASE_URL=http://127.0.0.1:8000
```

O login Google é opcional no desenvolvimento. Para habilitá-lo, informe
`--dart-define=GOOGLE_CLIENT_ID=<cliente-web>`; sem essa variável, o cadastro
por e-mail e telefone continua disponível.

## Estado atual

Norma vigente para novas alterações e releases.

## Regras

- Produção não usa segredo versionado.
- Mudança possui rollback e verificação.
- Operação é repetível e observável.
- Backup só é válido após teste de restauração.

## Critérios de verificação

- Comportamento principal e falhas possuem passos reproduzíveis.
- Entradas, saídas, dependências e responsáveis estão explícitos.
- Segurança, tenant e dados sensíveis foram avaliados.
- Testes e documentação são atualizados na mesma alteração.

## Referências

- [Environment Setup](environment-setup.md)
- [Secrets Management](../05-security/secrets-management.md)
- [Api Unavailable](runbooks/api-unavailable.md)
