import reflex as rx
from ..components.header import tovp_header
from ..data.books import books
from ..data.library_extras import transcripts, letters

class LibraryState(rx.State):
    active_tab: str = "Books"

    def set_tab(self, tab: str):
        self.active_tab = tab

def library_button(text: str, count: str = None, is_active: bool = False) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.text(text),
            rx.cond(
                count,
                rx.text(f"({count})", opacity=0.7),
            ),
            spacing="2",
        ),
        variant=rx.cond(is_active, "solid", "ghost"),
        color_scheme="brown",
        background=rx.cond(is_active, "#d2a679", "rgba(0,0,0,0.05)"),
        color=rx.cond(is_active, "black", "#5c4033"),
        padding_y="1.5rem",
        padding_x="1.5rem",
        border_radius="4px",
        _hover={"background": rx.cond(is_active, "#c09568", "rgba(0,0,0,0.1)")},
        on_click=lambda: LibraryState.set_tab(text),
    )

def book_card(book: dict) -> rx.Component:
    return rx.link(
        rx.vstack(
            rx.image(
                src=book["image"],
                width="100%",
                height="auto",
                object_fit="cover",
                border_radius="4px",
                box_shadow="0 4px 8px rgba(0,0,0,0.2)",
                transition="transform 0.2s ease, box-shadow 0.2s ease",
                _hover={
                    "transform": "translateY(-5px)",
                    "box_shadow": "0 8px 16px rgba(0,0,0,0.3)",
                },
            ),
            rx.text(
                book["title"],
                font_family="Times New Roman, serif",
                font_size="1.1rem",
                font_weight="500",
                color="#333",
                text_align="center",
                margin_top="0.5rem",
            ),
            align="center",
            spacing="2",
            width="100%",
            height="100%",
        ),
        href=book["url"],
        text_decoration="none",
        width="100%",
    )

def list_item(item: dict) -> rx.Component:
    return rx.link(
        rx.box(
            rx.text(
                item["title"],
                font_family="Times New Roman, serif",
                font_size="1.1rem",
                color="#333",
                _hover={"color": "#d4af37"},
            ),
            padding="1rem",
            background="white",
            border_radius="8px",
            box_shadow="0 2px 4px rgba(0,0,0,0.05)",
            width="100%",
            transition="all 0.2s ease",
            _hover={
                "transform": "translateX(4px)",
                "box_shadow": "0 4px 8px rgba(0,0,0,0.1)",
            },
        ),
        href=item["url"],
        text_decoration="none",
        width="100%",
    )

def chapters_page() -> rx.Component:
    """Library page matching Vedabase style."""
    return rx.vstack(
        tovp_header(),
        rx.box(
            rx.vstack(
                # Top Controls
                rx.hstack(
                    library_button("Books", is_active=LibraryState.active_tab == "Books"),
                    library_button("Transcripts", "3703", is_active=LibraryState.active_tab == "Transcripts"),
                    library_button("Letters", "6587", is_active=LibraryState.active_tab == "Letters"),
                    spacing="4",
                    width="100%",
                    max_width="1200px",
                    margin="0 auto",
                    padding_top="2rem",
                ),
                
                # Main Heading
                rx.box(
                    rx.heading(
                        "Library", 
                        size="9", 
                        color="#1a1a1a",
                        font_family="Times New Roman, serif",
                        font_weight="400",
                        margin_top="1rem",
                        margin_bottom="2rem",
                    ),
                    width="100%",
                    max_width="1200px",
                    margin="0 auto",
                ),
                
                width="100%",
                padding_x="2rem",
                padding_bottom="3rem",
            ),
            width="100%",
            background="#f3e5ab", # Beige background similar to Vedabase
            border_bottom="1px solid #e0d5a0",
        ),
        
        # Content Area
        rx.box(
            rx.cond(
                LibraryState.active_tab == "Books",
                rx.grid(
                    *[book_card(book) for book in books],
                    columns=rx.breakpoints(initial="2", sm="3", md="4", lg="5", xl="6"),
                    spacing="6",
                    width="100%",
                    max_width="1400px",
                ),
                rx.vstack(
                    rx.cond(
                        LibraryState.active_tab == "Transcripts",
                        rx.vstack(
                            *[list_item(item) for item in transcripts],
                            spacing="3",
                            width="100%",
                        ),
                        rx.vstack(
                            *[list_item(item) for item in letters],
                            spacing="3",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    max_width="800px",
                    align="stretch",
                ),
            ),
            width="100%",
            display="flex",
            justify_content="center",
            padding="3rem 2rem",
            background="#fcfcfc",
            min_height="60vh",
        ),
        
        width="100%",
        min_height="100vh",
        spacing="0",
    )
