import reflex as rx
from ..state import State
from ..components.header import tovp_header

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
    """Articles overview section with links to all bhu-mandala articles, styled like TOVP."""
    
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
            tovp_header(),
            
            # Hero Section
            rx.box(
                rx.vstack(
                    rx.heading(
                        "VEDIC SCIENCE",
                        size="9",
                        color="white",
                        font_weight="bold",
                        text_align="center",
                        letter_spacing="0.1em",
                    ),
                    rx.text(
                        "Exploring the Universe through the eyes of the Vedas",
                        size="5",
                        color="white",
                        text_align="center",
                        margin_top="1rem",
                    ),
                    padding="6rem 2rem",
                    align="center",
                    justify="center",
                    width="100%",
                    background="linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('/bhu-mandala/img/bg-stars.jpg')",
                    background_size="cover",
                    background_position="center",
                ),
                width="100%",
            ),
            
            # Content Container
            rx.container(
                rx.vstack(
                    # Intro Text
                    rx.text(
                        "Welcome to the Vedic Science page. Vedic refers to the ancient culture of India and the sacred texts of wisdom called the Vedas which encompass all branches of human experience and knowledge, material and spiritual.",
                        size="4",
                        color="#444",
                        line_height="1.8",
                        text_align="center",
                        margin_y="3rem",
                        max_width="800px",
                    ),
                    
                    rx.divider(margin_bottom="3rem"),
                    
                    # Grid Layout for Categories
                    rx.grid(
                        # Vedic Cosmology Section
                        rx.box(
                            rx.heading("VEDIC COSMOLOGY", size="6", color="#333", margin_bottom="1.5rem", border_bottom="2px solid #gold"),
                            rx.vstack(
                                *[
                                    rx.link(
                                        rx.box(
                                            rx.heading(article["title"], size="4", color="#0056b3", _hover={"color": "#d4af37"}),
                                            rx.text(article["desc"], size="2", color="#666", margin_top="0.5rem"),
                                            padding="1rem",
                                            border_bottom="1px solid #eee",
                                            width="100%",
                                            _hover={"background": "#f9f9f9"},
                                        ),
                                        href=f"/article/{article['file']}1.html", # Default to part 1
                                        text_decoration="none",
                                        width="100%",
                                    )
                                    for article in flat_earth_series
                                ],
                                width="100%",
                                spacing="0",
                            ),
                            padding="1rem",
                            background="white",
                            box_shadow="0 4px 12px rgba(0,0,0,0.05)",
                            border_radius="8px",
                        ),
                        
                        # Vedic Science Essays Section
                        rx.box(
                            rx.heading("VEDIC SCIENCE ESSAYS", size="6", color="#333", margin_bottom="1.5rem"),
                            rx.vstack(
                                *[
                                    rx.link(
                                        rx.box(
                                            rx.heading(title, size="4", color="#0056b3", _hover={"color": "#d4af37"}),
                                            padding="1rem",
                                            border_bottom="1px solid #eee",
                                            width="100%",
                                            _hover={"background": "#f9f9f9"},
                                        ),
                                        href=f"/article/{file}",
                                        text_decoration="none",
                                        width="100%",
                                    )
                                    for title, file, _ in single_articles[:6] # Show first 6
                                ],
                                width="100%",
                                spacing="0",
                            ),
                            padding="1rem",
                            background="white",
                            box_shadow="0 4px 12px rgba(0,0,0,0.05)",
                            border_radius="8px",
                        ),
                        
                        # More Essays / Other Section
                        rx.box(
                            rx.heading("MORE TOPICS", size="6", color="#333", margin_bottom="1.5rem"),
                            rx.vstack(
                                *[
                                    rx.link(
                                        rx.box(
                                            rx.heading(title, size="4", color="#0056b3", _hover={"color": "#d4af37"}),
                                            padding="1rem",
                                            border_bottom="1px solid #eee",
                                            width="100%",
                                            _hover={"background": "#f9f9f9"},
                                        ),
                                        href=f"/article/{file}",
                                        text_decoration="none",
                                        width="100%",
                                    )
                                    for title, file, _ in single_articles[6:] # Show remaining
                                ],
                                width="100%",
                                spacing="0",
                            ),
                            padding="1rem",
                            background="white",
                            box_shadow="0 4px 12px rgba(0,0,0,0.05)",
                            border_radius="8px",
                        ),
                        
                        columns="3",
                        spacing="6",
                        width="100%",
                    ),
                    
                    spacing="4",
                    padding_bottom="4rem",
                    width="100%",
                ),
                max_width="1200px",
            ),
            
            width="100%",
            spacing="0",
        ),
        background="#f8f9fa",
        min_height="100vh",
        width="100%",
    )
