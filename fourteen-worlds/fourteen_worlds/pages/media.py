import reflex as rx
from ..components.header import tovp_header

def media_page() -> rx.Component:
    """Media section with YouTube videos."""
    
    videos = [
        {
            "title": "Saturday Bhakti Vaibhav 151125 SB 8.7.26 - 8.8 Churning of the milk ocean - Lord Siva drinks poison",
            "url": "https://www.youtube.com/watch?v=J_6rj--fjCw",
            "video_id": "J_6rj--fjCw",
            "views": "25 views",
            "date": "6 days ago",
            "duration": "2:05:56"
        },
        {
            "title": "Description of Jambhudvipa, Bharata Varsa and Bharata Khanda from Bhugola Varnanam",
            "url": "https://www.youtube.com/watch?v=ObjkdcE_TXo",
            "video_id": "ObjkdcE_TXo",
            "views": "1.2K views",
            "date": "1 year ago",
            "duration": "15:30"
        }
    ]

    def render_video_card(video):
        return rx.link(
            rx.box(
                rx.box(
                    rx.image(
                        src=f"https://img.youtube.com/vi/{video['video_id']}/hqdefault.jpg",
                        width="100%",
                        height="auto",
                        aspect_ratio="16/9",
                        object_fit="cover",
                        border_radius="12px",
                    ),
                    rx.text(
                        video["duration"],
                        background="rgba(0, 0, 0, 0.8)",
                        color="white",
                        font_size="0.75rem",
                        padding="2px 4px",
                        border_radius="4px",
                        position="absolute",
                        bottom="8px",
                        right="8px",
                        font_weight="bold",
                    ),
                    position="relative",
                ),
                rx.vstack(
                    rx.text(
                        video["title"],
                        size="3",
                        weight="bold",
                        color="#0f0f0f",
                        line_height="1.4",
                        max_height="2.8em",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        display="-webkit-box",
                        _webkit_line_clamp="2",
                        _webkit_box_orient="vertical",
                        margin_top="0.75rem",
                    ),
                    rx.hstack(
                        rx.text(video["views"], size="1", color="#606060"),
                        rx.text("•", size="1", color="#606060"),
                        rx.text(video["date"], size="1", color="#606060"),
                        spacing="1",
                        align_items="center",
                    ),
                    align_items="start",
                    spacing="1",
                    width="100%",
                ),
                width="100%",
                cursor="pointer",
                transition="transform 0.2s",
                _hover={"transform": "scale(1.02)"},
            ),
            href=video["url"],
            is_external=True,
            text_decoration="none",
            width="100%",
        )

    return rx.box(
        rx.vstack(
            tovp_header(),
            
            # Content Container
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Media - Systematic Study of Bhagavad Gita and Srimad Bhagavatam",
                        size="7",
                        color="#000099",
                        text_align="center",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Selected videos relevant to Bhu-mandala and Vedic Cosmology.",
                        size="3",
                        color="#333",
                        text_align="center",
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                    
                    # Video Grid
                    rx.grid(
                        *[render_video_card(video) for video in videos],
                        columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.divider(width="100%", margin_y="3rem"),
                    
                    rx.text(
                        "Visit the full channel:",
                        size="3",
                        color="#333",
                        margin_bottom="0.5rem",
                    ),
                    rx.link(
                        "Systematic Study of Bhagavad Gita and Srimad Bhagavatam",
                        href="https://www.youtube.com/channel/UCqn9xNl4DOjXbo78awGlGXA",
                        is_external=True,
                        color="#000099",
                        text_decoration="underline",
                        font_size="1.1rem",
                        _hover={"opacity": "0.7"},
                    ),
                    
                    spacing="4",
                    align="center",
                    width="100%",
                ),
                width="100%",
                padding="2rem",
                max_width="1400px",
                margin="0 auto",
            ),
            
            spacing="0",
            width="100%",
        ),
        background="#f9f9f9",
        min_height="100vh",
        width="100%",
    )
