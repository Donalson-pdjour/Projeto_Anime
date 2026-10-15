from flask import Blueprint, abort, jsonify, render_template, url_for

from app.services.articles import ARTICLES, FEATURED_ARTICLE_SLUGS
from app.services.news import NEWS_ARTICLE


# Blueprint para as páginas públicas do site.
# Não requer autenticação — qualquer visitante pode acessar.
public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def index():
    """Renderiza a página inicial com os artigos em destaque.

    Monta a lista de artigos vindos de ARTICLES (dados estáticos) e adiciona
    a notícia principal do NEWS_ARTICLE ao final da lista de destaques.
    O template recebe um dicionário enriquecido com 'slug' e 'href' para
    facilitar a criação dos links sem lógica extra no HTML.
    """
    featured_articles = []

    # Itera sobre os slugs definidos em FEATURED_ARTICLE_SLUGS para preservar
    # a ordem de exibição na home, em vez de depender da ordem do dicionário.
    for slug in FEATURED_ARTICLE_SLUGS:
        article = ARTICLES[slug]
        featured_articles.append(
            {
                **article,           # Copia todos os campos do artigo (título, capa, etc.)
                "slug": slug,        # Adiciona o slug para referência
                "href": url_for("public.article_detail", slug=slug),  # URL do artigo
            }
        )

    # Adiciona a notícia principal como último card de destaque, com a rota de notícias.
    featured_articles.append(
        {
            "title": NEWS_ARTICLE["title"],
            "category": "Notícia",
            "cover": NEWS_ARTICLE["cover"],
            "cover_alt": NEWS_ARTICLE["cover_alt"],
            "href": url_for("public.news_list"),
        }
    )
    return render_template(
        "public/index.html",
        featured_articles=featured_articles,
    )


@public_bp.get("/noticias")
def news_list():
    """Exibe a página de notícias com o artigo principal de notícias."""
    return render_template(
        "public/news.html",
        article=NEWS_ARTICLE,
    )


@public_bp.get("/publicacoes/<slug>")
def article_detail(slug):
    """Exibe a página de detalhe de um artigo identificado pelo slug.

    O slug é a parte da URL que identifica o artigo de forma legível
    (ex: 'ordem-cronologica-cavaleiros-do-zodiaco').
    Se não existir nenhum artigo com aquele slug, retorna 404.
    """
    article = ARTICLES.get(slug)
    if article is None:
        abort(404)
    return render_template(
        "public/article.html",
        article=article,
    )


@public_bp.get("/health")
def health():
    """Endpoint de health check — retorna 200 OK com status 'ok'.

    Útil para balanceadores de carga e ferramentas de monitoramento
    confirmarem que a aplicação está rodando e respondendo.
    """
    return jsonify(status="ok")
