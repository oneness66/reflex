import reflex as rx
from ..components.header import tovp_header
from ..data.sb import cantos
from ..components.video_card import render_video_card
from ..pages.vedic_science import video_categories

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
                    margin_bottom="12px",
                    width="100%",
                ),
                
                # Title
                rx.heading(
                    "Śrīmad-Bhāgavatam",
                    font_size="2.5rem",
                    font_weight="700",
                    font_family="'Noto Serif', Georgia, serif",
                    margin_bottom="8px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                rx.text(
                    "The Beautiful Story of the Personality of Godhead",
                    font_size="1.1rem",
                    color="#666",
                    font_style="italic",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    margin_bottom="24px",
                    text_align="center",
                    width="100%",
                ),
                
                # Tabs for different versions and videos
                rx.tabs.root(
                    # Tab navigation with arrows
                    rx.hstack(
                        # Left scroll arrow
                        rx.box(
                            rx.icon(
                                "chevron-left",
                                size=20,
                                color="white",
                            ),
                            cursor="pointer",
                            on_click=rx.call_script("document.querySelector('.tab-scroll-container').scrollBy({left: -200, behavior: 'smooth'})"),
                            padding="0.75rem 1rem",
                            _hover={"background_color": "rgba(0,0,0,0.1)"},
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        # Scrollable tabs list
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "Śrīmad-Bhāgavatam",
                                value="sb_cantos",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            *[
                                rx.tabs.trigger(
                                    speaker,
                                    value=speaker,
                                    color="white",
                                    background_color="transparent",
                                    padding="0.5rem 1rem",
                                    white_space="nowrap",
                                    _hover={"background_color": "rgba(255,255,255,0.1)"},
                                    _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                                )
                                for speaker in video_categories.keys()
                            ],
                            display="flex",
                            overflow_x="auto",
                            overflow_y="hidden",
                            flex="1",
                            class_name="tab-scroll-container",
                            css={
                                "scrollbar-width": "none",
                                "&::-webkit-scrollbar": {"display": "none"},
                            },
                        ),
                        # Right scroll arrow
                        rx.box(
                            rx.icon(
                                "chevron-right",
                                size=20,
                                color="white",
                            ),
                            cursor="pointer",
                            on_click=rx.call_script("document.querySelector('.tab-scroll-container').scrollBy({left: 200, behavior: 'smooth'})"),
                            padding="0.75rem 1rem",
                            _hover={"background_color": "rgba(0,0,0,0.1)"},
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        spacing="0",
                        width="100%",
                        background_color="#3c9fa8",
                        border_radius="8px 8px 0 0",
                        align_items="center",
                    ),
                    # Cantos tab content
                    rx.tabs.content(
                        rx.vstack(
                            *[canto_link(canto) for canto in cantos],
                            spacing="4",
                            width="100%",
                            align="start",
                            padding="1.5rem",
                        ),
                        value="sb_cantos",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Video tabs content
                    *[
                        rx.tabs.content(
                            rx.grid(
                                *[render_video_card(video) for video in videos],
                                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                                spacing="4",
                                width="100%",
                                padding="1.5rem",
                            ) if videos else rx.text(
                                "No videos available in this category yet.",
                                padding="2rem",
                                color="gray",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                            ),
                            value=speaker,
                            background_color="white",
                            border_radius="0 0 8px 8px",
                            border="1px solid #e0e0e0",
                            width="100%",
                        )
                        for speaker, videos in video_categories.items()
                    ],
                    default_value="sb_cantos",
                    width="100%",
                ),
                
                # Bottom Navigation (Vedabase-style)
                rx.hstack(
                    # Previous book (Bhagavad-gītā)
                    rx.link(
                        rx.hstack(
                            rx.icon(
                                "arrow-left",
                                size=18,
                                color="#8b4513",
                            ),
                            rx.text(
                                "Bhagavad-gītā As It Is",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                font_size="0.95rem",
                                color="#8b4513",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        href="/library/bg",
                        text_decoration="none",
                        padding="0.75rem 1.25rem",
                        background_color="#e8d4b8",
                        border_radius="6px",
                        _hover={"background_color": "#d4c4a8"},
                        transition="all 0.2s",
                    ),
                    rx.box(flex="1"),  # Spacer
                    # Next book (Caitanya-caritāmṛta)
                    rx.link(
                        rx.hstack(
                            rx.text(
                                "Śrī Caitanya-caritāmṛta",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                font_size="0.95rem",
                                color="#8b4513",
                            ),
                            rx.icon(
                                "arrow-right",
                                size=18,
                                color="#8b4513",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        href="/library/cc",
                        text_decoration="none",
                        padding="0.75rem 1.25rem",
                        background_color="#e8d4b8",
                        border_radius="6px",
                        _hover={"background_color": "#d4c4a8"},
                        transition="all 0.2s",
                    ),
                    width="100%",
                    justify="between",
                    margin_top="3rem",
                    margin_bottom="2rem",
                ),
                
                width="100%",
                max_width="100%",
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
