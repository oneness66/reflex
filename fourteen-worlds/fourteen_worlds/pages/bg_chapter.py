import reflex as rx
from ..components.header import tovp_header
from ..data.bg_content import bg_chapters, bg_verses_metadata
from ..data.bg_verse_content import bg_verse_content

class BGChapterState(rx.State):
    @rx.var
    def chapter_num(self) -> int:
        try:
            return int(self.router.page.params.get("chapter", 1))
        except:
            return 1

    @rx.var
    def verses(self) -> list[dict]:
        # Get verses metadata for this chapter
        base_verses = bg_verses_metadata.get(self.chapter_num, [])
        
        # Merge with translation data
        enhanced_verses = []
        for verse in base_verses:
            # Construct key for verse_content (e.g., "1-1")
            verse_key = f"{self.chapter_num}-{verse['number']}"
            content = bg_verse_content.get(verse_key, {})
            
            enhanced_verse = verse.copy()
            enhanced_verse["translation"] = content.get("translation", "")
            enhanced_verses.append(enhanced_verse)
            
        return enhanced_verses
        
    @rx.var
    def chapter_data(self) -> dict:
        # Find chapter data in bg_chapters list
        for chapter in bg_chapters:
            if chapter.get("is_chapter") and chapter.get("number") == self.chapter_num:
                return chapter
        return {"title": f"Chapter {self.chapter_num}"}

    @rx.var
    def prev_link(self) -> dict:
        """Get previous link data (title, url)"""
        if self.chapter_num == 1:
            # Link to BG Main page
            return {"title": "Bhagavad-gītā As It Is", "url": "/library/bg"}
        else:
            # Link to previous chapter
            prev_num = self.chapter_num - 1
            for chapter in bg_chapters:
                if chapter.get("is_chapter") and chapter.get("number") == prev_num:
                    return {"title": chapter["title"], "url": f"/library/bg/{prev_num}"}
            return None

    @rx.var
    def next_link(self) -> dict:
        """Get next link data (title, url)"""
        next_num = self.chapter_num + 1
        for chapter in bg_chapters:
            if chapter.get("is_chapter") and chapter.get("number") == next_num:
                return {"title": chapter["title"], "url": f"/library/bg/{next_num}"}
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
        href=f"/library/bg/{BGChapterState.chapter_num}/{verse['slug']}", # Local link
        text_decoration="none",
        width="100%",
        _hover={"text_decoration": "none"},
    )

def verse_link_sanskrit(verse: dict) -> rx.Component:
    return rx.link(
        rx.box(
            rx.text(
                verse["title"],
                font_family="Georgia, 'Times New Roman', Times, serif",
                font_size="1.2rem",
                color="#c0392b",  # Vedabase reddish-brown
                font_weight="400",
                display="block", # Block display for Sanskrit only view
                line_height="1.6",
            ),
            width="100%",
            margin_bottom="16px",
            display="block",
        ),
        href=f"/library/bg/{BGChapterState.chapter_num}/{verse['slug']}", # Local link
        text_decoration="none",
        width="100%",
        _hover={"text_decoration": "none"},
    )

def bg_chapter_page() -> rx.Component:
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
                        "Bhagavad-gītā As It Is",
                        href="/library/bg",
                        color="#c0392b",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="14px",
                    ),
                    rx.text("»", color="#666", font_size="14px"),
                    rx.text(
                        BGChapterState.chapter_data["title"],
                        color="#c0392b",
                        font_size="14px",
                    ),
                    spacing="2",
                    margin_bottom="24px",
                    width="100%",
                    flex_wrap="wrap",
                ),
                
                # Chapter Title
                rx.heading(
                    BGChapterState.chapter_data["title"],
                    font_size="3rem",
                    font_weight="700",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    margin_bottom="48px",
                    text_align="center",
                    width="100%",
                    color="#000000",
                ),
                
                # Tabbed interface for Verses and other content
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
                            on_click=rx.call_script("document.querySelector('.bg-chapter-tab-scroll-container').scrollBy({left: -200, behavior: 'smooth'})"),
                            padding="0.75rem 1rem",
                            _hover={"background_color": "rgba(0,0,0,0.1)"},
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        # Scrollable tabs list
                        rx.tabs.list(
                            rx.tabs.trigger(
                                "Srila Prabhupada",
                                value="prabhupada",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            rx.tabs.trigger(
                                "Original Sanskrit",
                                value="sanskrit",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            rx.tabs.trigger(
                                "Other Translations",
                                value="other_translations",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            rx.tabs.trigger(
                                "Commentaries",
                                value="commentaries",
                                color="white",
                                background_color="transparent",
                                padding="0.5rem 1rem",
                                white_space="nowrap",
                                _hover={"background_color": "rgba(255,255,255,0.1)"},
                                _selected={"background_color": "rgba(0,0,0,0.2)", "font_weight": "bold"},
                            ),
                            rx.tabs.trigger(
                                "Sri Sampati Dasa Videos",
                                value="videos",
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
                            class_name="bg-chapter-tab-scroll-container",
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
                            on_click=rx.call_script("document.querySelector('.bg-chapter-tab-scroll-container').scrollBy({left: 200, behavior: 'smooth'})"),
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
                    # Srila Prabhupada tab content
                    rx.tabs.content(
                        rx.vstack(
                            rx.foreach(BGChapterState.verses, verse_link),
                            spacing="4",
                            width="100%",
                            align="start",
                            padding="1.5rem",
                        ),
                        value="prabhupada",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Original Sanskrit tab content
                    rx.tabs.content(
                        rx.vstack(
                            rx.foreach(BGChapterState.verses, verse_link_sanskrit),
                            spacing="4",
                            width="100%",
                            align="start",
                            padding="1.5rem",
                        ),
                        value="sanskrit",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Other Translations tab content
                    rx.tabs.content(
                        rx.text(
                            "Other translations will be available soon.",
                            padding="2rem",
                            color="gray",
                            font_family="Georgia, 'Times New Roman', Times, serif",
                        ),
                        value="other_translations",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Commentaries tab content
                    rx.tabs.content(
                        rx.text(
                            "Commentaries will be available soon.",
                            padding="2rem",
                            color="gray",
                            font_family="Georgia, 'Times New Roman', Times, serif",
                        ),
                        value="commentaries",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    # Videos tab content
                    rx.tabs.content(
                        rx.text(
                            "Sri Sampati Dasa videos for this chapter will be available soon.",
                            padding="2rem",
                            color="gray",
                            font_family="Georgia, 'Times New Roman', Times, serif",
                        ),
                        value="videos",
                        background_color="white",
                        border_radius="0 0 8px 8px",
                        border="1px solid #e0e0e0",
                        width="100%",
                    ),
                    default_value="prabhupada",
                    width="100%",
                    margin_bottom="64px",
                ),
                
                # Footer Navigation Buttons
                rx.hstack(
                    rx.cond(
                        BGChapterState.prev_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("arrow-left", size=16),
                                    rx.text(BGChapterState.prev_link["title"]),
                                    spacing="2",
                                    align="center",
                                ),
                                bg="#e6d0b3",
                                color="#000",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                font_size="14px",
                                padding="12px 20px",
                                border_radius="6px",
                                _hover={"bg": "#d4a574"},
                                cursor="pointer",
                            ),
                            href=BGChapterState.prev_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no prev link
                    ),
                    rx.spacer(),
                    rx.cond(
                        BGChapterState.next_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text(BGChapterState.next_link["title"]),
                                    rx.icon("arrow-right", size=16),
                                    spacing="2",
                                    align="center",
                                ),
                                bg="#e6d0b3",
                                color="#000",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                font_size="14px",
                                padding="12px 20px",
                                border_radius="6px",
                                _hover={"bg": "#d4a574"},
                                cursor="pointer",
                            ),
                            href=BGChapterState.next_link["url"],
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
