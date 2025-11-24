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
                    margin_bottom="24px",
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
