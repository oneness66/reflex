import reflex as rx
from ..components.header import tovp_header

def photos_page() -> rx.Component:
    """Placeholder page for Photos."""
    return rx.vstack(
        tovp_header(),
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
