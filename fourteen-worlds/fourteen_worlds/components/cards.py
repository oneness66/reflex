import reflex as rx
from ..state import State

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
                font_style_type="italic", # Corrected argument name if needed, or just font_style
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
