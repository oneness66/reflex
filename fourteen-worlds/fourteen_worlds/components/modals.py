import reflex as rx
from ..state import State

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
