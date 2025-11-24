import reflex as rx
from ..components.header import tovp_header
from ..data.sb_content import sb_verses, sb_chapters
from ..data.sb_verse_content import verse_content
from ..data.sb import cantos

class SBChapterState(rx.State):
    @rx.var
    def canto_num(self) -> int:
        try:
            return int(self.router.page.params.get("canto", 1))
        except:
            return 1

    @rx.var
    def chapter_num(self) -> int:
        try:
            return int(self.router.page.params.get("chapter", 1))
        except:
            return 1

    @rx.var
    def verses(self) -> list[dict]:
        key = f"{self.canto_num}-{self.chapter_num}"
        base_verses = sb_verses.get(key, [])
        
        # Merge with translation data
        enhanced_verses = []
        for verse in base_verses:
            # Construct key for verse_content (e.g., "1-1-1")
            verse_key = f"{self.canto_num}-{self.chapter_num}-{verse['number']}"
            content = verse_content.get(verse_key, {})
            
            enhanced_verse = verse.copy()
            enhanced_verse["translation"] = content.get("translation", "")
            enhanced_verses.append(enhanced_verse)
            
        return enhanced_verses
        
    @rx.var
    def canto_data(self) -> dict:
        try:
            return cantos[self.canto_num - 1]
        except:
            return {"title": f"Canto {self.canto_num}", "url": f"/library/sb/{self.canto_num}"}

    @rx.var
    def chapter_data(self) -> dict:
        try:
            # sb_chapters keys are ints
            chapters = sb_chapters.get(self.canto_num, [])
            if 0 < self.chapter_num <= len(chapters):
                return chapters[self.chapter_num - 1]
            return {"title": f"Chapter {self.chapter_num}"}
        except:
            return {"title": f"Chapter {self.chapter_num}"}

    @rx.var
    def prev_link(self) -> dict:
        """Get previous link data (title, url)"""
        if self.chapter_num == 1:
            # Link to Canto page
            return {"title": self.canto_data["title"], "url": f"/library/sb/{self.canto_num}"}
        else:
            # Link to previous chapter
            try:
                chapters = sb_chapters.get(self.canto_num, [])
                prev_chap = chapters[self.chapter_num - 2]
                return {"title": prev_chap["title"], "url": prev_chap["url"]}
            except:
                return None

    @rx.var
    def next_link(self) -> dict:
        """Get next link data (title, url)"""
        try:
            chapters = sb_chapters.get(self.canto_num, [])
            if self.chapter_num < len(chapters):
                # Link to next chapter
                next_chap = chapters[self.chapter_num]
                return {"title": next_chap["title"], "url": next_chap["url"]}
            else:
                # Link to next Canto (if exists)
                if self.canto_num < len(cantos):
                    next_canto = cantos[self.canto_num]
                    return {"title": next_canto["title"], "url": f"/library/sb/{self.canto_num + 1}/1"}
                return None
        except:
            return None

def verse_link(verse: dict) -> rx.Component:
    return rx.link(
        rx.box(
            rx.text(
                verse["title"],
                font_family="Georgia, 'Times New Roman', Times, serif",
                font_size="1.2rem",
                color="#c0392b",  # Vedabase reddish-brown
                font_weight="400",
                display="inline",
                margin_right="8px",
                line_height="1.6",
            ),
            rx.text(
                verse["translation"],
                font_family="Georgia, 'Times New Roman', Times, serif",
                font_size="1.2rem",
                color="#333",
                display="inline",
                line_height="1.6",
            ),
            width="100%",
            margin_bottom="16px",
            display="block",
        ),
        href=verse["url"],
        text_decoration="none",
        width="100%",
        _hover={"text_decoration": "none"},
    )

def sb_chapter_page() -> rx.Component:
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
                    rx.text("»", color="#666", font_size="14px"),
                    rx.link(
                        SBChapterState.canto_data["title"],
                        href=rx.cond(
                            SBChapterState.canto_data["url"], 
                            SBChapterState.canto_data["url"], 
                            f"/library/sb/{SBChapterState.canto_num}"
                        ),
                        color="#c0392b",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="14px",
                    ),
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                
                # Tabbed interface for Verses and Videos
                
                # Chapter Title
                rx.heading(
                    SBChapterState.chapter_data["title"],
                    font_size="3rem",
                    font_weight="700",
                    font_family="'Noto Serif', Georgia, serif",
                    margin_bottom="48px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                
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
                            on_click=rx.call_script("document.querySelector('.chapter-tab-scroll-container').scrollBy({left: -200, behavior: 'smooth'})"),
                            padding="0.75rem 1rem",
                            _hover={"background_color": "rgba(0,0,0,0.1)"},
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        # Scrollable tabs list
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "Verses",
                                value="verses",
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
                            class_name="chapter-tab-scroll-container",
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
                            on_click=rx.call_script("document.querySelector('.chapter-tab-scroll-container').scrollBy({left: 200, behavior: 'smooth'})"),
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
                    # Verses tab content
                    rx.tabs.content(
                        rx.vstack(
                            rx.foreach(SBChapterState.verses, verse_link),
                            spacing="4",
                            width="100%",
                            align="start",
                            padding="1.5rem",
                        ),
                        value="verses",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Pavaneswar Das videos tab content
                    rx.tabs.content(
                        rx.text(
                            "Pavaneswar Das videos for this chapter will be available soon.",
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
                    default_value="verses",
                    width="100%",
                    margin_bottom="64px",
                ),
                
                # Footer Navigation Buttons
                rx.hstack(
                    rx.cond(
                        SBChapterState.prev_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("arrow-left", size=16),
                                    rx.text(SBChapterState.prev_link["title"]),
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
                            href=SBChapterState.prev_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no prev link
                    ),
                    rx.spacer(),
                    rx.cond(
                        SBChapterState.next_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text(SBChapterState.next_link["title"]),
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
                            href=SBChapterState.next_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no next link
                    ),
                    width="100%",
                    padding_top="32px",
                    border_top="1px solid rgba(0,0,0,0.1)",
                ),
                
                width="100%",
                max_width="100%",
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
