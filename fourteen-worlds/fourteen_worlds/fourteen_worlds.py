"""Fourteen Worlds - Interactive Visualization of Vedic Cosmology."""

import reflex as rx
import re
from pathlib import Path
from rxconfig import config
from .data.worlds_data import (
    WORLDS_DATA, 
    get_world_by_id,
    LOKA_TRAYA_INFO,
    LOTUS_COSMOLOGY,
    BILA_SVARGA_INFO,
)


# Path to bhu-mandala HTML files
BHU_MANDALA_PATH = Path(__file__).parent.parent / "assets" / "bhu-mandala"


class State(rx.State):
    """The app state."""
    selected_world_id: int = 0
    show_detail: bool = False
    # current_page removed in favor of URL routing
    
    # For dynamic article routing
    article_content: str = ""
    article_name: str = ""
    
    def select_world(self, world_id: int):
        """Select a world to view details."""
        self.selected_world_id = world_id
        self.show_detail = True
    
    def close_detail(self):
        """Close the detail view."""
        self.show_detail = False
        self.selected_world_id = 0
    
    def load_article_content(self, filename: str):
        """Load article content based on the current article_id from URL."""
        if not filename:
            return
            
        # Ensure filename ends with .html if not present (though links should include it)
        if not filename.endswith('.html'):
            filename += '.html'
            
        article_path = BHU_MANDALA_PATH / filename
        if article_path.exists():
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Remove conflicting elements
                # Remove the background stretch div which obscures content
                content = re.sub(r'<div id="bg-stretch">.*?</div>', '', content, flags=re.DOTALL)
                # Remove original header and nav as we use our own
                content = re.sub(r'<div id="header">.*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<ul id="nav">.*?</ul>', '', content, flags=re.DOTALL)
                
                # Fix relative paths to work with Reflex asset serving
                content = content.replace('src="img/', 'src="/bhu-mandala/img/')
                content = content.replace('href="img/', 'href="/bhu-mandala/img/')
                content = content.replace('src="fotos/', 'src="/bhu-mandala/fotos/')
                content = content.replace('href="fotos/', 'href="/bhu-mandala/fotos/')
                content = content.replace('href="css/', 'href="/bhu-mandala/css/')
                content = content.replace('src="js/', 'src="/bhu-mandala/js/')
                # Fix links to other articles to use the new route structure
                content = content.replace('href="jambudvipa', 'href="/article/jambudvipa')
                content = content.replace('href="articles-overview.html"', 'href="/articles"')
                content = content.replace('href="chapter-index.html"', 'href="/chapters"')
                
                # Inject styles to ensure readability (fix for missing background images)
                style_override = """
                <style>
                .box .content { background: white !important; }
                body { background: none !important; }
                </style>
                """
                content = content.replace('</head>', style_override + '</head>')
                
                self.article_content = content
                self.article_name = filename.replace('.html', '').replace('-', ' ').title()
        else:
            self.article_content = f"<h1>Article not found: {filename}</h1>"

    def load_article_from_url(self):
        """Load article content using the filename from the URL router params."""
        args = self.router.page.params
        filename = args.get("filename", "")
        if filename:
            self.load_article_content(filename)

    
    @rx.var
    def selected_world(self) -> dict:
        """Get the currently selected world data."""
        if self.selected_world_id > 0:
            return get_world_by_id(self.selected_world_id)
        return {}


def world_card(world: dict) -> rx.Component:
    """Create a world card component."""
    return rx.box(
        rx.vstack(
            rx.heading(
                world["name"],
                size="6",
                color="white",
                weight="bold",
            ),
            rx.text(
                world["alt_name"],
                size="2",
                color="rgba(255, 255, 255, 0.8)",
                font_style="italic",
            ),
            rx.text(
                world["description"],
                size="2",
                color="rgba(255, 255, 255, 0.9)",
                text_align="center",
            ),
            spacing="2",
            align="center",
        ),
        on_click=lambda: State.select_world(world["id"]),
        background=f"linear-gradient(135deg, {world['color']} 0%, {world['color']}dd 100%)",
        padding="1.5rem",
        border_radius="12px",
        cursor="pointer",
        transition="all 0.3s ease",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
        _hover={
            "transform": "translateY(-5px) scale(1.02)",
            "box_shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
        },
        width="100%",
        max_width="400px",
    )


def detail_modal() -> rx.Component:
    """Create a modal to show world details."""
    return rx.cond(
        State.show_detail,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            State.selected_world["name"],
                            size="8",
                            color=State.selected_world["color"],
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=State.close_detail,
                            variant="ghost",
                            size="3",
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.text(
                        State.selected_world["alt_name"],
                        size="4",
                        color="gray",
                        font_style="italic",
                    ),
                    rx.divider(),
                    rx.heading("Description", size="5", margin_top="1rem"),
                    rx.text(
                        State.selected_world["description"],
                        size="3",
                        line_height="1.6",
                    ),
                    rx.heading("Details", size="5", margin_top="1.5rem"),
                    rx.text(
                        State.selected_world["details"],
                        size="3",
                        line_height="1.6",
                    ),
                    rx.cond(
                        State.selected_world.get("reference", "") != "",
                        rx.box(
                            rx.text(
                                "Scriptural Reference: ",
                                State.selected_world.get("reference", ""),
                                size="2",
                                color="gray",
                                font_style="italic",
                                margin_top="1rem",
                            ),
                        ),
                    ),
                    rx.button(
                        "Close",
                        on_click=State.close_detail,
                        margin_top="2rem",
                        size="3",
                        color_scheme="blue",
                    ),
                    spacing="3",
                    align="start",
                ),
                background="white",
                padding="2rem",
                border_radius="16px",
                max_width="600px",
                width="90%",
                max_height="80vh",
                overflow_y="auto",
                box_shadow="0 20px 60px rgba(0, 0, 0, 0.3)",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.5)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="1000",
            backdrop_filter="blur(4px)",
        ),
    )


def classic_header() -> rx.Component:
    """Classic styled header with navigation menu matching bhu-mandala format."""
    return rx.vstack(
        # Header image/title
        rx.box(
            rx.link(
                rx.heading(
                    "Sailing to the Fourteen Worlds",
                    size="9",
                    color="#000099",
                    font_family="'Times New Roman', serif",
                    font_style="italic",
                    font_weight="normal",
                    text_align="center",
                    text_shadow="2px 2px 4px rgba(255, 255, 255, 0.8)",
                ),
                href="/",
                text_decoration="none",
                _hover={"opacity": "0.8"},
            ),
            padding="2rem 0 1rem 0",
            background="rgba(255, 255, 255, 0.95)",
            width="100%",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        ),
        
        # Navigation menu
        rx.box(
            rx.hstack(
                rx.link(
                    rx.box(
                        rx.text("Articles overview", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/articles",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Chapter Index", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/chapters",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Media", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/media",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Photos", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/photos",
                    text_decoration="none",
                    color="inherit",
                ),
                spacing="0",
                justify="center",
                width="100%",
            ),
            background="#d8d8d8",
            padding="0",
            width="100%",
            border_top="1px solid #c0c0c0",
            border_bottom="1px solid #c0c0c0",
        ),
        
        spacing="0",
        width="100%",
        margin_bottom="2rem",
    )


def article_page() -> rx.Component:
    """Display the loaded HTML article."""
    return rx.box(
        rx.vstack(
            # Back button - more prominent
            rx.box(
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.text("←", font_size="1.2rem"),
                            rx.text("Back to Articles"),
                            spacing="2",
                        ),
                        size="3",
                        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color="white",
                        border_radius="8px",
                        cursor="pointer",
                        _hover={"opacity": "0.9", "transform": "translateX(-3px)"},
                        transition="all 0.3s ease",
                    ),
                    href="/articles",
                    text_decoration="none",
                ),
                padding="1rem",
                width="100%",
                background="#f8f9fa",
                border_bottom="1px solid #e0e0e0",
            ),
            
            # Article Content
            rx.box(
                rx.html(State.article_content),
                padding="2rem",
                width="100%",
                max_width="900px",
                margin="0 auto",
                background="white",
                min_height="80vh",
            ),
            spacing="0",
            width="100%",
        ),
        width="100%",
        background="#f0f2f5",
        min_height="100vh",
    )


def articles_page() -> rx.Component:
    """Articles overview section with links to all bhu-mandala articles."""
    
    # Define article categories and their articles
    flat_earth_series = [
        {"title": "The Flat Earth According to Śrīmad-Bhāgavatam", "parts": 3, "file": "jambudvipa", "desc": "Exploring Vedic cosmology and the flat earth perspective", "color": "#667eea"},
        {"title": "The Vedic History Reveals a Greater Earth Plane", "parts": 2, "file": "greater-earth-plane", "desc": "Discovering the expanded earth beyond our known world", "color": "#764ba2"},
        {"title": "The Earth is Not a Globe", "parts": 3, "file": "earth-is-not-a-globe", "desc": "Challenging the global earth model with Vedic evidence", "color": "#f093fb"},
        {"title": "Flat-Earth or Globular Earth?", "parts": 3, "file": "flat-or-globular-earth-", "desc": "Examining both perspectives through scriptural analysis", "color": "#4facfe"},
    ]
    
    single_articles = [
        ("Flat-Earth in the Ramayana", "flat-earth-in-the-ramayana.html", "#FF6B6B"),
        ("Vedic History and The Flat Earth", "vedic-history-and-the-flat-earth.html", "#4ECDC4"),
        ("What's Below the Earth? — The Subterranean Worlds", "whats-below-the-earth.html", "#45B7D1"),
        ("The 3-layered planetary systems and the 14 worlds", "fourteen-worlds.html", "#96CEB4"),
        ("Bhū-maṇḍala and its seven islands", "bhumandala-dvipas.html", "#FFEAA7"),
        ("Jambūdvīpa the center island of Bhū-maṇḍala", "jambudvipa-varshas.html", "#DFE6E9"),
        ("Ananta-Sesha - the Support of the Earth", "earth-support-ananta-sesha.html", "#A29BFE"),
        ("THE POLESTAR - DHRUVA-LOKA", "polestar-dhruva-loka.html", "#FD79A8"),
        ("THE ORBITS OF THE PLANETS", "orbits-of-the-planets.html", "#FDCB6E"),
        ("The Gravity Hoax", "gravity-hoax.html", "#E17055"),
        ("Virāṭ-rūpa - the Lords Cosmic Form", "viratrupa.html", "#6C5CE7"),
        ("NARAKA - punishment in 28 hells", "naraka-punishment.html", "#00B894"),
    ]
    
    return rx.box(
        rx.vstack(
            classic_header(),
            # Header
            rx.vstack(
                rx.heading(
                    "Sailing to Jambūdvīpa",
                    size="9",
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    background_clip="text",
                    font_weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "Articles on Vedic Cosmology and Flat Earth",
                    size="5",
                    color="#666",
                    text_align="center",
                ),
                spacing="2",
                margin_bottom="3rem",
            ),
            
            # Featured Article Series - Card Grid
            rx.heading("Featured Article Series", size="7", color="#333", margin_bottom="1.5rem"),
            rx.box(
                *[
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.heading(
                                    article["title"],
                                    size="5",
                                    color="white",
                                    font_weight="bold",
                                ),
                                padding="1.5rem",
                                background=f"linear-gradient(135deg, {article['color']} 0%, {article['color']}dd 100%)",
                                border_radius="12px 12px 0 0",
                            ),
                            rx.vstack(
                                rx.text(
                                    article["desc"],
                                    size="3",
                                    color="#666",
                                    line_height="1.6",
                                ),
                                rx.hstack(
                                    *[
                                        rx.link(
                                            rx.button(
                                                f"Part {part_num}",
                                                size="2",
                                                background=article['color'],
                                                color="white",
                                                border_radius="20px",
                                                _hover={"opacity": "0.8", "transform": "translateY(-2px)"},
                                                transition="all 0.3s ease",
                                            ),
                                            href=f"/article/{article['file']}{part_num}.html",
                                        )
                                        for part_num in range(1, article["parts"] + 1)
                                    ],
                                    spacing="2",
                                    wrap="wrap",
                                ),
                                spacing="3",
                                padding="1.5rem",
                            ),
                            spacing="0",
                            align="start",
                        ),
                        background="white",
                        border_radius="12px",
                        box_shadow="0 4px 20px rgba(0, 0, 0, 0.08)",
                        transition="all 0.3s ease",
                        _hover={
                            "box_shadow": "0 8px 30px rgba(0, 0, 0, 0.12)",
                            "transform": "translateY(-5px)",
                        },
                    )
                    for article in flat_earth_series
                ],
                display="grid",
                grid_template_columns="repeat(auto-fill, minmax(300px, 1fr))",
                gap="2rem",
                width="100%",
                margin_bottom="3rem",
            ),
            
            # Additional Articles - Compact Cards
            rx.heading("Additional Articles", size="7", color="#333", margin_bottom="1.5rem"),
            rx.box(
                *[
                    rx.link(
                        rx.button(
                            title,
                            variant="surface",
                            size="3",
                            color_scheme="gray",
                            width="100%",
                            text_align="left",
                            justify_content="start",
                            padding="1rem 1.5rem",
                            background="white",
                            border=f"1px solid {color}20",
                            border_left=f"4px solid {color}",
                            border_radius="8px",
                            cursor="pointer",
                            _hover={
                                "background": f"{color}10",
                                "transform": "translateX(5px)",
                            },
                            transition="all 0.3s ease",
                        ),
                        href=f"/article/{file}",
                        text_decoration="none",
                        width="100%",
                    )
                    for title, file, color in single_articles
                ],
                display="grid",
                grid_template_columns="repeat(auto-fill, minmax(350px, 1fr))",
                gap="1rem",
                width="100%",
                margin_bottom="2rem",
            ),
            
            spacing="4",
            padding="3rem 2rem",
            max_width="1400px",
            width="100%",
        ),
        background="#ffffff",
        min_height="100vh",
        display="flex",
        justify_content="center",
        width="100vw",
    )


def media_page() -> rx.Component:
    """Media section with YouTube videos."""
    return rx.box(
        rx.vstack(
            classic_header(),
            rx.heading(
                "Media - Systematic Study of Bhagavad Gita and Srimad Bhagavatam",
                size="7",
                color="#000099",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                "Selected videos relevant to Bhu-mandala and Vedic Cosmology.",
                size="3",
                color="#333",
                text_align="center",
                line_height="1.8",
                margin_bottom="2rem",
            ),
            
            # YouTube Video Embed
            rx.box(
                rx.html(
                    """
                    <iframe width="100%" height="500" 
                        src="https://www.youtube.com/embed/ObjkdcE_TXo" 
                        title="Description of Jambhudvipa, Bharata Varsa and Bharata Khanda from Bhugola Varnanam" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        allowfullscreen
                        style="border-radius: 12px;">
                    </iframe>
                    """
                ),
                width="100%",
                max_width="900px",
                margin_bottom="2rem",
                box_shadow="0 8px 16px rgba(0, 0, 0, 0.2)",
                border_radius="12px",
            ),
            
            rx.text(
                "Description of Jambhudvipa, Bharata Varsa and Bharata Khanda from Bhugola Varnanam",
                size="5",
                weight="bold",
                color="#000099",
                margin_bottom="1rem",
            ),
            
            rx.divider(width="50%"),
            
            rx.text(
                "Visit the full channel:",
                size="3",
                color="#333",
                margin_top="1rem",
                margin_bottom="0.5rem",
            ),
            rx.link(
                "Systematic Study of Bhagavad Gita and Srimad Bhagavatam",
                href="https://www.youtube.com/channel/UCqn9xNl4DOjXbo78awGlGXA",
                is_external=True,
                color="#000099",
                text_decoration="underline",
                font_size="1.1rem",
                _hover={"opacity": "0.7"},
            ),
            
            spacing="4",
            align="center",
            width="100%",
            padding="2rem",
        ),
        background="#f9f9f9",
        min_height="100vh",
    )


def introduction_section() -> rx.Component:
    """Introduction section with Loka-traya explanation."""
    return rx.box(
        rx.vstack(
            rx.heading(
                LOKA_TRAYA_INFO["title"],
                size="7",
                color="#FFD700",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                LOKA_TRAYA_INFO["description"],
                size="3",
                color="rgba(255, 255, 255, 0.9)",
                text_align="center",
                line_height="1.8",
                margin_bottom="1.5rem",
            ),
            
            # Three worlds explanation
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "☀️ " + LOKA_TRAYA_INFO["upper_world"]["name"],
                        size="4",
                        color="#FFD700",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["upper_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(255, 215, 0, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(255, 215, 0, 0.3)",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(
                        "🌍 " + LOKA_TRAYA_INFO["middle_world"]["name"],
                        size="4",
                        color="#6B8E23",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["middle_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(107, 142, 35, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(107, 142, 35, 0.3)",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(
                        "🌑 " + LOKA_TRAYA_INFO["lower_world"]["name"],
                        size="4",
                        color="#8B4513",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["lower_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(139, 69, 19, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(139, 69, 19, 0.3)",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                flex_wrap="wrap",
            ),
            
            # Cosmological diagram
            rx.image(
                src="/14-lokas.jpg",
                alt="The Fourteen Lokas",
                width="100%",
                max_width="600px",
                border_radius="12px",
                box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                margin_top="2rem",
            ),
            
            spacing="4",
            align="center",
            width="100%",
        ),
        background="rgba(0, 0, 0, 0.3)",
        padding="2rem",
        border_radius="16px",
        margin_bottom="3rem",
    )


def lotus_cosmology_section() -> rx.Component:
    """Lotus cosmology explanation with images."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "🌺 The Lotus Flower Cosmology",
                size="7",
                color="#FF69B4",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                LOTUS_COSMOLOGY["description"],
                size="3",
                color="rgba(255, 255, 255, 0.9)",
                text_align="center",
                line_height="1.8",
                margin_bottom="1rem",
            ),
            rx.text(
                f"— {LOTUS_COSMOLOGY['reference']}",
                size="2",
                color="rgba(255, 255, 255, 0.7)",
                font_style="italic",
                text_align="center",
                margin_bottom="2rem",
            ),
            
            # Lotus images
            rx.hstack(
                rx.image(
                    src="/vishnu_lotus.jpg",
                    alt="Lotus flower growing from Lord Viṣṇu's navel",
                    width="45%",
                    border_radius="12px",
                    box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                ),
                rx.image(
                    src="/brahma-lotus.jpg",
                    alt="Brahma on lotus flower",
                    width="45%",
                    border_radius="12px",
                    box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                ),
                spacing="4",
                width="100%",
                justify="center",
                flex_wrap="wrap",
            ),
            
            spacing="4",
            align="center",
            width="100%",
        ),
        background="rgba(255, 105, 180, 0.1)",
        padding="2rem",
        border_radius="16px",
        border="1px solid rgba(255, 105, 180, 0.3)",
        margin_bottom="3rem",
    )


def index() -> rx.Component:
    """Main page showing all fourteen worlds."""
    upper_worlds = [w for w in WORLDS_DATA if w["category"] == "upper"]
    middle_worlds = [w for w in WORLDS_DATA if w["category"] == "middle"]
    lower_worlds = [w for w in WORLDS_DATA if w["category"] == "lower"]
    
    return rx.box(
        detail_modal(),
        rx.container(
            rx.vstack(
                # Classic Header with Navigation
                classic_header(),
                
                # Home content (default)
                rx.vstack(
                    # Introduction Section
                    introduction_section(),
                    
                    # Lotus Cosmology Section
                    lotus_cosmology_section(),
                    
                    # Upper Worlds
                    rx.vstack(
                        rx.heading(
                            "☀️ Upper Worlds (Svargaloka)",
                            size="6",
                            color="#FFD700",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in upper_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="3rem",
                    ),
                    
                    # Middle Worlds
                    rx.vstack(
                        rx.heading(
                            "🌍 Middle Worlds (Madhya-loka)",
                            size="6",
                            color="#6B8E23",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in middle_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="3rem",
                    ),
                    
                    # Lower Worlds
                    rx.vstack(
                        rx.heading(
                            "🌑 Lower Worlds (Pātāla)",
                            size="6",
                            color="#8B4513",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in lower_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="2rem",
                    ),
                    
                    # Footer
                    rx.box(
                        rx.vstack(
                            rx.divider(margin_y="2rem"),
                            rx.heading(
                                "About This Content",
                                size="5",
                                color="rgba(255, 255, 255, 0.9)",
                                text_align="center",
                            ),
                            rx.text(
                                "The information on this website is based on Śrīmad-Bhāgavatam and other Vedic scriptures, describing the fourteen planetary systems (Catur-daśa-bhuvana) that comprise the material universe.",
                                size="2",
                                color="rgba(255, 255, 255, 0.7)",
                                text_align="center",
                                line_height="1.6",
                            ),
                            rx.text(
                                "Source references include the bhu-mandala cosmological research and vedabase.io scriptural database.",
                                size="2",
                                color="rgba(255, 255, 255, 0.6)",
                                font_style="italic",
                                text_align="center",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        margin_top="3rem",
                    ),
                    
                    spacing="5",
                    padding_y="2rem",
                    width="100%",
                ),  # Close home content vstack
                
                spacing="5",
                padding_y="2rem",
            ),
            max_width="900px",
        ),
        background="#ffffff",
        min_height="100vh",
        padding="0",
    )


def chapters_page() -> rx.Component:
    """Placeholder page for Chapters."""
    return rx.vstack(
        classic_header(),
        rx.box(
            rx.vstack(
                rx.heading("Chapter Index", size="8", color="#000099"),
                rx.text("Explore the detailed chapters of Vedic Cosmology.", size="4", color="gray"),
                rx.divider(),
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text("We are currently working on digitizing the chapter index. Please check back later.", size="3"),
                rx.button("Return Home", on_click=rx.redirect("/"), size="3", variant="outline"),
                spacing="6",
                align="center",
                padding="4rem",
                background="white",
                border_radius="12px",
                box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
                max_width="800px",
                width="100%",
            ),
            width="100%",
            display="flex",
            justify_content="center",
            padding="2rem",
        ),
        width="100%",
        min_height="100vh",
        background="#f0f2f5",
    )


def photos_page() -> rx.Component:
    """Placeholder page for Photos."""
    return rx.vstack(
        classic_header(),
        rx.box(
            rx.vstack(
                rx.heading("Photo Gallery", size="8", color="#000099"),
                rx.text("Visual journey through the Fourteen Worlds.", size="4", color="gray"),
                rx.divider(),
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text("A curated collection of cosmological diagrams and artwork is being prepared.", size="3"),
                rx.button("Return Home", on_click=rx.redirect("/"), size="3", variant="outline"),
                spacing="6",
                align="center",
                padding="4rem",
                background="white",
                border_radius="12px",
                box_shadow="0 4px 12px rgba(0, 0, 0, 0.1)",
                max_width="800px",
                width="100%",
            ),
            width="100%",
            display="flex",
            justify_content="center",
            padding="2rem",
        ),
        width="100%",
        min_height="100vh",
        background="#f0f2f5",
    )


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
# Dynamic route for articles
app.add_page(
    article_page, 
    route="/article/[filename]", 
    title="Article Viewer - Fourteen Worlds",
    on_load=State.load_article_from_url,
)
