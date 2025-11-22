import reflex as rx
from ..components.header import tovp_header
from ..components.video_card import render_video_card

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
