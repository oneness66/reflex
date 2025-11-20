import reflex as rx
from ..components.header import tovp_header

def media_page() -> rx.Component:
    """Media section with YouTube videos."""
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
                    
                    # YouTube Video Embed
                    rx.box(
                        rx.html(
                            """
                            <iframe width="100%" height="500" 
                                src="https://www.youtube.com/embed/ObjkdcE_TXo" 
                                title="Description of Jambhudvipa, Bharata Varsa and Bharata Khanda from Bhugola Varnanam" 
                                frameborder="0" 
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                                allowfullscreen
                                style="border-radius: 12px;">
                            </iframe>
                            """
                        ),
                        width="100%",
                        max_width="900px",
                        margin_bottom="2rem",
                        box_shadow="0 8px 16px rgba(0, 0, 0, 0.2)",
                        border_radius="12px",
                    ),
                    
                    rx.text(
                        "Description of Jambhudvipa, Bharata Varsa and Bharata Khanda from Bhugola Varnanam",
                        size="5",
                        weight="bold",
                        color="#000099",
                        margin_bottom="1rem",
                    ),
                    
                    rx.divider(width="50%"),
                    
                    rx.text(
                        "Visit the full channel:",
                        size="3",
                        color="#333",
                        margin_top="1rem",
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
                max_width="1200px",
                margin="0 auto",
            ),
            
            spacing="0",
            width="100%",
        ),
        background="#f9f9f9",
        min_height="100vh",
        width="100%",
    )
