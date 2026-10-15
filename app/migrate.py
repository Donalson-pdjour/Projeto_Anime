from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# Garante que o .env seja carregado antes de importar Config,
# pois este script pode ser executado diretamente via "python -m app.migrate".
load_dotenv()

from app.config import Config


# Pasta onde ficam todos os arquivos de migração SQL.
MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "migrations"

# Lista ordenada das migrações que devem ser aplicadas.
# A ordem importa: migrações posteriores podem depender de tabelas criadas antes.
MIGRATION_FILES = [
    MIGRATIONS_DIR / "001_initial_schema.sql",
    MIGRATIONS_DIR / "002_password_reset_tokens.sql",
]


def _run_migration_file(connection: mysql.connector.MySQLConnection, path: Path) -> None:
    """Executa todos os statements SQL de um arquivo na conexão fornecida.

    O arquivo é dividido por ';' para rodar cada instrução separadamente,
    pois o mysql.connector não aceita múltiplos statements em uma única chamada.

    CORREÇÃO BUG 4: adicionado connection.commit() após executar todos os
    statements DML do arquivo. Statements DDL (CREATE, ALTER) recebem commit
    implícito no MySQL, mas INSERT/UPDATE dentro de migrações precisam de commit
    explícito para serem persistidos.
    """
    sql_script = path.read_text(encoding="utf-8")

    # Divide pelo ponto-e-vírgula e descarta linhas vazias resultantes.
    statements = [s.strip() for s in sql_script.split(";") if s.strip()]

    cursor = connection.cursor()
    try:
        for statement in statements:
            cursor.execute(statement)
        # FIX BUG 4: commit explícito para garantir que statements DML sejam salvos.
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


def apply_migrations() -> None:
    """Abre uma conexão e aplica todas as migrações pendentes em ordem.

    A conexão não especifica banco de dados inicialmente porque a primeira
    migração é quem cria o banco com CREATE DATABASE IF NOT EXISTS.
    """
    connection = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        port=int(Config.MYSQL_PORT),
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset="utf8mb4",
        use_unicode=True,
    )
    try:
        for migration_file in MIGRATION_FILES:
            print(f"  → Aplicando {migration_file.name}...")
            _run_migration_file(connection, migration_file)
            print(f"    ✓ {migration_file.name} concluída.")
    finally:
        # Garante que a conexão seja fechada mesmo se uma migração falhar.
        connection.close()


# Mantém o nome antigo como alias para não quebrar código que já chame apply_initial_migration().
def apply_initial_migration() -> None:
    """Alias mantido para compatibilidade. Prefira apply_migrations()."""
    apply_migrations()


if __name__ == "__main__":
    apply_migrations()
    print("Todas as migrações aplicadas ao banco anime_mania.")
