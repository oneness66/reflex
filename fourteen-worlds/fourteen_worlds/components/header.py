import reflex as rx

def tovp_header() -> rx.Component:
    """TOVP styled header with top bar and main navigation."""
    return rx.vstack(
        # Top Utility Bar
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.link("GIFT STORE", href="#", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    rx.link("BOOK MARKETPLACE", href="#", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    rx.link("DONATE", href="#", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    spacing="4",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.link("HOME", href="/", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    rx.link("NEWS", href="#", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    rx.link("CONTACT", href="#", color="white", font_size="0.75rem", font_weight="bold", text_decoration="none", _hover={"color": "#FFD700"}),
                    spacing="4",
                ),
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding_x="1rem",
            ),
            background="#1a1a1a",
            width="100%",
            padding_y="0.5rem",
        ),
        
        # Main Navigation Bar
        rx.box(
            rx.hstack(
                # Logo / Title
                rx.link(
                    rx.hstack(
                        rx.image(src="/favicon.ico", height="40px", width="auto"), # Placeholder logo
                        rx.vstack(
                            rx.heading("FOURTEEN WORLDS", size="4", color="#333", font_weight="bold", letter_spacing="0.1em"),
                            rx.text("VEDIC COSMOLOGY", size="1", color="#666", letter_spacing="0.2em"),
                            spacing="0",
                            align="start",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    href="/",
                    text_decoration="none",
                ),
                
                rx.spacer(),
                
                # Navigation Links
                rx.hstack(
                    rx.link("HOME", href="/", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    rx.link("VEDIC SCIENCE", href="/vedic-science", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    rx.link("ARTICLES", href="/articles", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    rx.link("MEDIA", href="/media", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    rx.link("CHAPTERS", href="/chapters", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    rx.link("PHOTOS", href="/photos", color="#333", font_weight="bold", font_size="0.9rem", text_decoration="none", padding="0.5rem", _hover={"color": "#d4af37"}),
                    spacing="4",
                ),
                
                # Donate Button
                rx.button(
                    "DONATE",
                    background="#d4af37",
                    color="white",
                    font_weight="bold",
                    border_radius="0",
                    padding_x="1.5rem",
                    _hover={"background": "#b5952f"},
                ),
                
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding_x="1rem",
                align="center",
            ),
            background="white",
            width="100%",
            padding_y="1rem",
            box_shadow="0 2px 10px rgba(0,0,0,0.05)",
            position="sticky",
            top="0",
            z_index="999",
        ),
        
        spacing="0",
        width="100%",
    )

# Keep classic_header for backward compatibility if needed, or we can remove it.
# For now, I'll leave it but we won't use it.
def classic_header() -> rx.Component:
    """Classic styled header with navigation menu matching bhu-mandala format."""
    return rx.vstack(
        # Header image/title
        rx.box(
            rx.link(
                rx.heading(
                    "Sailing to the Fourteen Worlds",
                    size="9",
                    color="#000099",
                    font_family="'Times New Roman', serif",
                    font_style="italic",
                    font_weight="normal",
                    text_align="center",
                    text_shadow="2px 2px 4px rgba(255, 255, 255, 0.8)",
                ),
                href="/",
                text_decoration="none",
                _hover={"opacity": "0.8"},
            ),
            padding="2rem 0 1rem 0",
            background="rgba(255, 255, 255, 0.95)",
            width="100%",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
        ),
        
        # Navigation menu
        rx.box(
            rx.hstack(
                rx.link(
                    rx.box(
                        rx.text("Articles overview", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/articles",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Chapter Index", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/chapters",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Media", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/media",
                    text_decoration="none",
                    color="inherit",
                ),
                rx.link(
                    rx.box(
                        rx.text("Photos", size="3"),
                        padding="0.75rem 1.5rem",
                        background="#f0f0f0",
                        border_radius="0",
                        _hover={"background": "#e0e0e0"},
                    ),
                    href="/photos",
                    text_decoration="none",
                    color="inherit",
                ),
                spacing="0",
                justify="center",
                width="100%",
            ),
            background="#d8d8d8",
            padding="0",
            width="100%",
            border_top="1px solid #c0c0c0",
            border_bottom="1px solid #c0c0c0",
        ),
        
        spacing="0",
        width="100%",
        margin_bottom="2rem",
    )
