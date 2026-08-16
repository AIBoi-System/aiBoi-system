---
title: "Requisitos do MVP"
type: reference
status: active
owner: product
canonical: true
ai_index: true
last_verified: 2026-08-14
---
# Requisitos do MVP

| ID | Requisito | Prioridade | Evidencia esperada |
|---|---|---|---|
| RF001 | Cadastrar e autenticar usuario | Essencial | API, tela e teste |
| RF002 | Gerenciar propriedades proprias | Essencial | CRUD isolado |
| RF003 | Gerenciar animais por propriedade | Essencial | CRUD e invariantes |
| RF004 | Gerenciar lotes por propriedade | Essencial | CRUD isolado |
| RF005 | Registrar reproducao e nascimento | Essencial | Eventos por propriedade e catalogo global gravavel apenas por admin |
| RF006 | Registrar sanidade | Essencial | Animal ou lote valido |
| RF008 | Gerenciar piquetes | Essencial | Vinculo a propriedade/pastagem |
| RF009 | Gerenciar pastagens | Essencial | CRUD isolado |
| RF011 | Listar modulos contratados | Essencial | Autorizacao por proprietario |
| RNF001 | Isolamento entre propriedades | Bloqueador | Teste cross-tenant |
| RNF002 | Protecao de credenciais | Bloqueador | Segredo externo e hash |
| RNF003 | Interface para telas pequenas | Alta | Widget e verificacao visual |
| RNF004 | Erros seguros e consistentes | Alta | Testes de contrato |
| RNF005 | Rate limiting distribuido em producao | Bloqueador | `REDIS_URL` obrigatoria, Redis alcancavel e teste multi-instancia |
