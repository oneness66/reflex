"""Fourteen Worlds - Interactive Visualization of Vedic Cosmology."""

import reflex as rx
from .state import State
from .pages.index import index
from .pages.articles import articles_page, article_page
from .pages.media import media_page
from .pages.chapters import chapters_page
from .pages.photos import photos_page

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
)

# Register pages with routes
app.add_page(index, route="/", title="Fourteen Worlds - Vedic Cosmology")
app.add_page(articles_page, route="/articles", title="Articles - Fourteen Worlds")
app.add_page(media_page, route="/media", title="Media - Fourteen Worlds")
app.add_page(chapters_page, route="/chapters", title="Chapters - Fourteen Worlds")
app.add_page(photos_page, route="/photos", title="Photos - Fourteen Worlds")

# Dynamic route for articles
app.add_page(
    article_page, 
    route="/article/[filename]", 
    title="Article Viewer - Fourteen Worlds",
    on_load=State.load_article_from_url,
)
