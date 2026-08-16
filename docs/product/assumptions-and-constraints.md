---
title: "Premissas e Restrições"
type: reference
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Premissas e Restrições

Este documento lista os fatores que aceitamos como verdadeiros para o projeto (Premissas) e as limitações que moldam nosso desenvolvimento (Restrições).

## Premissas (Hipóteses e Decisões)
- **Adoção de Dispositivos:** Assumimos que o produtor ou seu gerente possui um smartphone Android com especificações mínimas de 4GB de RAM.
- **Inserção de Dados:** O sucesso do sistema depende da disciplina do usuário em inserir os dados no momento do manejo.
- **Sincronização:** Os usuários entendem que precisam de sinal de internet em algum momento do dia para garantir o backup dos dados na nuvem.
- **Modelo de Negócio:** O modelo SaaS (Assinatura) é viável para o público de pequenos e médios produtores.

## Restrições (Limitações Reais)
- **Plataforma Única:** O desenvolvimento inicial é exclusivo para Android, deixando iOS e Web para fases futuras.
- **Conectividade:** O sistema deve ser projetado para áreas com "zero sinal" de internet durante 90% do tempo de uso.
- **Tempo de Mercado:** O MVP deve ser lançado em um cronograma agressivo para validar o mercado antes da expansão para ERP.
- **Equipe:** O desenvolvimento deve ser otimizado para uma equipe enxuta, priorizando tecnologias de alta produtividade.

## Distinções Importantes
- **Restrição Confirmada:** O foco exclusivo em pecuária de **Cria**. Não atenderemos Recria e Engorda no MVP.
- **Hipótese:** A interface simplificada converterá usuários que hoje preferem o papel.
- **Decisão Confirmada:** Uso de arquitetura modular preparando para expansão de microserviços.
