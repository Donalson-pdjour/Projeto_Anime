from collections.abc import Mapping
import logging

from flask import Flask

from app.config import Config
from app.extensions import csrf
from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.profile import profile_bp
from app.routes.public import public_bp

logger = logging.getLogger(__name__)


def _ensure_tables(app: Flask) -> None:
    """Cria as tabelas necessárias caso ainda não existam no banco.

    Usa CREATE TABLE IF NOT EXISTS para que a operação seja idempotente —
    pode ser chamada toda vez que o app sobe sem causar erros ou perda de dados.
    Isso elimina a necessidade de rodar scripts de migração manualmente para
    o fluxo de recuperação de senha funcionar.
    """
    import mysql.connector

    try:
        conn = mysql.connector.connect(
            host=app.config["MYSQL_HOST"],
            port=int(app.config["MYSQL_PORT"]),
            user=app.config["MYSQL_USER"],
            password=app.config.get("MYSQL_PASSWORD", ""),
            database=app.config["MYSQL_DATABASE"],
            charset="utf8mb4",
            use_unicode=True,
        )
        try:
            cursor = conn.cursor()
            try:
                # Tabela de tokens de recuperação de senha.
                # Cada usuário tem no máximo um token ativo por vez (UNIQUE em usuario_id).
                # Tokens expirados permanecem até serem consumidos ou limpos manualmente.
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS password_reset_tokens (
                        id          BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
                        usuario_id  BIGINT UNSIGNED  NOT NULL,
                        token       VARCHAR(128)     NOT NULL,
                        expira_em   DATETIME         NOT NULL,
                        criado_em   TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        PRIMARY KEY (id),
                        UNIQUE KEY uq_prt_token (token),
                        UNIQUE KEY uq_prt_usuario (usuario_id),
                        CONSTRAINT fk_prt_usuario
                            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                            ON UPDATE CASCADE ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                    """
                )
                conn.commit()
                logger.debug("Tabela 'password_reset_tokens' verificada/criada com sucesso.")
            finally:
                cursor.close()
        finally:
            conn.close()
    except mysql.connector.Error as exc:
        # Loga o erro mas não impede a aplicação de subir.
        # Se o banco estiver fora do ar, as rotas vão falhar individualmente
        # com mensagens de erro mais específicas.
        logger.warning("Não foi possível verificar tabelas do banco: %s", exc)


def create_app(test_config: Mapping[str, object] | None = None) -> Flask:
    """Cria e configura a aplicação Flask usando o padrão Application Factory.

    Usar uma factory (função que cria o app) em vez de um objeto global facilita:
    - Criar múltiplas instâncias com configurações diferentes nos testes.
    - Evitar imports circulares entre módulos que dependem do app.

    Args:
        test_config: Dicionário opcional com configurações que sobrescrevem
                     as do Config. Útil para passar um banco de dados em
                     memória ou desativar o CSRF durante os testes.

    Returns:
        A instância configurada do Flask pronta para receber requisições.
    """
    # instance_relative_config=True faz o Flask procurar arquivos de configuração
    # na pasta /instance, que fica fora do controle de versão (não vai pro git).
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Se uma configuração de teste for passada, ela sobrescreve os valores do Config.
    if test_config is not None:
        app.config.update(test_config)

    # A SECRET_KEY é obrigatória para o Flask assinar os cookies de sessão.
    # Se não estiver configurada, a aplicação não sobe — melhor falhar logo
    # do que ter problemas silenciosos de segurança em produção.
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "Configure FLASK_SECRET_KEY no ambiente antes de iniciar a aplicação."
        )

    # Ativa a proteção CSRF globalmente para todos os formulários da aplicação.
    csrf.init_app(app)

    # Registra os blueprints (módulos de rotas).
    # Cada blueprint agrupa rotas de uma área funcional diferente do site.
    app.register_blueprint(public_bp)   # Páginas públicas: home, artigos, notícias
    app.register_blueprint(auth_bp)     # Autenticação: login, cadastro, recuperar senha
    app.register_blueprint(profile_bp)  # Área do usuário logado
    app.register_blueprint(admin_bp)    # Painel administrativo

    # Garante que as tabelas extras (além das da migração inicial) existam.
    # Roda dentro do contexto da aplicação para ter acesso a app.config.
    with app.app_context():
        _ensure_tables(app)

    return app
