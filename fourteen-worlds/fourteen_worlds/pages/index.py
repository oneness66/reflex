import reflex as rx
from ..state import State
from ..components.header import tovp_header
from ..components.cards import world_card
from ..components.modals import detail_modal
from ..data.worlds_data import WORLDS_DATA, LOKA_TRAYA_INFO, LOTUS_COSMOLOGY

def introduction_section() -> rx.Component:
    """Introduction section with Loka-traya explanation."""
    return rx.box(
        rx.vstack(
            rx.heading(
                LOKA_TRAYA_INFO["title"],
                size="7",
                color="#FFD700",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                LOKA_TRAYA_INFO["description"],
                size="3",
                color="rgba(255, 255, 255, 0.9)",
                text_align="center",
                line_height="1.8",
                margin_bottom="1.5rem",
            ),
            
            # Three worlds explanation
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "☀️ " + LOKA_TRAYA_INFO["upper_world"]["name"],
                        size="4",
                        color="#FFD700",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["upper_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(255, 215, 0, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(255, 215, 0, 0.3)",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(
                        "🌍 " + LOKA_TRAYA_INFO["middle_world"]["name"],
                        size="4",
                        color="#6B8E23",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["middle_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(107, 142, 35, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(107, 142, 35, 0.3)",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(
                        "🌑 " + LOKA_TRAYA_INFO["lower_world"]["name"],
                        size="4",
                        color="#8B4513",
                    ),
                    rx.text(
                        LOKA_TRAYA_INFO["lower_world"]["description"],
                        size="2",
                        color="rgba(255, 255, 255, 0.8)",
                        text_align="center",
                    ),
                    background="rgba(139, 69, 19, 0.1)",
                    padding="1rem",
                    border_radius="8px",
                    border="1px solid rgba(139, 69, 19, 0.3)",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                flex_wrap="wrap",
            ),
            
            # Cosmological diagram
            rx.image(
                src="/14-lokas.jpg",
                alt="The Fourteen Lokas",
                width="100%",
                max_width="600px",
                border_radius="12px",
                box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                margin_top="2rem",
            ),
            
            spacing="4",
            align="center",
            width="100%",
        ),
        background="rgba(0, 0, 0, 0.3)",
        padding="2rem",
        border_radius="16px",
        margin_bottom="3rem",
    )


def lotus_cosmology_section() -> rx.Component:
    """Lotus cosmology explanation with images."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "🌺 The Lotus Flower Cosmology",
                size="7",
                color="#FF69B4",
                text_align="center",
                margin_bottom="1rem",
            ),
            rx.text(
                LOTUS_COSMOLOGY["description"],
                size="3",
                color="rgba(255, 255, 255, 0.9)",
                text_align="center",
                line_height="1.8",
                margin_bottom="1rem",
            ),
            rx.text(
                f"— {LOTUS_COSMOLOGY['reference']}",
                size="2",
                color="rgba(255, 255, 255, 0.7)",
                font_style="italic",
                text_align="center",
                margin_bottom="2rem",
            ),
            
            # Lotus images
            rx.hstack(
                rx.image(
                    src="/vishnu_lotus.jpg",
                    alt="Lotus flower growing from Lord Viṣṇu's navel",
                    width="45%",
                    border_radius="12px",
                    box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                ),
                rx.image(
                    src="/brahma-lotus.jpg",
                    alt="Brahma on lotus flower",
                    width="45%",
                    border_radius="12px",
                    box_shadow="0 8px 16px rgba(0, 0, 0, 0.3)",
                ),
                spacing="4",
                width="100%",
                justify="center",
                flex_wrap="wrap",
            ),
            
            spacing="4",
            align="center",
            width="100%",
        ),
        background="rgba(255, 105, 180, 0.1)",
        padding="2rem",
        border_radius="16px",
        border="1px solid rgba(255, 105, 180, 0.3)",
        margin_bottom="3rem",
    )


def index() -> rx.Component:
    """Main page showing all fourteen worlds."""
    upper_worlds = [w for w in WORLDS_DATA if w["category"] == "upper"]
    middle_worlds = [w for w in WORLDS_DATA if w["category"] == "middle"]
    lower_worlds = [w for w in WORLDS_DATA if w["category"] == "lower"]
    
    return rx.box(
        detail_modal(),
        rx.vstack(
            # TOVP Header
            tovp_header(),
            
            rx.container(
                rx.vstack(
                
                # Home content (default)
                rx.vstack(
                    # Introduction Section
                    introduction_section(),
                    
                    # Lotus Cosmology Section
                    lotus_cosmology_section(),
                    
                    # Upper Worlds
                    rx.vstack(
                        rx.heading(
                            "☀️ Upper Worlds (Svargaloka)",
                            size="6",
                            color="#FFD700",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in upper_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="3rem",
                    ),
                    
                    # Middle Worlds
                    rx.vstack(
                        rx.heading(
                            "🌍 Middle Worlds (Madhya-loka)",
                            size="6",
                            color="#6B8E23",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in middle_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="3rem",
                    ),
                    
                    # Lower Worlds
                    rx.vstack(
                        rx.heading(
                            "🌑 Lower Worlds (Pātāla)",
                            size="6",
                            color="#8B4513",
                            margin_bottom="1rem",
                        ),
                        rx.vstack(
                            *[world_card(world) for world in lower_worlds],
                            spacing="4",
                            width="100%",
                            align="center",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="2rem",
                    ),
                    
                    # Footer
                    rx.box(
                        rx.vstack(
                            rx.divider(margin_y="2rem"),
                            rx.heading(
                                "About This Content",
                                size="5",
                                color="rgba(255, 255, 255, 0.9)",
                                text_align="center",
                            ),
                            rx.text(
                                "The information on this website is based on Śrīmad-Bhāgavatam and other Vedic scriptures, describing the fourteen planetary systems (Catur-daśa-bhuvana) that comprise the material universe.",
                                size="2",
                                color="rgba(255, 255, 255, 0.7)",
                                text_align="center",
                                line_height="1.6",
                            ),
                            rx.text(
                                "Source references include the bhu-mandala cosmological research and vedabase.io scriptural database.",
                                size="2",
                                color="rgba(255, 255, 255, 0.6)",
                                font_style="italic",
                                text_align="center",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        margin_top="3rem",
                    ),
                    
                    spacing="5",
                    padding_y="2rem",
                    width="100%",
                ),  # Close home content vstack
                
                spacing="5",
                padding_y="2rem",
            ),
            max_width="900px",
        ),
        ),
        background="#ffffff",
        min_height="100vh",
        padding="0",
    )
