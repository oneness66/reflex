import reflex as rx
from ..components.header import tovp_header
from ..data.sb import cantos

def canto_link(canto: dict) -> rx.Component:
    return rx.link(
        rx.text(
            canto["title"],
            font_family="Georgia, 'Times New Roman', Times, serif",
            font_size="1.2rem",
            color="#c0392b",  # Vedabase reddish-brown
            font_weight="400",
            _hover={"text_decoration": "underline"},
        ),
        href=canto["url"],
        text_decoration="none",
        width="100%",
        padding_y="4px",
    )

def sb_page() -> rx.Component:
    """Srimad Bhagavatam Library Page."""
    return rx.vstack(
        tovp_header(),
        
        # Main Content Container
        rx.box(
            rx.vstack(
                # Breadcrumb navigation
                rx.hstack(
                    rx.link(
                        "Library",
                        href="/library",
                        color="#333",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="14px",
                        font_weight="bold",
                    ),
                    rx.text("»", color="#666", font_size="14px"),
                    rx.link(
                        "Śrīmad-Bhāgavatam",
                        href="/library/sb",
                        color="#c0392b",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="14px",
                    ),
                    spacing="2",
                    margin_bottom="24px",
                    width="100%",
                ),
                
                # View Options Buttons
                rx.hstack(
                    rx.button(
                        "Default View",
                        bg="#dcbfa3",
                        color="#333",
                        font_family="Georgia, 'Times New Roman', Times, serif",
                        font_size="14px",
                        padding="8px 16px",
                        border_radius="4px",
                        _hover={"bg": "#d4a574"},
                        cursor="pointer",
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.hstack(
                                    rx.icon("languages", size=16),
                                    rx.text("Dual Language View"),
                                    rx.icon("chevron-down", size=16),
                                    spacing="2",
                                    align="center",
                                ),
                                bg="#f0e0c9",
                                color="#333",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                font_size="14px",
                                padding="8px 16px",
                                border_radius="4px",
                                border="1px solid #dcbfa3",
                                _hover={"bg": "#e6d0b3"},
                                cursor="pointer",
                            ),
                        ),
                        rx.menu.content(
                            rx.menu.item("English"),
                            rx.menu.item("Hindi"),
                            rx.menu.item("Russian"),
                            bg="#fff",
                            border="1px solid #e0e0e0",
                        ),
                    ),
                    spacing="3",
                    margin_bottom="48px",
                    width="100%",
                ),
                
                # Title
                rx.heading(
                    "Śrīmad-Bhāgavatam",
                    font_size="3rem",
                    font_weight="700",
                    font_family="'Noto Serif', Georgia, serif",
                    margin_bottom="16px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                rx.text(
                    "The Beautiful Story of the Personality of Godhead",
                    font_size="1.2rem",
                    color="#666",
                    font_style="italic",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    margin_bottom="48px",
                    text_align="center",
                    width="100%",
                ),
                
                # Canto List
                rx.vstack(
                    *[canto_link(canto) for canto in cantos],
                    spacing="4",
                    width="100%",
                    align="start",
                    margin_bottom="24px",
                ),
                
                # About the Author Link
                rx.link(
                    "About the Author",
                    href="#",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    font_size="1.2rem",
                    color="#c0392b",
                    text_decoration="none",
                    _hover={"text_decoration": "underline"},
                    margin_bottom="64px",
                ),
                
                # About the Author Section
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "About the Author",
                            size="6",
                            color="#333",
                            font_family="Georgia, 'Times New Roman', Times, serif",
                            margin_bottom="24px",
                        ),
                        rx.hstack(
                            rx.image(
                                src="/prabhupada.jpg", # Placeholder, assumes image exists or will show broken link icon which is fine for now
                                width="150px",
                                height="auto",
                                border_radius="4px",
                                border="1px solid #ccc",
                            ),
                            rx.vstack(
                                rx.text(
                                    "His Divine Grace A.C. Bhaktivedanta Swami Prabhupāda",
                                    font_weight="bold",
                                    font_size="1.1rem",
                                    color="#333",
                                    font_family="Georgia, 'Times New Roman', Times, serif",
                                ),
                                rx.text(
                                    "Founder-Ācārya of the International Society for Krishna Consciousness",
                                    font_size="0.9rem",
                                    color="#666",
                                    font_family="Georgia, 'Times New Roman', Times, serif",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            spacing="6",
                            align="start",
                            flex_wrap="wrap",
                        ),
                        align="start",
                        width="100%",
                        padding_top="32px",
                        border_top="1px solid rgba(0,0,0,0.1)",
                    ),
                    width="100%",
                ),
                
                width="100%",
                max_width="1000px",
                padding="40px",
            ),
            width="100%",
            display="flex",
            justify_content="center",
            background="#f5e6d3",  # Vedabase cream background
            min_height="100vh",
        ),
        
        width="100%",
        min_height="100vh",
        spacing="0",
    )
