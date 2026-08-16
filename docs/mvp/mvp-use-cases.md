---
title: "Casos de Uso do MVP"
type: reference
status: deprecated
owner: documentation
canonical: false
ai_index: false
last_verified: 2026-07-16
---
# Casos de Uso do MVP

Esta seção detalha as interações essenciais entre os usuários (Atores) e o AiBoi.

## Gestão de Acesso
- **UC-MVP-01 Criar conta:** Usuário solicita registro -> Recebe código e-mail -> Define senha -> Cadastro concluído.
- **UC-MVP-02 Realizar login:** Usuário informa credenciais -> Sistema valida e gera token -> Acesso liberado.
- **UC-MVP-03 Gerenciar perfil:** Usuário edita nome/foto/endereço -> Sistema salva alterações.

## Configuração da Propriedade
- **UC-MVP-05 Cadastrar propriedade:** Usuário informa nome/área/localização -> Sistema cria registro vinculado ao dono.
- **UC-MVP-06 Selecionar propriedade:** Usuário escolhe uma fazenda da lista -> Sistema filtra todos os dados para aquela fazenda.
- **UC-MVP-16 Cadastrar piquete:** Usuário define nome e área do piquete -> Vincula à fazenda ativa.

## Operações com Animais
- **UC-MVP-07 Cadastrar animal:** Usuário informa Brinco/Sexo/Raça -> Sistema valida unicidade na fazenda -> Animal registrado.
- **UC-MVP-10 Registrar nascimento:** Usuário seleciona Matriz (mãe) -> Informa data e brinco da cria -> Novo animal criado no inventário.
- **UC-MVP-11 Registrar morte:** Usuário pesquisa animal -> Informa data/causa -> Sistema remove da lista de ativos e gera registro histórico.
- **UC-MVP-18 Registrar pesagem:** Usuário seleciona animal -> Digita peso em KG -> Sistema registra com data/hora.

## Manejo e Lotes
- **UC-MVP-12 Criar lote:** Usuário define nome do grupo -> Seleciona animais para incluir -> Lote formado.
- **UC-MVP-17 Movimentar lote:** Usuário seleciona lote -> Escolhe piquete de destino -> Sistema atualiza localização e data de entrada.

## Sanidade e Consulta
- **UC-MVP-19 Registrar vacinação:** Usuário seleciona animal/lote -> Escolhe vacina -> Registra data e responsável.
- **UC-MVP-25 Consultar histórico:** Usuário pesquisa brinco -> Sistema exibe timeline de nascimentos, pesos e vacinas.
- **UC-MVP-24 Consultar dashboard:** Usuário abre app -> Sistema exibe total de animais ativos, nascimentos do mês e mortes.

---

### Exemplo de Detalhamento: UC-MVP-07 (Cadastrar Animal)
- **Ator:** Gerente / Peão.
- **Pré-condição:** Estar logado em uma propriedade ativa.
- **Fluxo Principal:** 
    1. Usuário clica em "Novo Animal".
    2. Informa número do Brinco.
    3. Escolhe Sexo (M/F) e Categoria.
    4. Sistema verifica se brinco já existe na fazenda.
    5. Usuário clica em "Salvar".
- **Gatilho:** Necessidade de inclusão de animal recém-comprado ou não inventariado.
- **Critério de Aceitação:** O animal deve aparecer imediatamente na listagem filtrada por "Ativos".
