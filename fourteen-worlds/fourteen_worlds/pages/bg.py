import reflex as rx
from ..components.header import tovp_header
from ..data.bg_content import bg_chapters
from ..components.video_card import render_video_card
import json
import os

# Load Sri Sampati Dasa BG videos
def load_sampati_videos():
    """Load Sri Sampati Dasa BG videos from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), "..", "..", "bg_sampati_videos.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('videos', [])
    except:
        return []

sampati_videos = load_sampati_videos()

# Playlist display name mapping
playlist_display_names = {
    "Bhagavad Gita Chapter Summary": "Bhagavad Gita",
    "What Happens after Death": "Bhagavad Gita Chapter Summary"
}

# BG versions/commentaries organized by category
bg_versions = {
    "Srila Prabhupada": bg_chapters,  # Current translation
    "Original Sanskrit": [],
    "Other Translations": [],
    "Commentaries": [],
    "Sri Sampati Dasa Videos": sampati_videos,  # BG-related videos
}

def chapter_link(chapter: dict) -> rx.Component:
    return rx.link(
        rx.text(
            chapter["title"],
            font_family="Georgia, 'Times New Roman', Times, serif",
            font_size="1.2rem",
            color="#c0392b",  # Vedabase reddish-brown
            font_weight="400",
            _hover={"text_decoration": "underline"},
        ),
        href=f"/library/bg/{chapter['slug']}" if chapter['is_chapter'] else "#",
        text_decoration="none",
        width="100%",
        padding_y="4px",
    )

def bg_page() -> rx.Component:
    """Bhagavad-gita Library Page."""
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
                    rx.text(
                        "Bhagavad-gītā As It Is",
                        color="#c0392b",
                        font_size="14px",
                    ),
                    spacing="2",
                    margin_bottom="24px",
                    width="100%",
                ),
                
                # Title
                rx.heading(
                    "Bhagavad-gītā As It Is",
                    font_size="3rem",
                    font_weight="700",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    margin_bottom="32px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                
                # Tabs for different versions
                rx.tabs.root(
                    rx.tabs.list(
                        *[
                            rx.tabs.trigger(
                                version_name,
                                value=version_name,
                                color="white",
                                background_color="transparent",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _active={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            )
                            for version_name in bg_versions.keys()
                        ],
                        background_color="#3c9fa8",  # Teal color matching cosmology videos
                        border_radius="8px 8px 0 0",
                        padding="0.5rem",
                    ),
                    *[
                        rx.tabs.content(
                            # Check if this is the videos tab
                            (
                                # Group videos by playlist
                                rx.vstack(
                                    *[
                                        rx.vstack(
                                            # Compact header with inline video count
                                            rx.hstack(
                                                rx.heading(
                                                    playlist_display_names.get(playlist_name, playlist_name),
                                                    font_size="1.3rem",
                                                    font_weight="600",
                                                    font_family="Georgia, 'Times New Roman', Times, serif",
                                                    color="#333",
                                                ),
                                                rx.text(
                                                    f"• {len(playlist_videos)} videos",
                                                    font_size="0.95rem",
                                                    color="#666",
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            rx.grid(
                                                *[render_video_card(video) for video in playlist_videos],
                                                columns=rx.breakpoints(initial="1", sm="2", md="3"),
                                                spacing="4",
                                                width="100%",
                                            ),
                                            width="100%",
                                            align="start",
                                            spacing="3",
                                            padding_bottom="1.5rem" if i < len({v['playlist'] for v in content}) - 1 else "0",
                                            margin_bottom="1.5rem" if i < len({v['playlist'] for v in content}) - 1 else "0",
                                            border_bottom="1px solid #e0e0e0" if i < len({v['playlist'] for v in content}) - 1 else "none",
                                        )
                                        for i, (playlist_name, playlist_videos) in enumerate([
                                            (playlist, [v for v in content if v.get('playlist') == playlist])
                                            for playlist in sorted(set(v.get('playlist', 'Other') for v in content))
                                        ])
                                    ],
                                    width="100%",
                                    padding="1.5rem",
                                    spacing="0",
                                )
                            ) if version_name == "Sri Sampati Dasa Videos" and content else (
                                # For chapters, display as list
                                rx.vstack(
                                    *[chapter_link(chapter) for chapter in content],
                                    spacing="4",
                                    width="100%",
                                    align="start",
                                    padding="1.5rem",
                                ) if content and version_name != "Sri Sampati Dasa Videos" else rx.text(
                                    "No content available in this category yet.",
                                    padding="2rem",
                                    color="gray",
                                    font_family="Georgia, 'Times New Roman', Times, serif",
                                )
                            ),
                            value=version_name,
                            background_color="white",
                            border_radius="0 0 8px 8px",
                            border="1px solid #e0e0e0",
                            width="100%",
                        )
                        for version_name, content in bg_versions.items()
                    ],
                    default_value="Srila Prabhupada",
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

