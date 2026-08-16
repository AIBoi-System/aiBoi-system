# Regras de Negócio do MVP

As regras abaixo garantem a integridade dos dados zootécnicos e o isolamento entre propriedades.

## 1. Regras de Conta e Segurança (ACC)
- **BR-ACC-001:** O CPF deve ser validado pelo algoritmo oficial e ser único no sistema.
- **BR-ACC-002:** Um e-mail só pode ser registrado após a verificação bem-sucedida do código (OTP) enviado.
- **BR-ACC-003:** A senha deve possuir no mínimo 8 caracteres e conter pelo menos um número.

## 2. Regras de Animal e Inventário (ANM)
- **BR-ANM-001:** A identificação (Brinco) do animal deve ser única por **Propriedade**. Dois proprietários diferentes podem ter animais com o mesmo brinco, mas nunca na mesma fazenda.
- **BR-ANM-002:** Animais marcados como "Morto" ou "Vendido" não podem receber novos registros de pesagem ou vacina.
- **BR-ANM-003:** O registro de nascimento exige a identificação de uma Matriz (mãe) ativa para garantir a genealogia.
- **BR-ANM-004:** O óbito realiza uma **exclusão lógica**; o animal some da lista de ativos, mas seu histórico permanece acessível para relatórios.

## 3. Regras de Lote e Espaço (BAT)
- **BR-BAT-001:** Um animal ativo só pode pertencer a um único lote por vez. Ao ser transferido, ele deve sair automaticamente do lote anterior.
- **BR-BAT-002:** Não é possível excluir um lote que possua animais vinculados.
- **BR-BAT-003:** Um piquete não pode ser removido se estiver marcado como "Ocupado" por um lote.

## 4. Regras de Manejo e Pesagem (WGH)
- **BR-WGH-001:** O valor do peso deve ser sempre positivo (> 0).
- **BR-WGH-002:** A data de pesagem não pode ser anterior à data de nascimento ou de entrada do animal na propriedade.
- **BR-WGH-003:** Em caso de pesagem coletiva (Lote), o sistema deve replicar o registro para todos os animais vinculados no momento da ação.

## 5. Regras de Sanidade e Reprodução (HLT/REP)
- **BR-HLT-001:** O registro de vacinação deve obrigatoriamente conter a data de aplicação e o tipo de vacina.
- **BR-REP-001:** Um diagnóstico de prenhez só pode ser registrado para fêmeas (Sexo=F) e com data posterior à última cobertura registrada.
- **BR-REP-002:** O registro de parto não pode ter data futura (maior que o dia atual).

## 6. Regras de Movimentação (MOV)
- **BR-MOV-001:** Uma movimentação de lote exige que o piquete de destino seja diferente do piquete de origem.
- **BR-MOV-002:** Toda movimentação deve atualizar o contador de "Dias de Ocupação" do piquete.
