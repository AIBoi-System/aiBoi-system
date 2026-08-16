---
title: "Regras de negocio"
type: reference
status: active
owner: product
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Regras de negocio

| ID | Regra |
|---|---|
| RN001 | Todo recurso operacional pertence a exatamente uma propriedade. |
| RN002 | A propriedade deve pertencer ao usuario ou estar vinculada por permissao explicita. |
| RN003 | O numero de identificacao do animal e unico dentro da propriedade. |
| RN004 | Um registro sanitario referencia animal ou lote da mesma propriedade. |
| RN005 | Nascimento cria animal ativo e registra origem genealogica quando disponivel. |
| RN006 | Morte, venda ou transferencia preservam o historico e alteram o estado de vida. |
| RN007 | Um lote nao pode receber animal de outra propriedade. |
| RN008 | Piquete pertence a uma pastagem e ambos pertencem a mesma propriedade. |
| RN009 | Datas futuras somente sao aceitas quando representam previsao declarada. |
| RN010 | Senha, token, CPF e segredo nunca sao expostos em log ou resposta indevida. |
| RN011 | Funcionalidade planejada nao pode ser apresentada como concluida. |
| RN012 | Protocolos reprodutivos e suas etapas formam catalogo global: usuarios autenticados podem consultar, mas somente admin pode criar ou modificar o catalogo. |
| RN013 | O cadastro somente define a senha depois da confirmação de e-mail e telefone. |
| RN014 | CPF pertence a uma relação one-to-one separada, é validado e único no sistema. |
| RN015 | Endereço é uma entidade separada e deve conter CEP, UF e campos obrigatórios válidos. |
| RN016 | Refresh token é de uso rotativo; logout e redefinição de senha revogam sessões. |
| RN017 | Após o cadastro, criação ou alteração de dados exige usuário autenticado e autorizado. |
