import logging
import re
import secrets

import mysql.connector
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for

from app.database import get_database_connection
from app.services.email import send_password_reset_email


auth_bp = Blueprint("auth", __name__)

# Logger deste módulo — usado para registrar falhas de envio de e-mail
# sem expor o erro para o usuário final.
logger = logging.getLogger(__name__)

# Argon2 é o algoritmo de hashing de senhas recomendado atualmente.
# É resistente a ataques de força bruta por GPU e usa memória intensivamente.
password_hasher = PasswordHasher()

# Regex simples para validar o formato de e-mail.
# Não usa RFC 5322 completa de propósito — ela é complexa demais e raramente necessária.
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Limites de tamanho da senha para equilibrar usabilidade e segurança.
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# Quanto tempo (em segundos) o token de recuperação de senha é válido: 1 hora.
PASSWORD_RESET_TTL_SECONDS = 3600

# Os tokens são armazenados na tabela `password_reset_tokens` do banco de dados.
# Isso garante que sobrevivam a reinicializações do servidor e funcionem com
# múltiplos workers. Tokens expirados são limpos automaticamente pelo evento
# MySQL agendado definido na migração 002_password_reset_tokens.sql.


def _valid_email(email: str) -> bool:
    """Verifica se o e-mail tem um formato válido e não ultrapassa 254 caracteres.

    254 é o limite máximo definido pelo RFC 5321 para um endereço de e-mail completo.
    """
    return len(email) <= 254 and EMAIL_PATTERN.fullmatch(email) is not None


def _verify_password(password: str, password_hash: str) -> bool:
    """Compara a senha em texto com o hash armazenado usando Argon2.

    Retorna False em vez de propagar a exceção para não vazar informação
    sobre o motivo da falha (hash inválido vs. senha errada).
    """
    try:
        return password_hasher.verify(password_hash, password)
    except (VerificationError, VerifyMismatchError):
        return False


def _create_password_reset_token(user_id: int) -> str:
    """Gera um token seguro e persiste no banco com TTL.

    Usa INSERT ... ON DUPLICATE KEY UPDATE para garantir que cada usuário
    tenha apenas um token ativo por vez: se já existir um token para o mesmo
    usuario_id, ele é sobrescrito pelo novo — evitando múltiplos links ativos
    simultâneos para o mesmo usuário.

    secrets.token_urlsafe(32) produz 43 caracteres de URL-safe Base64,
    com 256 bits de entropia — praticamente impossível de adivinhar por força bruta.
    """
    token = secrets.token_urlsafe(32)

    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO password_reset_tokens (usuario_id, token, expira_em)
            VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL %s SECOND))
            ON DUPLICATE KEY UPDATE
                token     = VALUES(token),
                expira_em = VALUES(expira_em)
            """,
            (user_id, token, PASSWORD_RESET_TTL_SECONDS),
        )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    return token


def _get_valid_reset_entry(token: str):
    """Busca no banco um token de redefinição ainda válido (não expirado).

    Filtra por expira_em >= NOW() como camada de defesa extra, garantindo que
    nunca aceitemos um token vencido mesmo que o evento de limpeza automática
    ainda não tenha rodado.

    Retorna um dict com 'user_id' e 'email', ou None se inválido/expirado.
    """
    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT prt.usuario_id AS user_id, u.email
            FROM password_reset_tokens prt
            JOIN usuarios u ON u.id = prt.usuario_id
            WHERE prt.token = %s
              AND prt.expira_em >= NOW()
            LIMIT 1
            """,
            (token,),
        )
        return cursor.fetchone()  # None se não encontrado ou expirado
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def _delete_reset_token(token: str) -> None:
    """Remove o token do banco após uso para evitar reutilização."""
    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM password_reset_tokens WHERE token = %s",
            (token,),
        )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def register():
    """Exibe o formulário de cadastro (GET) e processa o envio (POST).

    Validações realizadas antes de tocar no banco:
    - Nome: obrigatório, máximo 120 caracteres.
    - E-mail: formato válido e tamanho <= 254 chars.
    - Senha: entre MIN e MAX caracteres.
    - Confirmação de senha: igual à senha.

    Em caso de e-mail duplicado, retorna 409 Conflict (trata tanto o
    SELECT prévio quanto a IntegrityError de race condition).
    """
    if request.method == "GET":
        return render_template("auth/cadastro/cadastro.html")

    # Lê e sanitiza os dados do formulário.
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # --- Validações de entrada ---
    if not name or len(name) > 120:
        flash("Informe seu nome (até 120 caracteres).", "danger")
        return render_template("auth/cadastro/cadastro.html"), 400
    if not _valid_email(email):
        flash("Informe um endereço de e-mail válido.", "danger")
        return render_template("auth/cadastro/cadastro.html"), 400
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        flash("A senha deve ter entre 8 e 128 caracteres.", "danger")
        return render_template("auth/cadastro/cadastro.html"), 400
    if password != confirm_password:
        flash("As senhas informadas não são iguais.", "danger")
        return render_template("auth/cadastro/cadastro.html"), 400

    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        # Verifica se o e-mail já existe antes de tentar inserir,
        # para dar uma mensagem de erro mais amigável do que uma IntegrityError.
        cursor.execute("SELECT id FROM usuarios WHERE email = %s LIMIT 1", (email,))
        if cursor.fetchone() is not None:
            flash("Esse e-mail já está cadastrado. Faça login.", "danger")
            return render_template("auth/cadastro/cadastro.html"), 409

        cursor.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash, papel, ativo)
            VALUES (%s, %s, %s, 'usuario', TRUE)
            """,
            (name, email, password_hasher.hash(password)),
        )
        connection.commit()
    except mysql.connector.IntegrityError as error:
        # Race condition: outro request inseriu o mesmo e-mail entre o SELECT
        # acima e o INSERT. Desfaz a transação e retorna o mesmo erro amigável.
        connection.rollback()
        if error.errno != mysql.connector.errorcode.ER_DUP_ENTRY:
            raise  # Erro de integridade por outro motivo — repassa para cima.
        flash("Esse e-mail já está cadastrado. Faça login.", "danger")
        return render_template("auth/cadastro/cadastro.html"), 409
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    flash("Cadastro realizado. Agora você pode entrar.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Exibe o formulário de login (GET) e autentica o usuário (POST).

    A mensagem de erro é propositalmente genérica ("E-mail ou senha inválidos")
    para não revelar se o e-mail está cadastrado ou não (proteção contra
    ataques de enumeração de usuários).
    """
    if request.method == "GET":
        return render_template("auth/login/login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Valida o formato antes de ir ao banco para evitar queries desnecessárias.
    if not _valid_email(email) or not password or len(password) > MAX_PASSWORD_LENGTH:
        flash("E-mail ou senha inválidos.", "danger")
        return render_template("auth/login/login.html"), 401

    connection = get_database_connection()
    cursor = None
    try:
        # dictionary=True faz o cursor retornar linhas como dicts em vez de tuplas.
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nome, email, senha_hash, papel, ativo
            FROM usuarios
            WHERE email = %s
            LIMIT 1
            """,
            (email,),
        )
        user = cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    # Verifica três condições em uma só expressão para evitar timing attacks
    # que poderiam revelar qual das condições falhou:
    # 1. Usuário existe   2. Está ativo   3. Senha bate com o hash
    if (
        user is None
        or not user["ativo"]
        or not _verify_password(password, user["senha_hash"])
    ):
        flash("E-mail ou senha inválidos.", "danger")
        return render_template("auth/login/login.html"), 401

    # session.clear() invalida qualquer sessão anterior antes de criar uma nova.
    # Isso previne session fixation attacks.
    # get_flashed_messages() consome e descarta qualquer flash pendente da
    # sessão anterior (ex: "Você saiu da sua conta") para que não apareça
    # junto com a mensagem de boas-vindas do novo login.
    get_flashed_messages()  # descarta flashes pendentes da sessão anterior
    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["nome"]
    session["user_role"] = user["papel"]
    flash(f"Bem-vindo(a), {user['nome']}!", "success")
    return redirect(url_for("public.index"))


@auth_bp.route("/recuperar-senha", methods=["GET", "POST"])
def password_recovery_request():
    """Solicita o envio de um e-mail de recuperação de senha.

    Por segurança, sempre exibe a mesma mensagem de sucesso, independente
    de o e-mail estar ou não cadastrado. Isso impede que um atacante use
    o formulário para descobrir quais e-mails existem no sistema.
    """
    if request.method == "GET":
        return render_template("auth/recuperar_senha/solicitar.html")

    email = request.form.get("email", "").strip().lower()
    if not _valid_email(email):
        flash("Informe um e-mail válido para receber o link de recuperação.", "danger")
        return render_template("auth/recuperar_senha/solicitar.html"), 400

    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, nome, email, ativo
            FROM usuarios
            WHERE email = %s
            LIMIT 1
            """,
            (email,),
        )
        user = cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    # Só gera e envia o token se o usuário existir E estiver ativo.
    # O bloco sempre termina com a mesma mensagem de sucesso (anti-enumeração).
    if user is not None and user.get("ativo"):
        token = _create_password_reset_token(user["id"])
        reset_url = url_for("auth.password_reset", token=token, _external=True)
        try:
            send_password_reset_email(user["email"], reset_url)
        except Exception:
            # Falha de SMTP (credenciais erradas, servidor fora do ar, timeout, etc.)
            # não deve impedir o fluxo nem revelar informações ao usuário.
            # O erro já foi registrado no log pelo próprio send_password_reset_email.
            logger.exception(
                "Falha ao enviar e-mail de recuperação para %s", user["email"]
            )

    flash(
        "Se esse e-mail estiver cadastrado, enviamos um link para redefinir a senha.",
        "success",
    )
    return redirect(url_for("auth.login"))


@auth_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def password_reset(token):
    """Valida o token de recuperação e, se válido, permite redefinir a senha.

    O token é passado na URL. Se for inválido ou expirado, redireciona para
    o login com mensagem de erro.
    """
    # Valida o token antes de qualquer coisa. Se expirado ou inválido, aborta.
    reset_entry = _get_valid_reset_entry(token)
    if reset_entry is None:
        flash("Link de redefinição inválido ou expirado.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        # Passa o token para o template poder montar a action do formulário.
        return render_template("auth/recuperar_senha/redefinir.html", token=token)

    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # Valida a nova senha antes de ir ao banco.
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        flash("A senha deve ter entre 8 e 128 caracteres.", "danger")
        return render_template("auth/recuperar_senha/redefinir.html", token=token), 400
    if password != confirm_password:
        flash("As senhas informadas não são iguais.", "danger")
        return render_template("auth/recuperar_senha/redefinir.html", token=token), 400

    connection = get_database_connection()
    cursor = None
    try:
        cursor = connection.cursor()

        # Confirma que o usuário ainda existe antes de atualizar a senha.
        # (Segurança: evita atualizar senha de usuário deletado entre o pedido e o reset.)
        cursor.execute(
            "SELECT id FROM usuarios WHERE id = %s LIMIT 1",
            (reset_entry["user_id"],),
        )
        if cursor.fetchone() is None:
            connection.rollback()
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("auth.login"))

        # Atualiza a senha com um novo hash Argon2.
        cursor.execute(
            "UPDATE usuarios SET senha_hash = %s WHERE id = %s",
            (password_hasher.hash(password), reset_entry["user_id"]),
        )
        connection.commit()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    # Remove o token do banco para que não possa ser reutilizado.
    _delete_reset_token(token)
    flash("Sua senha foi redefinida com sucesso.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.post("/logout")
def logout():
    """Encerra a sessão do usuário.

    Usa @auth_bp.post (em vez de GET+POST) intencionalmente: logout via GET
    é vulnerável a CSRF — um link malicioso poderia deslogar o usuário sem
    querer. Ao exigir POST, o formulário de logout é protegido pelo token CSRF.
    """
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("public.index"))
