# AiBoi — Frontend (Flutter)

Aplicativo multiplataforma para gestão pecuária: onboarding, cadastro com verificação de e-mail, propriedades e painel inicial.

---

## Stack

| Item | Tecnologia |
| :--- | :--- |
| Framework | Flutter 3.11+ (Dart) |
| Estado | flutter_bloc |
| Fonte | Poppins (assets) |
| Plataformas | Android, iOS, Web, Windows, Linux, macOS |

---

## Estrutura

```text
frontend/lib/
├── app/                    # MaterialApp e tema
├── core/
│   ├── di/                 # Injeção de dependências
│   ├── navigation/         # Rotas nomeadas
│   ├── theme/              # Cores e tipografia
│   └── widgets/            # Componentes reutilizáveis
└── features/
    ├── auth/               # Login e boas-vindas
    ├── registration/       # Fluxo de cadastro
    ├── property/           # Cadastro de propriedade
    └── home/               # Minhas propriedades
```

---

## Pré-requisitos

- [Flutter SDK](https://docs.flutter.dev/get-started/install) compatível com `sdk: ^3.11.0` no `pubspec.yaml`
- Editor (VS Code / Android Studio) com extensão Flutter

---

## Executar

```bash
cd frontend
flutter pub get
flutter run
```

Para dispositivo específico:

```bash
flutter devices
flutter run -d chrome
```

---

## Fluxo de telas (cadastro)

| Etapa | Tela | Rota |
| :--- | :--- | :--- |
| 0 | Boas-vindas (carrossel) | `/` |
| 1 | Acesse sua conta | `/signup` |
| 2 | Dados pessoais 1/3 | `/signup/personal` |
| 3 | Verificar e-mail 2/3 | `/signup/verify-email` |
| 4 | Criar senha 3/3 | `/signup/password` |
| 5 | Endereço | `/signup/address` |
| 6 | Cadastro concluído | `/signup/complete` |
| 7 | Cadastrar propriedade (opcional) | `/property/create` |
| 8 | Propriedade cadastrada | `/property/success` |
| 9 | Home | `/home` |

Login existente: `/login` → após sucesso pode ir para `/home`.

---

## Design

Paleta principal (Figma):

- Verde escuro (botões primários): `#1B4332`
- Verde progresso / sucesso: `#7CB518`
- Fundo claro: `#FFFFFF` / `#F8F9F8`

Componentes compartilhados: barra de progresso em 3 passos, campos com label, OTP de 5 dígitos, indicador de força de senha.

---

## Assets

```text
frontend/assets/
├── images/          # bg_welcome_page.jpg (onboarding)
└── fonts/           # Poppins
```

Se `bg_welcome_page.jpg` não existir, a tela de boas-vindas usa gradiente verde como fallback.

---

## Integração com API

Por padrão o app usa a **API real** em `http://localhost:8000`.

```bash
# Desktop / iOS simulator
flutter run

# Android emulator (localhost do host)
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000

# Mock offline
flutter run --dart-define=USE_MOCK_API=true
```

Endpoints usados:

- `POST /auth/signup/send-code`
- `POST /auth/signup/verify-code`
- `POST /auth/signup/register`
- `POST /auth/login`
- `POST /addresses/`
- `POST /properties/`

---

## Qualidade

```bash
flutter analyze
flutter test
```

---

## Build

```bash
flutter build apk
flutter build web
```
