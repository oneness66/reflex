import reflex as rx
from heartyculturenursery.state import AuthState

def navbar() -> rx.Component:
    return rx.vstack(
        # Top bar
        rx.hstack(
            # Logo area
            rx.hstack(
                rx.icon("tree-deciduous", size=40, color="green"),
                rx.vstack(
                    rx.text("heartyculture", font_size="1.5em", font_weight="bold", color="#b58900", line_height="1"),
                    rx.text("nursery", font_size="1.2em", color="green", line_height="1"),
                    spacing="0",
                    align_items="start",
                ),
                align_items="center",
                spacing="2",
            ),
            
            # Search bar
            rx.hstack(
                rx.select(
                    ["All categories"],
                    default_value="All categories",
                    background_color="#f0f0f0",
                    border="none",
                    padding="0.5em",
                ),
                rx.input(
                    placeholder="What are you looking for?",
                    border="none",
                    width="300px",
                    background_color="transparent",
                ),
                rx.button(
                    rx.icon("search", color="black"),
                    background_color="#ffd700", # Yellow
                    padding="0.5em 1em",
                ),
                background_color="white",
                border="1px solid #e0e0e0",
                border_radius="5px",
                padding="0",
                overflow="hidden",
            ),
            
            # Cart
            rx.icon("shopping-cart", size=24),
            
            justify="between",
            width="100%",
            padding="1em 2em",
            align_items="center",
        ),
        
        # Navigation bar
        rx.hstack(
            rx.hstack(
                rx.text("Plants", font_weight="500"),
                rx.icon("chevron-down", size=16),
                align_items="center",
                spacing="1",
                cursor="pointer",
            ),
            rx.hstack(
                rx.text("Seeds", font_weight="500"),
                rx.icon("chevron-down", size=16),
                align_items="center",
                spacing="1",
                cursor="pointer",
            ),
            rx.hstack(
                rx.text("Plant Care", font_weight="500"),
                rx.icon("chevron-down", size=16),
                align_items="center",
                spacing="1",
                cursor="pointer",
            ),
            rx.text("Blog", font_weight="500", cursor="pointer"),
            rx.text("Our Impact", font_weight="500", cursor="pointer"),
            rx.text("Our Services", font_weight="500", cursor="pointer"),
            
            rx.spacer(),
            
            rx.cond(
                AuthState.is_logged_in,
                rx.hstack(
                    rx.text("My Account", cursor="pointer"),
                    rx.text("Logout", cursor="pointer", on_click=AuthState.logout),
                    spacing="4",
                    color="gray",
                ),
                rx.text(
                    "Login", 
                    cursor="pointer", 
                    font_weight="bold",
                    color="black",
                    on_click=AuthState.toggle_login,
                    _hover={"color": "#b58900"}
                ),
            ),
            
            width="100%",
            padding="0.5em 2em",
            border_top="1px solid #f0f0f0",
        ),
        width="100%",
        background_color="white",
        z_index="50",
    )
