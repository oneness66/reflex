"""Fourteen Worlds - Interactive Visualization of Vedic Cosmology."""

import reflex as rx
from .state import State
from .pages.index import index
from .pages.articles import articles_page, article_page
from .pages.media import media_page
from .pages.chapters import chapters_page
from .pages.sb import sb_page
from .pages.sb_canto import sb_canto_page
from .pages.sb_chapter import sb_chapter_page
from .pages.sb_verse import sb_verse_page
from .pages.bg import bg_page
from .pages.bg_chapter import bg_chapter_page
from .pages.bg_verse import bg_verse_page
from .pages.photos import photos_page
from .pages.vedic_science import vedic_science_page, vedic_topic_page

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
)

# Register pages with routes
app.add_page(index, route="/", title="Fourteen Worlds - Vedic Cosmology")
app.add_page(articles_page, route="/articles", title="Articles - Fourteen Worlds")
app.add_page(media_page, route="/media", title="Media - Fourteen Worlds")
app.add_page(chapters_page, route="/library", title="Library - Fourteen Worlds")
app.add_page(sb_page, route="/library/sb", title="Śrīmad-Bhāgavatam - Fourteen Worlds")
app.add_page(sb_canto_page, route="/library/sb/[canto]", title="Canto - Fourteen Worlds")
app.add_page(sb_chapter_page, route="/library/sb/[canto]/[chapter]", title="Chapter - Fourteen Worlds")
app.add_page(sb_verse_page, route="/library/sb/[canto]/[chapter]/[verse]", title="Verse - Fourteen Worlds")
app.add_page(bg_page, route="/library/bg", title="Bhagavad-gītā As It Is - Fourteen Worlds")
app.add_page(bg_chapter_page, route="/library/bg/[chapter]", title="BG Chapter - Fourteen Worlds")
app.add_page(bg_verse_page, route="/library/bg/[chapter]/[verse]", title="BG Verse - Fourteen Worlds")
app.add_page(photos_page, route="/backtogodhead", title="Back To Godhead - Fourteen Worlds")
app.add_page(vedic_science_page, route="/vedic-science", title="Vedic Science - Fourteen Worlds")

# Dynamic route for Vedic Science topics
app.add_page(
    vedic_topic_page,
    route="/vedic-science/[topic]",
    title="Vedic Science Topic - Fourteen Worlds",
    on_load=State.load_vedic_topic,
)

# Dynamic route for articles
app.add_page(
    article_page, 
    route="/article/[filename]", 
    title="Article Viewer - Fourteen Worlds",
    on_load=State.load_article_from_url,
)
