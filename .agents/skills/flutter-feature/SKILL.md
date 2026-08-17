---
name: flutter-feature
description: "Cria e revisa funcionalidades Flutter organizadas por feature, com estados, validações, integração de API e responsividade. Use ao implementar telas, fluxos, Cubits e componentes do AiBoi. Palavras-chave: cubit, widget, feature-first, mobile, responsividade."
---

# Flutter Feature

Esta skill guia o desenvolvimento da interface e lógica de UI do app AiBoi, focando em usabilidade para o campo.

## Quando usar esta skill

- Ao criar novas telas (Pages) ou componentes (Widgets).
- Ao implementar gerenciamento de estado com Bloc/Cubit.
- Ao integrar o frontend com novos endpoints do backend.

## Quando não usar

- Para mudanças estruturais no servidor Python.
- Ao lidar apenas com regras de negócio puras (use `ddd-modeling`).

## Contexto obrigatório

- `frontend/lib/core/widgets/`
- `frontend/lib/features/`
- `frontend/lib/core/network/api_client.dart`

## Processo

1.  **Modelar Dados**: Crie a Entidade e o Model (DTO) na pasta da feature.
2.  **Gerenciar Estado**: Desenvolva o Cubit e seus estados (Initial, Loading, Success, Error).
3.  **Construir UI**: Implemente a tela seguindo os princípios de baixa carga cognitiva.
4.  **Validar**: Adicione validações de formulário e tratamento de erros da API.

## Convenções

- Siga a estrutura: `data`, `domain`, `presentation`.
- Use widgets globais (ex: `PrimaryButton`) para manter consistência.
- Considere o uso offline (cache local futuramente).

## Limites

### Sempre
- Implementar estados de erro e loading visuais.
- Seguir o sufixo `_page.dart` ou `_widget.dart` para arquivos de UI.

### Perguntar primeiro
- Adicionar novos pacotes ao `pubspec.yaml`.
- Mudar o tema global de cores.

### Nunca
- Colocar lógica de negócio complexa dentro do método `build`.
- Usar `dynamic` quando é possível definir um tipo concreto.

## Autoverificação

- A tela funciona bem em dispositivos com tela pequena?
- O botão de ação principal está em local de fácil alcance?
- O erro da API é exibido de forma clara para o produtor?
