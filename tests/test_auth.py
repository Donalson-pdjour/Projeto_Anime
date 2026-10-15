import unittest
from unittest.mock import MagicMock, patch

from argon2 import PasswordHasher

from app import create_app


class AuthTests(unittest.TestCase):
    def setUp(self):
        with patch("app._ensure_tables"):
            app = create_app(
                {
                    "TESTING": True,
                    "SECRET_KEY": "test-only-secret",
                    "WTF_CSRF_ENABLED": False,
                }
            )
        self.client = app.test_client()

    def make_database(self, user=None):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        cursor.fetchone.return_value = user
        return connection, cursor

    def test_login_and_registration_pages_render(self):
        login = self.client.get("/login")
        registration = self.client.get("/cadastro")

        self.assertEqual(login.status_code, 200)
        self.assertIn('name="csrf_token"', login.get_data(as_text=True))
        self.assertIn("Entrar", login.get_data(as_text=True))
        self.assertIn("Cadastre-se", login.get_data(as_text=True))
        self.assertEqual(registration.status_code, 200)
        self.assertIn('name="confirm_password"', registration.get_data(as_text=True))

    def test_logout_requires_post_and_csrf_token(self):
        with patch("app._ensure_tables"):
            app = create_app(
                {
                    "TESTING": True,
                    "SECRET_KEY": "test-only-secret",
                }
            )
        client = app.test_client()

        get_response = client.get("/logout")
        post_response = client.post("/logout")

        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(post_response.status_code, 400)

    @patch("app.routes.auth.get_database_connection")
    def test_registration_hashes_password_and_redirects_to_login(self, get_connection):
        connection, cursor = self.make_database()
        get_connection.return_value = connection

        response = self.client.post(
            "/cadastro",
            data={
                "name": "  Anime Fã  ",
                "email": "  Fã@Example.com ",
                "password": "senha-segura",
                "confirm_password": "senha-segura",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        insert = cursor.execute.call_args_list[1]
        values = insert.args[1]
        self.assertEqual(values[:2], ("Anime Fã", "fã@example.com"))
        self.assertNotEqual(values[2], "senha-segura")
        self.assertTrue(PasswordHasher().verify(values[2], "senha-segura"))
        connection.commit.assert_called_once()
        connection.close.assert_called_once()

    @patch("app.routes.auth.get_database_connection")
    def test_registration_rejects_duplicate_email(self, get_connection):
        connection, cursor = self.make_database(user={"id": 1})
        get_connection.return_value = connection

        response = self.client.post(
            "/cadastro",
            data={
                "name": "Anime Fã",
                "email": "existente@example.com",
                "password": "senha-segura",
                "confirm_password": "senha-segura",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(cursor.execute.call_count, 1)
        connection.commit.assert_not_called()
        connection.close.assert_called_once()

    @patch("app.routes.auth.get_database_connection")
    def test_registration_rejects_invalid_data_without_database_access(
        self, get_connection
    ):
        response = self.client.post(
            "/cadastro",
            data={
                "name": "Anime Fã",
                "email": "email-inválido",
                "password": "senha",
                "confirm_password": "diferente",
            },
        )

        self.assertEqual(response.status_code, 400)
        get_connection.assert_not_called()

    @patch("app.routes.auth.get_database_connection")
    def test_login_starts_session_and_logout_clears_it(self, get_connection):
        password_hash = PasswordHasher().hash("senha-segura")
        connection, _ = self.make_database(
            {
                "id": 12,
                "nome": "Anime Fã",
                "email": "fã@example.com",
                "senha_hash": password_hash,
                "papel": "usuario",
                "ativo": True,
            }
        )
        get_connection.return_value = connection

        response = self.client.post(
            "/login",
            data={"email": " FÃ@Example.com ", "password": "senha-segura"},
        )

        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as user_session:
            self.assertEqual(user_session["user_id"], 12)
            self.assertEqual(user_session["user_name"], "Anime Fã")
            self.assertEqual(user_session["user_role"], "usuario")

        response = self.client.post("/logout")

        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as user_session:
            self.assertNotIn("user_id", user_session)

    @patch("app.routes.auth.get_database_connection")
    def test_login_rejects_wrong_password_and_inactive_account(self, get_connection):
        active_connection, _ = self.make_database(
            {
                "id": 12,
                "nome": "Anime Fã",
                "email": "fã@example.com",
                "senha_hash": PasswordHasher().hash("senha-correta"),
                "papel": "usuario",
                "ativo": True,
            }
        )
        get_connection.return_value = active_connection

        wrong_password = self.client.post(
            "/login",
            data={"email": "fã@example.com", "password": "senha-incorreta"},
        )
        self.assertEqual(wrong_password.status_code, 401)

        inactive_connection, _ = self.make_database(
            {
                "id": 12,
                "nome": "Anime Fã",
                "email": "fã@example.com",
                "senha_hash": PasswordHasher().hash("senha-correta"),
                "papel": "usuario",
                "ativo": False,
            }
        )
        get_connection.return_value = inactive_connection

        inactive = self.client.post(
            "/login",
            data={"email": "fã@example.com", "password": "senha-correta"},
        )

        self.assertEqual(inactive.status_code, 401)
        with self.client.session_transaction() as user_session:
            self.assertNotIn("user_id", user_session)

    @patch("app.routes.auth.get_database_connection")
    @patch("app.routes.auth.send_password_reset_email")
    def test_password_recovery_request_sends_reset_email(self, send_email, get_connection):
        connection, cursor = self.make_database(
            {
                "id": 22,
                "nome": "Anime Fã",
                "email": "fã@example.com",
                "ativo": True,
            }
        )
        get_connection.return_value = connection

        response = self.client.post(
            "/recuperar-senha",
            data={"email": " FÃ@Example.com "},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        send_email.assert_called_once()
        self.assertIn("fã@example.com", send_email.call_args[0][0])
        self.assertIn("/redefinir-senha/", send_email.call_args[0][1])

    @patch("app.routes.auth.get_database_connection")
    def test_password_reset_updates_user_password(self, get_connection):
        token = "reset-token-test"
        token_connection, token_cursor = self.make_database(
            {"user_id": 88, "email": "fã@example.com"}
        )
        user_connection, user_cursor = self.make_database({"id": 88})
        delete_connection, delete_cursor = self.make_database()
        get_connection.side_effect = [
            token_connection,
            user_connection,
            delete_connection,
        ]

        response = self.client.post(
            f"/redefinir-senha/{token}",
            data={
                "password": "nova-senha-segura",
                "confirm_password": "nova-senha-segura",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")
        self.assertEqual(get_connection.call_count, 3)
        self.assertEqual(token_cursor.execute.call_count, 1)
        self.assertIn(
            "password_reset_tokens",
            token_cursor.execute.call_args.args[0],
        )
        self.assertEqual(token_cursor.execute.call_args.args[1], (token,))
        self.assertEqual(user_cursor.execute.call_count, 2)
        updated_hash = user_cursor.execute.call_args_list[1].args[1][0]
        self.assertNotEqual(updated_hash, "senha-antiga")
        self.assertTrue(PasswordHasher().verify(updated_hash, "nova-senha-segura"))
        self.assertIn(
            "DELETE FROM password_reset_tokens",
            delete_cursor.execute.call_args.args[0],
        )
        self.assertEqual(delete_cursor.execute.call_args.args[1], (token,))
        user_connection.commit.assert_called_once()
        delete_connection.commit.assert_called_once()
        for connection in (token_connection, user_connection, delete_connection):
            connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
