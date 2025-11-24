import reflex as rx
from ..components.header import tovp_header
from ..state import State
from ..components.video_card import render_video_card

# Video Data organized by Category
video_categories = {
    "Danavir Goswami": [],
    "Sadaputa Dasa (R. L. Thompson)": [],
    "Bhaktivedanta Vidyapitha Res. Ctr.": [],
    "Caitanya Chandra Das": [],
    "Ghanashyam Govinda Das": [],
    "Sri Sampati Dasa": [
        {
            "title": "The Cosmic Framework: Concept of Time | Srimad Bhagavatam | Creation Series - 1",
            "url": "https://www.youtube.com/watch?v=SRY-jvwhH3Y",
            "video_id": "SRY-jvwhH3Y",
            "duration": "",
            "description": "Exploring the Vedic concept of time and the cosmic framework from Srimad Bhagavatam"
        },
        {
            "title": "OM: The First Sound of Creation | Creation Series - 2",
            "url": "https://www.youtube.com/watch?v=RS1Yx1ft7M8",
            "video_id": "RS1Yx1ft7M8",
            "duration": "",
            "description": "Understanding the significance of OM as the primordial sound of creation"
        },
        {
            "title": "Before The Big Bang : Creation Series - 3",
            "url": "https://www.youtube.com/watch?v=AdovUgBsbKg",
            "video_id": "AdovUgBsbKg",
            "duration": "",
            "description": "Exploring what existed before the Big Bang from a Vedic perspective"
        },
        {
            "title": "Mahat-tattva: The Cosmic Intelligence That Shapes Creation | Creation Series 4",
            "url": "https://www.youtube.com/watch?v=K5nDluUz2sE",
            "video_id": "K5nDluUz2sE",
            "duration": "",
            "description": "Understanding the Mahat-tattva - the cosmic intelligence that shapes all creation"
        },
        {
            "title": "Ahankara: Cosmic Ego Explained : Creation Series - 5",
            "url": "https://www.youtube.com/watch?v=HKF-KnW5i8M",
            "video_id": "HKF-KnW5i8M",
            "duration": "",
            "description": "Deep dive into Ahankara - the cosmic ego principle in Vedic philosophy"
        },
        {
            "title": "The science of Devatas : Creation Series 6 | Srimad Bhagavatam",
            "url": "https://www.youtube.com/watch?v=YprQKc0YmUE",
            "video_id": "YprQKc0YmUE",
            "duration": "",
            "description": "Understanding the scientific principles behind the Devatas in Vedic cosmology"
        },
        {
            "title": "Pindanda: Origin of the Material Body | Creation Series - 7",
            "url": "https://www.youtube.com/watch?v=mPaF_WbLZ0U",
            "video_id": "mPaF_WbLZ0U",
            "duration": "",
            "description": "Exploring Pindanda - the origin and structure of the material body"
        },
        {
            "title": "How Souls Enter the Body | Creation Series - 8",
            "url": "https://www.youtube.com/watch?v=OYTHrSISskc",
            "video_id": "OYTHrSISskc",
            "duration": "",
            "description": "Understanding the process of how souls enter material bodies"
        },
        {
            "title": "Pralaya : All Secrets Revealed | Creation Series - 9",
            "url": "https://www.youtube.com/watch?v=EEox9unXb-U",
            "video_id": "EEox9unXb-U",
            "duration": "",
            "description": "Exploring Pralaya - the cosmic dissolution at the end of the universe"
        }
    ]
}

def vedic_science_item(title: str, url: str) -> rx.Component:
    return rx.link(
        rx.box(
            rx.text(title, font_weight="bold", font_size="1.1rem", color="#333"),
            rx.text("Explore this section", font_size="0.9rem", color="#666"),
            padding="1.5rem",
            border="1px solid #e0e0e0",
            border_radius="8px",
            background="white",
            width="100%",
            _hover={
                "background": "#f9f9f9",
                "border_color": "#d4af37",
                "transform": "translateY(-2px)",
                "box_shadow": "0 4px 12px rgba(0,0,0,0.1)",
            },
            transition="all 0.2s ease",
        ),
        href=url,
        text_decoration="none",
        width="100%",
    )

def vedic_science_page() -> rx.Component:
    return rx.vstack(
        tovp_header(),
        rx.box(
            rx.vstack(
                rx.heading("Vedic Science", size="8", color="#333", margin_bottom="1rem"),
                rx.text(
                    "Vedic refers to the ancient culture of India and the sacred texts of wisdom called the Vedas which encompass all branches of human experience and knowledge, material and spiritual.",
                    font_size="1.1rem",
                    color="#555",
                    max_width="800px",
                    text_align="center",
                    margin_bottom="2rem",
                ),
                
                rx.grid(
                    vedic_science_item("Vedic Cosmology", "/vedic-science/cosmology"),
                    vedic_science_item("Vedic Cosmology Videos", "/vedic-science/cosmology-videos"),
                    vedic_science_item("Vedic Wisdom Videos", "/vedic-science/wisdom-videos"),
                    vedic_science_item("Vedic Science Essays", "/vedic-science/essays"),
                    vedic_science_item("Vedic Science Channel", "/vedic-science/channel"),
                    vedic_science_item("Vedic Science/History Channel", "/vedic-science/history-channel"),
                    vedic_science_item("Shabda Media", "/vedic-science/shabda-media"),
                    vedic_science_item("Vedic Science Books", "/vedic-science/books"),
                    vedic_science_item("Intelligent Design Videos", "/vedic-science/intelligent-design"),
                    columns="3",
                    spacing="6",
                    width="100%",
                ),
                
                padding="4rem 2rem",
                max_width="1200px",
                margin="0 auto",
                align="center",
            ),

            width="100%",
            background="#fcfcfc",
        ),
        
        # Learning Centers Section
        rx.box(
            rx.vstack(
                rx.heading("LEARNING CENTERS", size="6", color="#333", margin_bottom="2rem", text_align="center"),
                rx.grid(
                    # Card 1
                    rx.vstack(
                        rx.heading("THE BHAKTIVEDANTA INSTITUTE", size="4", color="#333", margin_bottom="0.5rem"),
                        rx.text(
                            "Bhaktivedanta Institute is an internationally acclaimed non-profit organization dedicated towards the cause of helping humanity through the interface of modern science and technology with spiritual traditions of the world.",
                            font_size="0.9rem",
                            color="#555",
                            margin_bottom="1rem",
                        ),
                        rx.link(
                            rx.button("Read more +", size="2", variant="solid", color_scheme="teal"),
                            href="https://bihstudies.org/",
                            is_external=True,
                        ),
                        padding="1.5rem",
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        height="100%",
                        align="start",
                    ),
                    
                    # Card 2
                    rx.vstack(
                        rx.heading("BHAKTIVEDANTA INSTITUTE FOR HIGHER STUDIES", size="4", color="#333", margin_bottom="0.5rem"),
                        rx.text(
                            "The Bhaktivedanta Institute for Higher Studies (BIHS) is a center for the research and dissemination of a nonmechanistic scientific view of reality.",
                            font_size="0.9rem",
                            color="#555",
                            margin_bottom="1rem",
                        ),
                        rx.link(
                            rx.button("Read more +", size="2", variant="solid", color_scheme="teal"),
                            href="https://bihstudies.org/",
                            is_external=True,
                        ),
                        padding="1.5rem",
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        height="100%",
                        align="start",
                    ),
                    
                    # Card 3
                    rx.vstack(
                        rx.heading("BHAKTIVEDANTA RESEARCH CENTER", size="4", color="#333", margin_bottom="0.5rem"),
                        rx.text(
                            "To be a leading global institution serving India's literary heritage by collecting, preserving, researching and teaching its ancient wisdom through state of the art means for the welfare of the society at large.",
                            font_size="0.9rem",
                            color="#555",
                            margin_bottom="1rem",
                        ),
                        rx.link(
                            rx.button("Read more +", size="2", variant="solid", color_scheme="teal"),
                            href="https://brcglobal.org/",
                            is_external=True,
                        ),
                        padding="1.5rem",
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        height="100%",
                        align="start",
                    ),
                    
                    # Card 4
                    rx.vstack(
                        rx.heading("BHAKTIVEDANTA VIDYAPITHA RESEARCH CENTER", size="4", color="#333", margin_bottom="0.5rem"),
                        rx.text(
                            "TRUTH, TRADITION. TRANSFORMATION. Facilitating the study, research and preservation of ancient Indian philosophy, arts and sciences for developing contemporary applied solutions in all spheres of life",
                            font_size="0.9rem",
                            color="#555",
                            margin_bottom="1rem",
                        ),
                        rx.link(
                            rx.button("Read more +", size="2", variant="solid", color_scheme="teal"),
                            href="https://mumbai.brcindia.com/",
                            is_external=True,
                        ),
                        padding="1.5rem",
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        height="100%",
                        align="start",
                    ),
                    
                    # Card 5
                    rx.vstack(
                        rx.heading("INSTITUTE FOR SCIENCE AND SPIRITUALITY", size="4", color="#333", margin_bottom="0.5rem"),
                        rx.text(
                            "ISS is working with the main objective of rekindling interest in spirituality within the scientific community whereby the latter evolves a spiritual, anti-material perspective.",
                            font_size="0.9rem",
                            color="#555",
                            margin_bottom="1rem",
                        ),
                        rx.link(
                            rx.button("Read more +", size="2", variant="solid", color_scheme="teal"),
                            href="https://iss.iskcondelhi.org/",
                            is_external=True,
                        ),
                        padding="1.5rem",
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        height="100%",
                        align="start",
                    ),
                    
                    columns="3",
                    spacing="6",
                    width="100%",
                ),
                padding="4rem 2rem",
                max_width="1200px",
                margin="0 auto",
                align="center",
            ),
            width="100%",
            background="#f4f4f4",
        ),
        width="100%",
        min_height="100vh",
    )

def vedic_topic_page() -> rx.Component:
    return rx.vstack(
        tovp_header(),
        rx.box(
            rx.vstack(
                rx.heading(State.vedic_topic, size="8", color="#333", margin_bottom="1rem"),
                
                rx.cond(
                    State.vedic_topic == "Cosmology Videos",
                    rx.tabs.root(
                        rx.tabs.list(
                            *[
                                rx.tabs.trigger(
                                    category,
                                    value=category,
                                    color="white",
                                    background_color="transparent",
                                    _hover={"background_color": "rgba(255,255,255,0.1)"},
                                    _active={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                                )
                                for category in video_categories.keys()
                            ],
                            background_color="#3c9fa8", # Teal color from screenshot
                            border_radius="8px 8px 0 0",
                            padding="0.5rem",
                        ),
                        *[
                            rx.tabs.content(
                                rx.grid(
                                    *[render_video_card(video) for video in videos],
                                    columns=rx.breakpoints(initial="1", sm="2", md="3"),
                                    spacing="4",
                                    width="100%",
                                    padding="1rem",
                                ) if videos else rx.text("No videos available in this category yet.", padding="2rem", color="gray"),
                                value=category,
                                background_color="white",
                                border_radius="0 0 8px 8px",
                                border="1px solid #e0e0e0",
                                width="100%",
                            )
                            for category, videos in video_categories.items()
                        ],
                        default_value="Danavir Goswami",
                        width="100%",
                    ),
                    rx.text("Content for this section is coming soon.", font_size="1.2rem", color="#555"),
                ),
                
                rx.link(
                    rx.button("Back to Vedic Science", variant="outline", margin_top="2rem"),
                    href="/vedic-science",
                ),
                padding="4rem 2rem",
                align="center",
            ),
            width="100%",
            background="#fcfcfc",
            min_height="80vh",
        ),
        width="100%",
    )
