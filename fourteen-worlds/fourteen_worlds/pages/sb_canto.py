import reflex as rx
from ..components.header import tovp_header
from ..data.sb_content import sb_chapters
from ..data.sb import cantos

class SBCantoState(rx.State):
    @rx.var
    def canto_num(self) -> int:
        try:
            return int(self.router.page.params.get("canto", 1))
        except:
            return 1
            
    @rx.var
    def canto_title(self) -> str:
        """Get full Canto title"""
        try:
            # Canto numbers are 1-based, list is 0-based
            canto_data = cantos[self.canto_num - 1]
            return canto_data["title"]
        except:
            return f"Canto {self.canto_num}"

    @rx.var
    def chapters(self) -> list[dict]:
        raw_chapters = sb_chapters.get(self.canto_num, [])
        return raw_chapters
    
    @rx.var
    def prev_link(self) -> dict:
        """Get previous link data (title, url)"""
        if self.canto_num == 1:
            return {"title": "Śrīmad-Bhāgavatam", "url": "/library/sb"}
        else:
            try:
                prev_canto = cantos[self.canto_num - 2]
                return {"title": prev_canto["title"], "url": prev_canto["url"]}
            except:
                return None

    @rx.var
    def next_link(self) -> dict:
        """Get next link data (title, url)"""
        try:
            # Current canto index is canto_num - 1. Next is canto_num.
            if self.canto_num < len(cantos):
                next_canto = cantos[self.canto_num]
                return {"title": next_canto["title"], "url": next_canto["url"]}
            return None
        except:
            return None

def chapter_link(chapter: dict) -> rx.Component:
    return rx.link(
        rx.text(
            chapter["title"],
            font_family="'Noto Serif', serif",
            font_size="1.2rem",
            color="#c0392b",  # Vedabase reddish-brown
            font_weight="400",
            _hover={"text_decoration": "underline"},
        ),
        href=chapter["url"],
        text_decoration="none",
        width="100%",
        padding_y="4px",
    )

def sb_canto_page() -> rx.Component:
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
                
                # Canto Title
                rx.heading(
                    SBCantoState.canto_title,
                    font_size="3rem",
                    font_weight="700",
                    font_family="'Noto Serif', Georgia, serif",
                    margin_bottom="48px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                
                # Tabbed interface for Chapters and Videos
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
                            on_click=rx.call_script("document.querySelector('.canto-tab-scroll-container').scrollBy({left: -200, behavior: 'smooth'})"),
                            padding="0.75rem 1rem",
                            _hover={"background_color": "rgba(0,0,0,0.1)"},
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        # Scrollable tabs list
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "Chapters",
                                value="chapters",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            rx.tabs.trigger(
                                "Pavaneswar Das",
                                value="pavaneswar_das",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            display="flex",
                            overflow_x="auto",
                            overflow_y="hidden",
                            flex="1",
                            class_name="canto-tab-scroll-container",
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
                            on_click=rx.call_script("document.querySelector('.canto-tab-scroll-container').scrollBy({left: 200, behavior: 'smooth'})"),
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
                    # Chapters tab content
                    rx.tabs.content(
                        rx.vstack(
                            rx.foreach(SBCantoState.chapters, chapter_link),
                            spacing="4",
                            width="100%",
                            align="start",
                            padding="1.5rem",
                        ),
                        value="chapters",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Pavaneswar Das videos tab content
                    rx.tabs.content(
                        rx.text(
                            "Pavaneswar Das videos for this canto will be available soon.",
                            padding="2rem",
                            color="gray",
                            font_family="Georgia, 'Times New Roman', Times, serif",
                        ),
                        value="pavaneswar_das",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    default_value="chapters",
                    width="100%",
                    margin_bottom="64px",
                ),
                
                # Footer Navigation Buttons
                rx.hstack(
                    rx.cond(
                        SBCantoState.prev_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("arrow-left", size=16),
                                    rx.text(SBCantoState.prev_link["title"]),
                                    spacing="2",
                                    align="center",
                                ),
                                bg="#e6d0b3",
                                color="#000",
                                font_family="'Noto Serif', serif",
                                font_size="14px",
                                padding="12px 20px",
                                border_radius="6px",
                                _hover={"bg": "#d4a574"},
                                cursor="pointer",
                            ),
                            href=SBCantoState.prev_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no prev link
                    ),
                    rx.spacer(),
                    rx.cond(
                        SBCantoState.next_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text(SBCantoState.next_link["title"]),
                                    rx.icon("arrow-right", size=16),
                                    spacing="2",
                                    align="center",
                                ),
                                bg="#e6d0b3",
                                color="#000",
                                font_family="'Noto Serif', serif",
                                font_size="14px",
                                padding="12px 20px",
                                border_radius="6px",
                                _hover={"bg": "#d4a574"},
                                cursor="pointer",
                            ),
                            href=SBCantoState.next_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no next link
                    ),
                    width="100%",
                    padding_top="32px",
                    border_top="1px solid rgba(0,0,0,0.1)",
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
