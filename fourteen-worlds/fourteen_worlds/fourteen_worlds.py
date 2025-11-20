"""Fourteen Worlds - Interactive Visualization of Vedic Cosmology."""

import reflex as rx
from rxconfig import config
from .data.worlds_data import (
    WORLDS_DATA, 
    get_world_by_id,
    LOKA_TRAYA_INFO,
    LOTUS_COSMOLOGY,
    BILA_SVARGA_INFO,
)


class State(rx.State):
    """The app state."""
    selected_world_id: int = 0
    show_detail: bool = False
    current_page: str = "home"  # "home", "media", "articles", "chapters", "photos"
    
    def select_world(self, world_id: int):
        """Select a world to view details."""
        self.selected_world_id = world_id
        self.show_detail = True
    
    def close_detail(self):
        """Close the detail view."""
        self.show_detail = False
        self.selected_world_id = 0
    
    def navigate_to(self, page: str):
        """Navigate to a different page."""
        self.current_page = page
        self.show_detail = False  # Close any open modals
    
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
            rx.heading(
                "Sailing to the Fourteen Worlds",
                size="9",
                color="#000099",
                font_family="'Times New Roman', serif",
                font_style="italic",
                font_weight="normal",
                text_align="center",
                cursor="pointer",
                on_click=lambda: State.navigate_to("home"),
                _hover={"opacity": "0.8"},
            ),
            padding="2rem 0 1rem 0",
            background="linear-gradient(to bottom, #f5f5f5, #ffffff)",
            width="100%",
        ),
        
        # Navigation menu
        rx.box(
            rx.hstack(
                rx.box(
                    rx.text("Articles overview", size="3"),
                    padding="0.75rem 1.5rem",
                    background=rx.cond(State.current_page == "articles", "#d0d0d0", "#f0f0f0"),
                    border_radius="0",
                    cursor="pointer",
                    on_click=lambda: State.navigate_to("articles"),
                    _hover={"background": "#e0e0e0"},
                ),
                rx.box(
                    rx.text("Chapter Index", size="3"),
                    padding="0.75rem 1.5rem",
                    background=rx.cond(State.current_page == "chapters", "#d0d0d0", "#f0f0f0"),
                    border_radius="0",
                    cursor="pointer",
                    on_click=lambda: State.navigate_to("chapters"),
                    _hover={"background": "#e0e0e0"},
                ),
                rx.box(
                    rx.text("Media", size="3"),
                    padding="0.75rem 1.5rem",
                    background=rx.cond(State.current_page == "media", "#d0d0d0", "#f0f0f0"),
                    border_radius="0",
                    cursor="pointer",
                    on_click=lambda: State.navigate_to("media"),
                    _hover={"background": "#e0e0e0"},
                ),
                rx.box(
                    rx.text("Photos", size="3"),
                    padding="0.75rem 1.5rem",
                    background=rx.cond(State.current_page == "photos", "#d0d0d0", "#f0f0f0"),
                    border_radius="0",
                    cursor="pointer",
                    on_click=lambda: State.navigate_to("photos"),
                    _hover={"background": "#e0e0e0"},
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


def media_section() -> rx.Component:
    """Media section with YouTube videos."""
    # YouTube video IDs from the Systematic Study channel
    videos = [
        {"id": "videoseries?list=PLcvzqXPfxvPV6vL3X5y5jQ9m0z0F0vqHF", "title": "Srimad Bhagavatam Playlist"},
        {"id": "videoseries?list=PLcvzqXPfxvPWU8XqH_s-5Q6p6Y3X5vX3z", "title": "Bhagavad Gita Playlist"},
        {"id": "videoseries?list=PLcvzqXPfxvPUL5fPqmvZX5v5X5X5X5X5X", "title": "Vedic Cosmology"},
    ]
    
    return rx.box(
        rx.vstack(
            rx.heading(
                "Media - Systematic Study of Bhagavad Gita and Srimad Bhagavatam",
                size="7",
                color="#000099",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                "Śrīla Prabhupāda advises all of his followers to read his books daily as far as possible and try to understand the subject matter from different angles of vision by discussing it frequently with other devotees.",
                size="3",
                color="#333",
                text_align="center",
                line_height="1.8",
                margin_bottom="2rem",
            ),
            
            # YouTube Channel Embed
            rx.box(
                rx.html(
                    """
                    <iframe width="100%" height="600" 
                        src="https://www.youtube.com/embed/videoseries?list=PLcvzqXPfxvPV6vL3X5y5jQ9m0z0F0vqHF" 
                        title="YouTube video player" 
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
            ),
            
            rx.text(
                "Visit the full channel:",
                size="3",
                color="#333",
                margin_bottom="0.5rem",
            ),
            rx.link(
                "Systematic Study of BG and SB - YouTube Channel",
                href="https://www.youtube.com/@systematicstudyofbgandsb410/videos",
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
        min_height="80vh",
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
                
                # Conditional content based on current_page
                rx.cond(
                    State.current_page == "media",
                    media_section(),
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
                ),  # Close rx.cond
                
                spacing="5",
                padding_y="2rem",
            ),
            max_width="900px",
        ),
        background="#ffffff",
        min_height="100vh",
        padding="0",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
)
app.add_page(index, title="Fourteen Worlds - Vedic Cosmology")
