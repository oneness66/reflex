import reflex as rx

def render_video_card(video: dict) -> rx.Component:
    """Render a video card with thumbnail, title, and metadata.
    
    Args:
        video (dict): Dictionary containing video details:
            - title: Video title
            - url: YouTube URL
            - video_id: YouTube video ID
            - views: View count string (optional)
            - date: Upload date string (optional)
            - duration: Video duration string
            - description: Video description text (optional)
    """
    return rx.link(
        rx.box(
            rx.box(
                rx.image(
                    src=f"https://img.youtube.com/vi/{video['video_id']}/hqdefault.jpg",
                    width="100%",
                    height="auto",
                    aspect_ratio="16/9",
                    object_fit="cover",
                    border_radius="4px",
                ),
                # Play button overlay
                rx.center(
                    rx.icon("play", color="white", size=40, fill="white"),
                    position="absolute",
                    top="0",
                    left="0",
                    width="100%",
                    height="100%",
                    background="rgba(0, 0, 0, 0.3)",
                    opacity="0.8",
                    transition="opacity 0.2s",
                    _hover={"opacity": "1"},
                ),
                rx.text(
                    video["duration"],
                    background="rgba(0, 0, 0, 0.8)",
                    color="white",
                    font_size="0.75rem",
                    padding="2px 4px",
                    border_radius="2px",
                    position="absolute",
                    bottom="8px",
                    right="8px",
                    font_weight="bold",
                ),
                position="relative",
                overflow="hidden",
                border_radius="4px",
            ),
            rx.vstack(
                rx.text(
                    video["title"],
                    size="3",
                    weight="bold",
                    color="#0f0f0f",
                    line_height="1.4",
                    margin_top="0.75rem",
                ),
                rx.cond(
                    "description" in video,
                    rx.text(
                        video.get("description", ""),
                        size="2",
                        color="#606060",
                        line_height="1.5",
                        max_height="4.5em",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        display="-webkit-box",
                        _webkit_line_clamp="3",
                        _webkit_box_orient="vertical",
                    ),
                ),
                align_items="start",
                spacing="1",
                width="100%",
            ),
            width="100%",
            cursor="pointer",
            transition="transform 0.2s",
            _hover={"transform": "translateY(-2px)"},
        ),
        href=video["url"],
        is_external=True,
        text_decoration="none",
        width="100%",
    )
