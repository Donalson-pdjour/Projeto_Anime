from flask_wtf.csrf import CSRFProtect


# Instância global do CSRFProtect.
# Ela é inicializada com o app Flask dentro de create_app() (app/__init__.py),
# seguindo o padrão "Application Factory" do Flask.
# Isso protege automaticamente todos os formulários POST contra ataques CSRF.
csrf = CSRFProtect()
