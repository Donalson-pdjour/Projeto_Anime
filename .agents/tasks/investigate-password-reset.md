# Relatório de Investigação — Fluxo de Recuperação de Senha

**Data:** investigação estática do código-fonte  
**Arquivo principal inspecionado:** `app/routes/auth.py`

---

## Resumo Executivo

O fluxo de recuperação de senha está **parcialmente correto** nas novas versões das funções (banco de dados), mas o arquivo `auth.py` está **corrompido**: ele contém o módulo inteiro duplicado. A segunda metade do arquivo define versões antigas das funções — que usam um dicionário em memória (`PASSWORD_RESET_TOKENS`) — e registra as mesmas rotas pela segunda vez. Isso causa erros de inicialização (`AssertionError: View function mapping is overwriting an existing endpoint function`) e faz com que as versões **antigas** (quebradas) de `_create_password_reset_token` e `_get_valid_reset_entry` sobrescrevam as novas no namespace do módulo. **O sistema não funciona no estado atual.**

---

## Respostas às Perguntas de Investigação

### 1. GET /recuperar-senha renderiza o template correto?
**✅ SIM.**  
`auth.py` linha ~218: `return render_template("auth/recuperar_senha/solicitar.html")` — caminho correto.

---

### 2. solicitar.html tem action correto, method POST, campo 'email'?
**✅ SIM.**  
- `action="{{ url_for('auth.password_recovery_request') }}"` — correto.  
- `method="post"` — correto.  
- `<input name="email" type="email" ...>` — presente.  
- Token CSRF presente: `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.

---

### 3. POST /recuperar-senha valida e-mail, busca usuário, gera token, chama send_password_reset_email?
**⚠️ PARCIALMENTE — depende de qual versão da função é executada (veja Bug #1).**

A primeira versão da rota `password_recovery_request` (linha ~220):
- Valida o e-mail com `_valid_email()` ✅  
- Busca o usuário no banco com `SELECT id, nome, email, ativo` ✅  
- Chama `_create_password_reset_token(user["id"])` — **sem o argumento `email`** ✅ (a nova versão só aceita `user_id`)  
- Gera `reset_url` com `url_for("auth.password_reset", token=token, _external=True)` ✅  
- Chama `send_password_reset_email(user["email"], reset_url)` ✅  

A segunda versão duplicada (linha ~370+) chama `_create_password_reset_token(user["id"], user["email"])` — assinatura da versão antiga.

---

### 4. _create_password_reset_token salva o token na tabela password_reset_tokens?
**❌ NÃO — a versão que prevalece no namespace usa dicionário em memória.**

Existem **duas definições** de `_create_password_reset_token` no arquivo:

| Definição | Linha aprox. | Comportamento |
|-----------|-------------|---------------|
| Primeira (correta) | ~65 | Salva no banco MySQL via `INSERT … ON DUPLICATE KEY UPDATE` |
| Segunda (antiga, **substitui a primeira**) | ~320 | Salva em `PASSWORD_RESET_TOKENS` (dicionário em memória) |

Em Python, quando um módulo define a mesma função duas vezes, a **segunda definição vence**. Portanto, `_create_password_reset_token` que está em uso é a velha, que:
- Usa `PASSWORD_RESET_TOKENS` — variável que **não existe** no arquivo (foi removida) → `NameError`
- Usa `time.time()` — mas `import time` foi removido → `NameError` adicional

**Resultado:** o sistema lança `NameError` ao tentar criar o token, e o e-mail nunca é enviado.

---

### 5. GET /redefinir-senha/\<token\> valida token e renderiza redefinir.html com o token?
**⚠️ PARCIALMENTE — a validação chama `_get_valid_reset_entry` que também está duplicada (veja Bug #2).**

A lógica da rota em si está correta: valida o token, retorna 302 para login se inválido, renderiza `redefinir.html` com `token=token` se válido.

---

### 6. redefinir.html tem action correto, method POST, campos 'password' e 'confirm_password'?
**✅ SIM.**  
- `action="{{ url_for('auth.password_reset', token=token) }}"` — correto.  
- `method="post"` — correto.  
- `<input name="password" ...>` e `<input name="confirm_password" ...>` — presentes.  
- Token CSRF presente.

---

### 7. POST /redefinir-senha/\<token\> valida token, senha, atualiza no banco, chama _delete_reset_token?
**❌ NÃO — a segunda versão da rota usa `PASSWORD_RESET_TOKENS.pop(token, None)` em vez de `_delete_reset_token(token)`.**

A primeira versão da rota `password_reset` (linha ~265):
- Valida token ✅  
- Valida senha ✅  
- Confirma usuário ainda existe ✅  
- Faz `UPDATE usuarios SET senha_hash` + `connection.commit()` ✅  
- Chama `_delete_reset_token(token)` ✅  

A segunda versão duplicada (linha ~430+):
- Faz tudo igual, exceto na última linha: chama `PASSWORD_RESET_TOKENS.pop(token, None)` — variável inexistente → `NameError`

---

### 8. _get_valid_reset_entry faz JOIN com usuarios e filtra por expira_em >= NOW()?
**❌ NÃO — a versão que prevalece no namespace usa dicionário em memória.**

Duas definições:

| Definição | Linha aprox. | Comportamento |
|-----------|-------------|---------------|
| Primeira (correta) | ~100 | Faz `SELECT … JOIN usuarios … WHERE prt.token = %s AND prt.expira_em >= NOW()` |
| Segunda (antiga, **substitui a primeira**) | ~345 | Busca em `PASSWORD_RESET_TOKENS.get(token)` → `NameError` |

---

### 9. _delete_reset_token remove o token do banco com commit?
**✅ SIM — a única definição desta função está correta.**  
Linha ~130: `DELETE FROM password_reset_tokens WHERE token = %s` + `connection.commit()`.  
Esta função **não foi duplicada** — é a única implementação e está correta.

---

### 10. send_password_reset_email funciona sem MAIL_SERVER (modo dev)?
**✅ SIM.**  
`email.py` linha ~22: `if not mail_server: logger.info("Password recovery link for %s: %s", to_email, reset_url); return`  
Sem MAIL_SERVER configurado, apenas loga o link e retorna — nenhuma exceção é levantada.

---

### 11. Problemas de import, nome de variável ou chamada de função?
**❌ SIM — múltiplos problemas críticos:**

| Problema | Arquivo | Linha aprox. | Descrição |
|----------|---------|-------------|-----------|
| `NameError: PASSWORD_RESET_TOKENS` | auth.py | ~330, ~450 | Variável removida, mas usada na segunda metade duplicada |
| `NameError: time` | auth.py | ~338 | `import time` foi removido, mas `time.time()` aparece na segunda versão de `_create_password_reset_token` |
| Rotas duplicadas (`/cadastro`, `/login`, `/recuperar-senha`, `/redefinir-senha/<token>`, `/logout`) | auth.py | ~360+ | Flask lança `AssertionError: View function mapping is overwriting an existing endpoint function` na inicialização |
| `_valid_email` definida duas vezes | auth.py | ~310 | Segunda definição sobrescreve a primeira (funcionalmente idênticas, mas indica duplicação) |
| `_verify_password` definida duas vezes | auth.py | ~318 | Idem |
| `_create_password_reset_token` assinatura incompatível | auth.py | ~326 | Segunda versão aceita `(user_id, email)`, primeira aceita apenas `(user_id)` — a segunda vence e quebra a chamada na primeira versão da rota |

---

## Diagnóstico Consolidado

O arquivo `auth.py` aparenta ter sido resultado de uma operação de edição que **colou o arquivo antigo inteiro abaixo do novo**, em vez de substituir o conteúdo. A estrutura atual é:

```
[linhas 1-310]   Versão NOVA  — funções de banco de dados, corretas
[linhas 311-fim] Versão ANTIGA — funções em memória, variáveis inexistentes, rotas duplicadas
```

O Flask **não consegue inicializar** com este arquivo porque registra a mesma rota duas vezes.

---

## Recomendações de Correção

### Correção principal (obrigatória)

**Remover toda a segunda metade duplicada de `auth.py`** — aproximadamente da linha 311 até o fim do arquivo. O conteúdo a ser removido começa logo após a primeira definição de `logout()` e inclui:

- Segunda definição de `_valid_email`
- Segunda definição de `_verify_password`
- Segunda definição de `_create_password_reset_token` (versão antiga com dicionário)
- Segunda definição de `_get_valid_reset_entry` (versão antiga com dicionário)
- Segunda definição de `register` (rota `/cadastro`)
- Segunda definição de `login` (rota `/login`)
- Segunda definição de `password_recovery_request` (rota `/recuperar-senha`)
- Segunda definição de `password_reset` (rota `/redefinir-senha/<token>`)
- Segunda definição de `logout` (rota `/logout`)

Após a remoção, o arquivo deve conter apenas as versões que usam banco de dados.

### Verificações após correção

1. `flask run` deve inicializar sem `AssertionError`.
2. POST `/recuperar-senha` com e-mail válido deve logar a URL no console (modo dev, sem MAIL_SERVER).
3. GET `/redefinir-senha/<token>` com token válido deve renderizar `redefinir.html`.
4. POST `/redefinir-senha/<token>` deve atualizar `senha_hash` no banco e redirecionar para login.

### Correção secundária (recomendada)

Garantir que a migração `002_password_reset_tokens.sql` foi executada no banco antes de testar — sem a tabela `password_reset_tokens`, o INSERT em `_create_password_reset_token` vai lançar `mysql.connector.errors.ProgrammingError`.

---

## Tabela-Resumo dos Problemas

| # | Arquivo | Linha aprox. | Severidade | Problema | Sugestão |
|---|---------|-------------|-----------|---------|---------|
| 1 | auth.py | 311–fim | **CRÍTICO** | Arquivo inteiro duplicado — Flask não inicializa | Remover segunda metade |
| 2 | auth.py | ~330 | **CRÍTICO** | `PASSWORD_RESET_TOKENS` não definido — `NameError` | Removida junto com a duplicata |
| 3 | auth.py | ~338 | **CRÍTICO** | `time.time()` sem `import time` — `NameError` | Removida junto com a duplicata |
| 4 | auth.py | ~450 | **CRÍTICO** | Segunda versão de `password_reset` usa `PASSWORD_RESET_TOKENS.pop()` em vez de `_delete_reset_token()` | Removida junto com a duplicata |
| 5 | auth.py | ~326 | Alto | Segunda `_create_password_reset_token` tem assinatura diferente `(user_id, email)` | Removida junto com a duplicata |
| 6 | migrations/ | — | Médio | Tabela `password_reset_tokens` precisa ser criada antes do deploy | Executar `002_password_reset_tokens.sql` |
