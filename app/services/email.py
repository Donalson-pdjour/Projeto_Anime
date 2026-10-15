import html
import logging
import smtplib
from email.message import EmailMessage

from flask import current_app

# Logger nomeado com o módulo atual para facilitar filtrar nos logs da aplicação.
# Ex: para ver só os logs deste módulo, filtre por 'app.services.email'.
logger = logging.getLogger(__name__)

# Timeout em segundos para conexão e operações SMTP.
# Evita que a aplicação trave indefinidamente se o servidor de e-mail não responder.
_SMTP_TIMEOUT_SECONDS = 10


def send_password_reset_email(to_email: str, reset_url: str) -> None:
    """Envia um e-mail de recuperação de senha via SMTP.

    Funciona com qualquer servidor SMTP, incluindo o Gmail.
    Para usar o Gmail, configure as variáveis de ambiente:

        MAIL_SERVER=smtp.gmail.com
        MAIL_PORT=587
        MAIL_USE_TLS=true
        MAIL_USE_SSL=false
        MAIL_USERNAME=seu-email@gmail.com
        MAIL_PASSWORD=<senha-de-app-gerada-no-google>
        MAIL_DEFAULT_SENDER=seu-email@gmail.com

    IMPORTANTE — O Gmail exige uma "Senha de App", não a senha normal da conta.
    Para gerar uma:
      1. Acesse myaccount.google.com → Segurança → Verificação em duas etapas (ative se precisar).
      2. Em Segurança → "Senhas de app", crie uma senha para "Outro (nome personalizado)".
      3. Copie os 16 caracteres gerados e use como MAIL_PASSWORD no .env.

    Modo de desenvolvimento:
      Se MAIL_SERVER não estiver configurado, o link é apenas logado no console.
      Isso permite testar o fluxo completo sem precisar de um servidor SMTP real.

    Args:
        to_email:  Endereço de e-mail do destinatário.
        reset_url: URL completa do link de redefinição de senha (com token).

    Raises:
        RuntimeError: Se as credenciais SMTP estiverem incompletas (username sem password).
        smtplib.SMTPAuthenticationError: Se o Gmail rejeitar as credenciais.
            Causa mais comum: usar a senha normal da conta em vez da Senha de App.
        OSError: Para erros de rede (timeout, host inacessível, etc.).
    """
    mail_server = current_app.config.get("MAIL_SERVER")
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")

    # --- Modo de desenvolvimento: sem servidor OU sem credenciais, só loga o link ---
    # Isso cobre dois casos comuns:
    #   1. MAIL_SERVER vazio (desenvolvimento local sem e-mail configurado)
    #   2. MAIL_SERVER preenchido mas MAIL_USERNAME/MAIL_PASSWORD vazios
    #      (variáveis adicionadas ao .env mas ainda não preenchidas)
    if not mail_server or not username or not password:
        logger.info(
            "MODO DEV — Link de recuperação de senha para %s: %s",
            to_email,
            reset_url,
        )
        return

    # --- Monta a mensagem de e-mail ---
    sender = current_app.config.get("MAIL_DEFAULT_SENDER", "no-reply@anime-mania.local")

    message = EmailMessage()
    message["Subject"] = "Anime Mania — redefinição de senha"
    message["From"] = sender
    message["To"] = to_email

    # Versão em texto puro: fallback para clientes sem suporte a HTML.
    message.set_content(
        "Você solicitou a redefinição de senha da sua conta no Anime Mania.\n\n"
        "Para criar uma nova senha, acesse o link abaixo:\n\n"
        f"{reset_url}\n\n"
        "Este link expira em 1 hora.\n\n"
        "Se você não fez essa solicitação, ignore este e-mail. Sua senha permanece a mesma."
    )

    # Versão HTML: exibida pela maioria dos clientes de e-mail modernos.
    # html.escape() garante que caracteres especiais na URL (ex: '&' em query strings)
    # não quebrem o HTML nem causem injeção de markup.
    safe_url = html.escape(reset_url)
    message.add_alternative(
        f"""<html>
<body style="font-family: Arial, sans-serif; color: #222; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h2 style="color: #e6a817;">Anime Mania — Redefinição de senha</h2>
  <p>Você solicitou a redefinição de senha da sua conta.</p>
  <p>Clique no botão abaixo para criar uma nova senha:</p>
  <p style="text-align: center; margin: 32px 0;">
    <a href="{safe_url}"
       style="background-color: #e6a817; color: #000; padding: 12px 28px;
              text-decoration: none; border-radius: 4px; font-weight: bold;">
      Redefinir minha senha
    </a>
  </p>
  <p style="font-size: 0.85em; color: #666;">
    Se o botão não funcionar, copie e cole este link no navegador:<br>
    <a href="{safe_url}" style="color: #e6a817;">{safe_url}</a>
  </p>
  <p style="font-size: 0.85em; color: #666;">
    Este link expira em <strong>1 hora</strong>.<br>
    Se você não solicitou essa alteração, ignore este e-mail.
  </p>
</body>
</html>""",
        subtype="html",
    )

    # --- Lê configurações de conexão SMTP ---
    port = int(current_app.config.get("MAIL_PORT", 587))
    use_tls = bool(current_app.config.get("MAIL_USE_TLS", True))
    use_ssl = bool(current_app.config.get("MAIL_USE_SSL", False))

    try:
        if use_ssl:
            # Conexão SSL direta — porta 465 normalmente.
            with smtplib.SMTP_SSL(mail_server, port, timeout=_SMTP_TIMEOUT_SECONDS) as server:
                if username and password:
                    server.login(username, password)
                server.send_message(message)
            return

        # Conexão padrão com upgrade para TLS via STARTTLS — porta 587 (Gmail e maioria dos provedores).
        with smtplib.SMTP(mail_server, port, timeout=_SMTP_TIMEOUT_SECONDS) as server:
            if use_tls:
                server.starttls()  # Faz o upgrade da conexão para TLS antes do login.
            if username and password:
                server.login(username, password)
            server.send_message(message)

    except smtplib.SMTPAuthenticationError:
        # Captura separadamente para dar uma mensagem mais útil sobre o Gmail.
        logger.exception(
            "Falha de autenticação SMTP ao enviar para %s. "
            "Se estiver usando o Gmail, confirme que MAIL_PASSWORD é uma Senha de App "
            "(não a senha normal da conta Google). "
            "Gere uma em: myaccount.google.com → Segurança → Senhas de app.",
            to_email,
        )
        raise
    except OSError:
        # Erros de rede: host inacessível, timeout, conexão recusada, etc.
        logger.exception("Erro de rede ao enviar e-mail de recuperação para %s", to_email)
        raise
