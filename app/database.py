import mysql.connector
from flask import current_app


def get_database_connection():
    """Abre e retorna uma nova conexão com o banco MySQL usando as configurações do Flask.

    Importante: o chamador é responsável por fechar a conexão depois de usar.
    O padrão recomendado é sempre usar um bloco try/finally:

        conn = get_database_connection()
        try:
            cursor = conn.cursor()
            # ... faz as queries ...
        finally:
            cursor.close()
            conn.close()

    Raises:
        RuntimeError: Se alguma configuração obrigatória (host, database, user)
                      estiver faltando, ou se a porta não for um número válido.
        mysql.connector.Error: Se o banco de dados recusar a conexão
                               (credenciais erradas, servidor fora do ar, etc.).
    """
    # Verifica se as configurações obrigatórias estão presentes antes de tentar conectar.
    # Isso gera uma mensagem de erro mais clara do que o erro nativo do mysql.connector.
    required_settings = ("MYSQL_HOST", "MYSQL_DATABASE", "MYSQL_USER")
    missing_settings = [
        setting
        for setting in required_settings
        if not current_app.config.get(setting)
    ]
    if missing_settings:
        settings = ", ".join(missing_settings)
        raise RuntimeError(f"Configuração MySQL ausente: {settings}.")

    # A porta vem como string do .env, então converte para int com tratamento de erro.
    try:
        port = int(current_app.config["MYSQL_PORT"])
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError("MYSQL_PORT deve ser um número inteiro válido.") from error

    return mysql.connector.connect(
        host=current_app.config["MYSQL_HOST"],
        port=port,
        database=current_app.config["MYSQL_DATABASE"],
        user=current_app.config["MYSQL_USER"],
        # Senha pode ser vazia (desenvolvimento local sem senha no MySQL).
        password=current_app.config.get("MYSQL_PASSWORD", ""),
        # utf8mb4 suporta emojis e caracteres especiais além do BMP do Unicode.
        charset="utf8mb4",
        use_unicode=True,
    )
