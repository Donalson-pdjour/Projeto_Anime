# Documentação técnica — Anime Mania

## 1. Identificação do projeto

| Item | Descrição |
|---|---|
| Nome | Anime Mania |
| Tipo | Aplicação web de conteúdo sobre animes |
| Idioma | Português do Brasil |
| Front-end | HTML, CSS, JavaScript e Bootstrap |
| Back-end planejado | Python com Flask |
| Banco de dados | MySQL |
| Público-alvo | Pessoas interessadas em animes, notícias e críticas |

O Flask é adotado nesta proposta por ser um framework Python simples e adequado
ao porte acadêmico do projeto. A aplicação deverá funcionar em diferentes
tamanhos de tela, incluindo celulares, tablets e computadores.

## 2. Objetivo

O Anime Mania reúne notícias, críticas e conteúdos informativos sobre animes.
Visitantes poderão navegar pelas publicações e consultar matérias, enquanto
usuários cadastrados poderão acessar sua conta. Uma área administrativa permitirá
gerenciar usuários e, futuramente, publicações.

## 3. Escopo funcional

### Funcionalidades para visitantes

- Visualizar a página inicial e publicações em destaque.
- Consultar a lista de notícias e abrir uma publicação.
- Ler conteúdos especiais, como a ordem cronológica dos animes de
  Cavaleiros do Zodíaco.
- Consultar críticas, como a de *Mortos de Amor*.
- Consultar informações sobre animes, como *InuYasha: Kanketsu-hen*.
- Criar uma conta, entrar no sistema e enviar uma mensagem de contato.

### Funcionalidades para usuários autenticados

- Encerrar a sessão com segurança.
- Visualizar e atualizar os dados básicos do próprio perfil.

### Funcionalidades administrativas

- Consultar a lista de usuários cadastrados.
- Gerenciar publicações, categorias e usuários, conforme as permissões
  atribuídas à conta administrativa.

## 4. Telas previstas

O projeto deve possuir pelo menos oito telas. A proposta contempla:

| Nº | Tela | Acesso | Descrição |
|---:|---|---|---|
| 1 | Início | Público | Destaques e atalhos para as publicações |
| 2 | Notícias | Público | Lista de notícias e lançamentos |
| 3 | Detalhe da publicação | Público | Conteúdo completo de uma notícia ou crítica |
| 4 | Ordem cronológica | Público | Matéria especial sobre Cavaleiros do Zodíaco |
| 5 | Detalhe de anime | Público | Conteúdo sobre títulos como InuYasha |
| 6 | Cadastro | Público | Formulário de criação de conta |
| 7 | Login | Público | Autenticação por e-mail e senha |
| 8 | Recuperação de senha | Público | Solicitação de redefinição de senha |
| 9 | Perfil | Usuário autenticado | Consulta e edição dos próprios dados |
| 10 | Contato | Público | Formulário de envio de mensagem |
| 11 | Administração de usuários | Administrador | Listagem e gerenciamento de usuários |
| 12 | Administração de publicações | Administrador | Cadastro, edição e remoção de matérias |

As telas 8, 9 e 12 são previstas para a arquitetura proposta; não devem ser
consideradas funcionalidades já implementadas no protótipo atual.

## 5. Arquitetura proposta

O navegador apresenta as páginas renderizadas com templates HTML e componentes
Bootstrap. As requisições são recebidas pelas rotas do Flask, que validam os
dados, aplicam as regras de negócio e acessam o MySQL por uma camada de
repositórios. As páginas públicas leem as publicações no banco, e as operações
de escrita ficam restritas às permissões necessárias.

```text
Navegador
   │ HTML, CSS, Bootstrap e formulários
   ▼
Aplicação Flask (rotas e regras de negócio)
   │ consultas parametrizadas
   ▼
MySQL
```

### Estrutura de diretórios sugerida (atualizada)

```text
projeto_anime/
├── app/
│   ├── __init__.py             # Factory da aplicação e registro de blueprints
│   ├── config.py               # Configurações da aplicação
│   ├── database.py             # Acesso ao banco de dados
│   ├── extensions.py           # Extensões compartilhadas do Flask
│   ├── migrate.py              # Execução das migrações SQL
│   ├── repositories/           # Camada disponível para repositórios
│   │   └── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py             # Rotas administrativas
│   │   ├── auth.py              # Cadastro, login e recuperação de senha
│   │   ├── profile.py           # Área do usuário autenticado
│   │   └── public.py            # Páginas públicas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── articles.py          # Serviços relacionados a artigos
│   │   ├── email.py             # Envio de e-mails
│   │   └── news.py              # Serviços relacionados a notícias
│   ├── static/
│   │   ├── css/
│   │   │   └── site.css
│   │   ├── images/              # Imagens e ícones da interface
│   │   └── js/                  # Scripts do navegador
│   ├── templates/
│   │   ├── base.html            # Estrutura compartilhada
│   │   ├── admin/               # Reservado para telas administrativas
│   │   ├── auth/
│   │   │   ├── cadastro/
│   │   │   │   └── cadastro.html
│   │   │   ├── login/
│   │   │   │   └── login.html
│   │   │   └── recuperar_senha/
│   │   │       ├── redefinir.html
│   │   │       └── solicitar.html
│   │   ├── profile/             # Reservado para telas do perfil
│   │   └── public/
│   │       ├── article.html
│   │       ├── index.html
│   │       └── news.html
├── migrations/
│   ├── 001_initial_schema.sql
│   └── 002_password_reset_tokens.sql
├── tests/
│   ├── test_app.py
│   └── test_auth.py
├── instance/                    # Arquivos locais da instância, não versionados
├── Regras/                      # Material de referência do projeto
│   └── PI - módulo 4.txt
├── .env.example                 # Modelo das variáveis de ambiente
├── .gitignore
├── requirements.txt             # Dependências Python
├── run.py                       # Ponto de entrada para execução local
└── DOCUMENTACAO_TECNICA.md
```

As pastas `app/repositories/`, `app/static/js/`, `app/templates/admin/` e
`app/templates/profile/` já existem, mas ainda não contêm implementações. Os
diretórios vazios são mantidos no projeto por arquivos `.gitkeep`. O arquivo
`.env` deve ser criado localmente a partir de `.env.example` e não deve ser
versionado.

Essa estrutura é uma referência de organização para a migração; ela não
corresponde à estrutura PHP que existe atualmente.

## 6. Rotas da aplicação

Cadastro (`/cadastro`), login (`/login`) e logout (`/logout`) estao
implementados na aplicacao Flask. O cadastro grava usuarios no MySQL com senha
protegida por Argon2; os formularios usam protecao CSRF. As demais rotas desta
tabela continuam previstas para etapas futuras.

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/` | Exibir a página inicial |
| GET | `/noticias` | Exibir notícias (requer login) |
| GET | `/publicacoes/<slug>` | Exibir uma publicação |
| GET | `/ordem-cronologica-cavaleiros` | Exibir a matéria especial |
| GET, POST | `/cadastro` | Exibir e processar cadastro |
| GET, POST | `/login` | Exibir e processar autenticação |
| POST | `/logout` | Encerrar a sessão |
| GET, POST | `/recuperar-senha` | Solicitar redefinição de senha |
| GET, POST | `/perfil` | Consultar e atualizar o perfil |
| GET, POST | `/contato` | Exibir e processar contato |
| GET | `/admin/usuarios` | Listar usuários para administradores |
| GET, POST | `/admin/publicacoes` | Listar e cadastrar publicações |

Rotas que alteram dados devem usar métodos HTTP apropriados, validar entrada e
proteger formulários contra CSRF.

## 7. Modelo inicial do banco de dados

O banco planejado é `anime_mania`, codificado em `utf8mb4`. As tabelas abaixo
representam um modelo inicial e podem ser refinadas conforme os requisitos.

### `usuarios`

- `id`: chave primária auto incremento.
- `nome`: nome de exibição.
- `email`: e-mail único usado na autenticação.
- `senha_hash`: hash seguro da senha; nunca armazenar a senha original.
- `papel`: tipo de conta, por exemplo `usuario` ou `admin`.
- `criado_em`: data e hora do cadastro.
- `ativo`: indica se a conta pode acessar o sistema.

### `categorias`

- `id`: chave primária.
- `nome`: nome único da categoria, como notícia, crítica ou guia.
- `slug`: identificador único usado em URLs.

### `publicacoes`

- `id`: chave primária.
- `categoria_id`: referência a `categorias.id`.
- `autor_id`: referência a `usuarios.id`, podendo ser nulo para conteúdo sem
  autoria associada a uma conta.
- `titulo`, `slug`, `resumo` e `conteudo`: informações editoriais.
- `imagem_capa`: caminho ou URL da imagem de capa.
- `status`: estado da publicação, como rascunho ou publicada.
- `publicado_em`, `criado_em` e `atualizado_em`: datas relevantes.

Relacionamentos iniciais:

- Uma categoria pode possuir várias publicações.
- Uma publicação pertence a uma categoria.
- Um usuário pode criar várias publicações.
- A tabela de usuários deve possuir índice único para o e-mail.
- A tabela de publicações deve possuir índice único para o slug.

O dump existente possui somente a tabela `usuarios`; categorias e publicações
precisam ser criadas para tornar as matérias administráveis pelo sistema. Dados
de demonstração antigos devem ser revisados e removidos ou substituídos antes
de compartilhar ou publicar o banco.

## 8. Tecnologias e dependências

- **Bootstrap:** grade responsiva, navegação, formulários e componentes de
  interface.
- **Python e Flask:** rotas web, validação e regras de negócio.
- **MySQL:** armazenamento persistente de contas e publicações.
- **Conector MySQL para Python:** comunicação entre a aplicação e o banco,
  utilizando consultas parametrizadas.
- **Jinja:** renderização de templates HTML no Flask.
- **JavaScript:** interações simples no navegador, sem substituir validações
  obrigatórias no servidor.

As versões das dependências deverão ser registradas em `requirements.txt`.
Credenciais do banco devem ser configuradas por variáveis de ambiente e não
incluídas no código-fonte.

## 9. Segurança e validação

- Armazenar senhas com algoritmo apropriado para senhas, como Argon2 ou bcrypt;
  não usar MD5 ou SHA simples.
- Usar consultas parametrizadas para reduzir risco de injeção SQL.
- Validar os dados no servidor, mesmo quando houver validação HTML/JavaScript.
- Escapar conteúdo inserido pelo usuário ao renderizar páginas.
- Restringir rotas administrativas a contas com papel de administrador.
- Proteger formulários contra CSRF e configurar cookies de sessão com atributos
  seguros em produção.
- Não exibir mensagens técnicas, senhas, segredos ou detalhes da conexão ao
  usuário final.
- Guardar configurações e credenciais fora do controle de versão.

## 10. Como executar a versão proposta

As instruções completas e atualizadas para Windows estão na seção 14:
preparação do ambiente virtual, dependências, `.env`, MySQL, migração, testes e
inicialização. Consulte essa seção para seguir o procedimento passo a passo.

1. Instalar Python compatível com as dependências e MySQL Server.
2. Na pasta do projeto, criar e ativar um ambiente virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Se o PowerShell bloquear a ativação, siga a orientação da seção 14 ou use
   diretamente o executável `.\.venv\Scripts\python.exe`.

3. Instalar as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

4. Copiar `.env.example` para `.env`, gerar um segredo para `FLASK_SECRET_KEY`
   e ajustar as variáveis `MYSQL_*` para a instalação local. O valor vazio de
   `MYSQL_PASSWORD` só é apropriado quando o usuário MySQL local realmente não
   possui senha. Não compartilhar nem versionar o arquivo `.env`.
5. Aplicar a migração inicial, que cria o banco novo `anime_mania` sem apagar
   nem modificar o banco legado `anime`:

   ```powershell
   py -m app.migrate
   ```

6. Iniciar o servidor Flask:

   ```powershell
   py run.py
   ```

7. Abrir `http://127.0.0.1:5000/`. O endpoint `http://127.0.0.1:5000/health`
   permite verificar se o servidor está respondendo.

O comando de migração precisa de um usuário MySQL com permissão para criar o
banco e as tabelas. Ele não foi executado durante esta etapa: o servidor local
recusou uma conexão de leitura sem senha para `root`, e as credenciais corretas
não foram fornecidas. O endpoint `/health` verifica apenas se a aplicação Flask
está ativa; ainda não verifica o banco.

## 11. Estado atual e próximos passos

### Estado observado

- O protótipo atual contém páginas `.php`, arquivos CSS, imagens e um dump SQL.
- A página inicial apresenta matérias e links para conteúdo sobre Cavaleiros do
  Zodíaco, notícias, críticas e InuYasha.
- Existem arquivos relacionados a cadastro, login, conexão com banco e consulta
  administrativa em PHP.
- O dump `usuarios.sql` define uma tabela de usuários no banco `anime`.
- A estrutura Flask inicial foi criada com fábrica de aplicação, blueprints,
  configuração por ambiente, proteção CSRF habilitada e endpoints de verificação.
- A aplicação agora possui um layout Jinja inicial com Bootstrap 5.3.3 e uma
  página inicial que apresenta cinco matérias e imagens copiadas do protótipo.
- A página original de notícias de lançamentos de 2023 foi migrada para
  `/noticias`, com as cinco seções existentes e vídeos incorporados pelo
  domínio sem cookies do YouTube.
- As matérias de ordem cronológica de Cavaleiros do Zodíaco, crítica de
  *Mortos de Amor*, InuYasha e Dicria estão disponíveis em
  `/publicacoes/<slug>`, a partir do catálogo em `app/services/articles.py`.
  Os cards da página inicial levam às respectivas matérias.
- Para esta primeira migração, partes dos textos longos foram condensadas e
  normalizadas para os templates; os PHP originais continuam preservados como
  fonte para revisar e completar a transcrição integral antes da migração para
  registros no banco. A crítica de *Mortos de Amor* foi revisada com base na
  fonte e recuperou os trechos condensados e a autoria/data; um par de
  parágrafos repetido no PHP foi mantido uma única vez.
- O conector MySQL recebe host, porta, banco, usuário e senha por configuração;
  a conexão real ainda não foi verificada e nenhuma tabela foi alterada.
- A migração `001_initial_schema.sql` e o comando `py -m app.migrate` foram
  preparados para criar as tabelas iniciais apenas no banco `anime_mania`; a
  migração não foi executada porque não há credenciais MySQL confirmadas.
- As dependências Python foram registradas em `requirements.txt`; as páginas
  PHP e os estilos existentes foram preservados.
- O conteúdo da página inicial e da notícia migrada ainda está em código
  Python, não em registros do banco de dados.

### Próximas etapas da migração

1. Criar e testar migrações MySQL para usuários, categorias e publicações, sem
   sobrescrever o banco legado.
2. Revisar e completar a transcrição integral das matérias no catálogo, usando
   os arquivos PHP originais como fonte.
3. Migrar as demais páginas públicas existentes para templates Jinja e
   completar as oito telas mínimas.
4. Implementar autorização administrativa, recuperação de senha e contato.
5. Migrar o conteúdo para registros de publicações.
6. Validar responsividade, acessibilidade básica e segurança antes de publicar.

## 12. Critérios de conclusão

- A aplicação abre e navega sem erros nas telas previstas.
- Pelo menos oito telas estão implementadas e utilizáveis em celular e desktop.
- Cadastro e autenticação persistem dados no MySQL.
- Senhas são armazenadas como hashes seguros.
- Uma pessoa sem permissão administrativa não acessa as rotas de administração.
- Publicações são exibidas a partir dos dados cadastrados no banco.
- Formulários apresentam validação e retorno claro em caso de sucesso ou erro.

## 13. Mapa atual do projeto

Este inventário descreve os arquivos presentes; a estrutura da seção 5 é uma
referência arquitetural e inclui componentes que ainda não foram implementados.

```text
projeto_anime/
|-- app/
|   |-- __init__.py                 fábrica Flask e registro de blueprints
|   |-- config.py                   configuração por ambiente
|   |-- database.py                 conexão MySQL
|   |-- extensions.py               proteção CSRF
|   |-- migrate.py                  aplicação da migração MySQL
|   |-- routes/
|   |   |-- public.py               início, notícias, artigos e health
|   |   |-- auth.py                 cadastro, login e logout
|   |   |-- profile.py              blueprint sem rotas implementadas
|   |   |-- admin.py                blueprint sem rotas implementadas
|   |   `-- __init__.py
|   |-- services/
|   |   |-- articles.py             catálogo de artigos
|   |   |-- news.py                 conteúdo da página de notícias
|   |   `-- __init__.py
|   |-- repositories/
|   |   `-- __init__.py             camada ainda sem repositórios
|   |-- templates/
|   |   |-- base.html               layout e navegação
|   |   |-- public/                 início, notícias e artigo
|   |   |-- auth/
|   |   |   |-- login/login.html
|   |   |   `-- cadastro/cadastro.html
|   |   |-- admin/                  reservado; sem telas
|   |   `-- profile/                reservado; sem telas
|   `-- static/
|       |-- css/site.css
|       |-- images/                  imagens e ícones
|       `-- js/                      reservado; sem scripts próprios
|-- migrations/001_initial_schema.sql
|-- tests/test_app.py
|-- tests/test_auth.py
|-- instance/.gitkeep                reservado para dados locais
|-- Regras/PI - módulo 4.txt         material de referência
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- run.py
`-- DOCUMENTACAO_TECNICA.md
```

Rotas Flask implementadas: `GET /`, `GET /noticias`,
`GET /publicacoes/<slug>`, `GET /health`, `GET|POST /login`,
`GET|POST /cadastro` e `POST /logout`. Recuperação de senha, contato, perfil e
administração permanecem pendentes. Os arquivos PHP antigos mencionados em
trechos históricos desta documentação não aparecem no inventário atual.

## 14. Comandos completos para executar no Windows

Esta seção detalha e atualiza as instruções resumidas da seção 10.

Abra o PowerShell e execute a partir da pasta que contém `projeto_anime`.
Troque o caminho de exemplo pelo local real da pasta:

```powershell
Set-Location "C:\caminho\para\projeto_anime"
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Cole o segredo gerado em `FLASK_SECRET_KEY` no `.env` e preencha
`MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER` e `MYSQL_PASSWORD`
com os dados do MySQL local. Salve o arquivo. Confirme que o serviço MySQL está
iniciado; para localizar seu nome no Windows:

```powershell
Get-Service *mysql*
```

Se necessário, inicie o serviço encontrado em um PowerShell com permissão:

```powershell
Start-Service NOME_DO_SERVICO
```

Com o banco acessível e as credenciais ajustadas, aplique a migração, rode os
testes e inicie o servidor:

```powershell
python -m app.migrate
python -m unittest discover -s tests -v
python run.py
```

Abra `http://127.0.0.1:5000/`. Para parar o servidor, pressione `Ctrl+C` no
PowerShell em que `python run.py` está rodando. `/health` verifica somente a
aplicação web, não a conexão MySQL.

Se a ativação do ambiente virtual for bloqueada pela política de execução,
libere scripts assinados localmente somente para a sessão atual do PowerShell
e tente ativar novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Essa alteração vale apenas para a janela atual do PowerShell e é descartada
quando ela for fechada. Se a política da organização impedir essa alteração,
não é necessário ativar o ambiente: use diretamente o Python do ambiente:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.migrate
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe run.py
```

## 15. Resultado da verificação

- Em 14/10/2026, `GET /`, `GET /health`, `GET /noticias`, `GET /login` e
  `GET /cadastro` responderam com HTTP 200 no servidor local.
- `python -m unittest discover -s tests -v`: 17 testes passaram.
- Os testes de cadastro e login simulam a conexão MySQL; não provam persistência
  num banco real. A migração e a conexão autenticada ao MySQL não foram
  verificadas nesta análise.
- Perfil, administração, recuperação de senha e contato ainda não estão
  implementados. A aplicação funciona nas páginas públicas e nos casos
  automatizados, mas não está completa nem certificada para produção.
