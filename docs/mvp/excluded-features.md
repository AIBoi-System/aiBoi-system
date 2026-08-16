---
title: "Funcionalidades Excluídas do MVP"
type: reference
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Funcionalidades Excluídas do MVP

As funcionalidades abaixo foram intencionalmente deixadas fora da versão inicial para reduzir a complexidade e acelerar o tempo de lançamento (Time-to-Market).

## Gestão Administrativa e Financeira
- **Financeiro Completo:** Fluxo de caixa, ROI, contas a pagar/receber. (Motivo: Complexidade de regras contábeis no MVP).
- **Estoque de Insumos:** Controle de inventário de farmácia e rações. (Risco: Distração do core zootécnico).
- **Emissão de GTA:** Guia de Trânsito Animal integrada. (Dependência: Órgãos governamentais).

## Gestão de Equipe Avançada
- **Hierarquia de Funcionários:** Papéis detalhados de Peão, Veterinário e Gerente. (Motivo: O MVP foca na visão do Dono/Gerente Único).
- **Auditoria:** Log detalhado de alterações por usuário. (Sugerido para V2).

## Tecnologia e Hardware
- **Integração Bluetooth:** Conexão com balanças eletrônicas e bastões. (Risco: Variedade de protocolos de hardware no mercado).
- **IoT e GPS:** Localização em tempo real do animal. (Impacto: Custo de infraestrutura inacessível para o MVP).
- **Sensores e Cercas Virtuais:** Telemetria de comportamento. (Versão Futura: Pós-V2).

## Inteligência Artificial
- **Reconhecimento Facial:** Identificação via câmera. (Pendente: Base de dados e processamento pesado).
- **Visão Computacional:** Pesagem por foto/vídeo. (Desejável para V3).
- **IA Preditiva:** Predição de produtividade e descarte. (Dependência: Histórico de dados de pelo menos 2 anos).

## Ecossistema e Serviços Externos
- **Marketplace:** Venda de gado ou insumos pelo app. (Negócio: Exige parcerias comerciais complexas).
- **Cursos e Consultorias:** Ambiente EAD integrado. (Impacto: Baixa prioridade técnica agora).

---

### Resumo de Impacto

| Item Excluído | Risco de Fazer Agora | Versão Sugerida |
| :--- | :--- | :--- |
| Financeiro | Erro em cálculos de lucro/prejuízo por falta de dados. | V2 |
| Bluetooth | Alta taxa de suporte técnico para pareamento de hardware. | V1.5 |
| GTA | Dependência de burocracia e APIs estatais instáveis. | Longo Prazo |
| IA Preditiva | Gerar conclusões erradas por falta de amostragem de dados. | Longo Prazo |
