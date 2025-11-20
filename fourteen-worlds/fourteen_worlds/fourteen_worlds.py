"""Fourteen Worlds - Interactive Visualization of Vedic Cosmology."""

import reflex as rx
from rxconfig import config
from .data.worlds_data import WORLDS_DATA, get_world_by_id


class State(rx.State):
    """The app state."""
    selected_world_id: int = 0
    show_detail: bool = False
    
    def select_world(self, world_id: int):
        """Select a world to view details."""
        self.selected_world_id = world_id
        self.show_detail = True
    
    def close_detail(self):
        """Close the detail view."""
        self.show_detail = False
        self.selected_world_id = 0
    
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


def index() -> rx.Component:
    """Main page showing all fourteen worlds."""
    upper_worlds = [w for w in WORLDS_DATA if w["category"] == "upper"]
    middle_worlds = [w for w in WORLDS_DATA if w["category"] == "middle"]
    lower_worlds = [w for w in WORLDS_DATA if w["category"] == "lower"]
    
    return rx.box(
        detail_modal(),
        rx.container(
            rx.vstack(
                # Header
                rx.vstack(
                    rx.heading(
                        "The Fourteen Worlds",
                        size="9",
                        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        background_clip="text",
                        font_weight="bold",
                        text_align="center",
                    ),
                    rx.text(
                        "Catur-daśa-bhuvana - The Fourteen Planetary Systems of Vedic Cosmology",
                        size="4",
                        color="gray",
                        text_align="center",
                    ),
                    rx.text(
                        "Click on any world to learn more",
                        size="2",
                        color="gray",
                        text_align="center",
                        font_style="italic",
                    ),
                    spacing="2",
                    margin_bottom="2rem",
                    width="100%",
                ),
                
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
                
                spacing="5",
                padding_y="2rem",
            ),
            max_width="900px",
        ),
        background="linear-gradient(to bottom, #0f0c29, #302b63, #24243e)",
        min_height="100vh",
        padding="2rem 1rem",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
)
app.add_page(index, title="Fourteen Worlds - Vedic Cosmology")
