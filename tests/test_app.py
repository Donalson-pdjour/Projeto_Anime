import unittest
from unittest.mock import patch

from app import create_app
from app.database import get_database_connection
from app.services.articles import ARTICLES
from app.services.news import NEWS_ARTICLE


class AppSmokeTests(unittest.TestCase):
    def setUp(self):
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
            }
        )
        self.client = app.test_client()

    def test_home_page_responds(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Anime Mania", response.get_data(as_text=True))
        self.assertIn("bootstrap", response.get_data(as_text=True).lower())
        self.assertIn("Cavaleiros do Zodíaco", response.get_data(as_text=True))
        self.assertIn("/publicacoes/ordem-cronologica-cavaleiros-do-zodiaco", response.get_data(as_text=True))
        self.assertIn("/publicacoes/critica-mortos-de-amor", response.get_data(as_text=True))
        self.assertIn("/publicacoes/inuyasha-kanketsu-hen", response.get_data(as_text=True))
        self.assertIn("/publicacoes/mostra-dicria", response.get_data(as_text=True))
        self.assertEqual(response.get_data(as_text=True).count("article-card h-100"), 5)

    def test_migrated_article_pages_render_original_titles_and_content(self):
        expected_content = {
            "/publicacoes/ordem-cronologica-cavaleiros-do-zodiaco": (
                "The Lost Canvas",
                "Saga de Hades: Campos Elíseos",
                "Saint Seiya – Saintia Shô",
            ),
            "/publicacoes/critica-mortos-de-amor": (
                "Junji Ito",
                "Garoto da Encruzilhada",
                "Editora Pipoca &amp; Nanquim",
            ),
            "/publicacoes/inuyasha-kanketsu-hen": (
                "InuYasha: Kanketsu-hen",
                "Pluto TV Anime",
                "inuyasha-kanketsu-hen2.jpg",
            ),
            "/publicacoes/mostra-dicria": (
                "Mostra Dicria",
                "Mangateca Dicria",
                "Entrada gratuita",
            ),
        }

        for path, phrases in expected_content.items():
            with self.subTest(path=path):
                response = self.client.get(path)
                content = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_mortos_de_amor_restores_original_passages_and_byline(self):
        response = self.client.get("/publicacoes/critica-mortos-de-amor")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        for phrase in (
            "Postado por Gabriel Zoldick | set 6, 2023 |",
            "onde frequentemente um denso nevoeiro se concentra",
            "lançado este ano pela editora Pipoca e Nanquim",
            "De fato, às vezes até mesmo falta susto.",
            "A edição compila, portanto, seis histórias, somando dez capítulos",
        ):
            with self.subTest(phrase=phrase):
                    self.assertIn(phrase, content)

        self.assertEqual(
            content.count("A trama tem como protagonista o adolescente Ryusuke"),
            1,
        )

    def test_unknown_article_returns_not_found(self):
        response = self.client.get("/publicacoes/artigo-inexistente")

        self.assertEqual(response.status_code, 404)

    def test_homepage_static_assets_are_served(self):
        article_images = {
            article["cover"]
            for article in ARTICLES.values()
        }
        article_images.update(
            block["src"]
            for article in ARTICLES.values()
            for block in article["blocks"]
            if block["type"] == "image"
        )
        article_images.add(NEWS_ARTICLE["cover"])

        for asset in (
            "css/site.css",
            "images/anime-mania-logo_jpg_640.jpg",
            "images/favicon.svg",
        ) + tuple(f"images/{image}" for image in sorted(article_images)):
            with self.subTest(asset=asset):
                response = self.client.get(f"/static/{asset}")
                try:
                    self.assertEqual(response.status_code, 200)
                finally:
                    response.close()

    def test_news_page_renders_original_releases(self):
        response = self.client.get("/noticias")
        content = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Os lançamentos de animes mais aguardados de 2023", content)
        self.assertIn("Bungou Stray Dogs 4ª temporada", content)
        self.assertIn("Junji Ito: Histórias Macabras do Japão", content)
        self.assertEqual(content.count("youtube-nocookie.com/embed/"), 5)

    def test_health_endpoint_reports_ok(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_secret_key_is_required(self):
        with patch("app.Config.SECRET_KEY", None):
            with self.assertRaisesRegex(RuntimeError, "FLASK_SECRET_KEY"):
                create_app()

    @patch("app._ensure_tables")
    @patch("app.database.mysql.connector.connect")
    def test_database_connection_uses_configured_settings(
        self, connect, ensure_tables
    ):
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-only-secret",
                "MYSQL_HOST": "db.example.test",
                "MYSQL_PORT": "3307",
                "MYSQL_DATABASE": "anime_mania_test",
                "MYSQL_USER": "test_user",
                "MYSQL_PASSWORD": "test_password",
            }
        )

        with app.app_context():
            get_database_connection()

        connect.assert_called_once_with(
            host="db.example.test",
            port=3307,
            database="anime_mania_test",
            user="test_user",
            password="test_password",
            charset="utf8mb4",
            use_unicode=True,
        )

    def test_database_connection_rejects_missing_configuration(self):
        with patch("app._ensure_tables"):
            app = create_app(
                {
                    "TESTING": True,
                    "SECRET_KEY": "test-only-secret",
                    "MYSQL_USER": "",
                }
            )

        with app.app_context():
            with self.assertRaisesRegex(RuntimeError, "MYSQL_USER"):
                get_database_connection()


if __name__ == "__main__":
    unittest.main()
