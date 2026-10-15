import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para o os.environ,
# assim não precisamos configurar nada manualmente no servidor de desenvolvimento.
load_dotenv()


def _environment_flag(name: str, default: bool = False) -> bool:
    """Lê uma variável de ambiente e interpreta como booleano.

    Aceita os valores '1', 'true', 'yes' e 'on' (sem distinção de maiúsculas)
    como True. Qualquer outra coisa é False. Se a variável não existir, retorna
    o valor padrão informado.
    """
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Configurações centrais da aplicação Flask.

    Todos os valores sensíveis (chaves, senhas, hosts) vêm das variáveis de
    ambiente, nunca hardcoded aqui. Isso facilita trocar as credenciais entre
    ambientes (desenvolvimento, staging, produção) sem mudar o código.
    """

    # Chave secreta usada pelo Flask para assinar cookies de sessão.
    # OBRIGATÓRIA: a aplicação rejeita a inicialização se estiver vazia.
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # Ativa o modo de depuração do Flask (recarregamento automático, traceback no browser).
    # NUNCA deixe True em produção.
    DEBUG = _environment_flag("FLASK_DEBUG")

    # Impede que o JavaScript do navegador acesse o cookie de sessão (proteção contra XSS).
    SESSION_COOKIE_HTTPONLY = True

    # "Lax" significa que o cookie é enviado em navegações normais, mas não em
    # requisições cross-site iniciadas por terceiros (proteção básica contra CSRF).
    SESSION_COOKIE_SAMESITE = "Lax"

    # Em produção, ative para que o cookie só seja transmitido via HTTPS.
    SESSION_COOKIE_SECURE = _environment_flag("SESSION_COOKIE_SECURE")

    # --- Banco de dados MySQL ---
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "anime_mania")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

    # --- Configurações de e-mail (SMTP) ---
    # Se MAIL_SERVER não for definido, o serviço de e-mail cai em modo de log
    # e apenas registra os links no console (útil para desenvolvimento local).
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))

    # TLS (STARTTLS) é o padrão recomendado na porta 587.
    MAIL_USE_TLS = _environment_flag("MAIL_USE_TLS", True)

    # SSL direto na conexão (porta 465). Normalmente TLS ou SSL, nunca os dois.
    MAIL_USE_SSL = _environment_flag("MAIL_USE_SSL")

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "no-reply@anime-mania.local")
