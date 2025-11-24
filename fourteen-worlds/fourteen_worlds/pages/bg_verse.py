import reflex as rx
import re
from ..components.header import tovp_header
from ..data.bg_content import bg_chapters
from ..data.bg_verse_content import bg_verse_content

class BGVerseState(rx.State):
    """State for individual verse pages"""
    
    @rx.var
    def chapter_num(self) -> int:
        """Get chapter number from route params"""
        try:
            params = self.router.page.params
            return int(params.get("chapter", 1))
        except:
            return 1
    
    @rx.var
    def verse_num(self) -> str:
        """Get verse number from route params"""
        # Verse number can be "1", "2", or "1-2" sometimes? Usually just number.
        # But let's treat as string to be safe with slugs.
        try:
            params = self.router.page.params
            return params.get("verse", "1")
        except:
            return "1"
            
    @rx.var
    def chapter_title(self) -> str:
        """Get full Chapter title"""
        for chapter in bg_chapters:
            if chapter.get("is_chapter") and chapter.get("number") == self.chapter_num:
                return chapter["title"]
        return f"Chapter {self.chapter_num}"
    
    @rx.var
    def verse_id(self) -> str:
        """Create verse ID for lookup"""
        return f"{self.chapter_num}-{self.verse_num}"
    
    @rx.var
    def has_content(self) -> bool:
        """Check if verse content is available locally"""
        return self.verse_id in bg_verse_content
    
    @rx.var
    def content(self) -> dict:
        """Get verse content"""
        return bg_verse_content.get(self.verse_id, {})
    
    @rx.var
    def devanagari_lines(self) -> list:
        """Get Devanagari text as list of lines"""
        content = self.content
        if content and "sanskrit_devanagari" in content:
            dev = content["sanskrit_devanagari"]
            return dev if isinstance(dev, list) else [dev]
        return []
    
    @rx.var
    def transliterated_lines(self) -> list:
        """Get transliterated Sanskrit as list of lines"""
        content = self.content
        if content and "sanskrit_transliterated" in content:
            trans = content["sanskrit_transliterated"]
            return trans if isinstance(trans, list) else [trans]
        return []
    
    @rx.var
    def synonyms_html(self) -> str:
        """Format synonyms with HTML styling to match Vedabase"""
        content = self.content
        if not content or "synonyms" not in content:
            return ""
        
        text = content["synonyms"]
        # Pattern: word—definition
        pattern = r'([^;—]+)—([^;]+)'
        
        def replace_match(match):
            word = match.group(1).strip()
            definition = match.group(2).strip()
            return f'<span style="color:#b85c00;font-style:italic">{word}</span>—{definition}'
        
        result = re.sub(pattern, replace_match, text)
        return result

    @rx.var
    def purport_paragraphs(self) -> list[str]:
        """Get purport text split into paragraphs"""
        c = self.content
        if c and "purport" in c:
            return c["purport"].split("\n\n")
        return []
    
    @rx.var
    def prev_verse_link(self) -> dict | None:
        """Get previous verse link data"""
        from ..data.bg_content import bg_verses_metadata
        
        # Get current verse number as int
        try:
            current_num = int(self.verse_num)
        except:
            return None
            
        # If verse 1, link back to chapter page
        if current_num == 1:
            return {
                "title": self.chapter_title,
                "url": f"/library/bg/{self.chapter_num}"
            }
        
        # Link to previous verse
        prev_num = current_num - 1
        verses = bg_verses_metadata.get(self.chapter_num, [])
        for verse in verses:
            if verse.get("number") == str(prev_num):
                return {
                    "title": f"TEXT {prev_num}",
                    "url": f"/library/bg/{self.chapter_num}/{prev_num}"
                }
        
        return None
    
    @rx.var
    def next_verse_link(self) -> dict | None:
        """Get next verse link data"""
        from ..data.bg_content import bg_verses_metadata
        
        # Get current verse number as int
        try:
            current_num = int(self.verse_num)
        except:
            return None
        
        # Link to next verse
        next_num = current_num + 1
        verses = bg_verses_metadata.get(self.chapter_num, [])
        for verse in verses:
            if verse.get("number") == str(next_num):
                return {
                    "title": f"TEXT {next_num}",
                    "url": f"/library/bg/{self.chapter_num}/{next_num}"
                }
        
        return None


def bg_verse_page() -> rx.Component:
    return rx.vstack(
        tovp_header(),
        
        # Content Container - Exact Vedabase styling
        rx.box(
            rx.vstack(
                # Breadcrumb navigation
                rx.hstack(
                    rx.link(
                        "Library",
                        href="/library",
                        color="#c17d3a",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="15px",
                        font_family="Georgia, 'Times New Roman', Times, serif",
                    ),
                    rx.text("»", color="#999", font_size="15px"),
                    rx.link(
                        "Bhagavad-gītā As It Is",
                        href="/library/bg",
                        color="#c17d3a",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="15px",
                        font_family="Georgia, 'Times New Roman', Times, serif",
                    ),
                    rx.text("»", color="#999", font_size="15px"),
                    rx.link(
                        BGVerseState.chapter_title,
                        href=f"/library/bg/{BGVerseState.chapter_num}",
                        color="#c17d3a",
                        text_decoration="none",
                        _hover={"text_decoration": "underline"},
                        font_size="15px",
                        font_family="Georgia, 'Times New Roman', Times, serif",
                    ),
                    spacing="2",
                    margin_bottom="24px",
                    flex_wrap="wrap",
                ),
                
                # Main heading - Vedabase exact
                rx.heading(
                    f"BG {BGVerseState.chapter_num}.{BGVerseState.verse_num}",
                    font_size="3rem",
                    font_weight="300",
                    font_family="Georgia, 'Times New Roman', Times, serif",
                    margin_bottom="56px",
                    text_align="center",
                    width="100%",
                    color="#1a1a1a",
                ),
                
                # Show content if available
                rx.cond(
                    BGVerseState.has_content,
                    # Display local content - Exact Vedabase match
                    rx.vstack(
                        # Devanagari section  
                        rx.vstack(
                            rx.heading(
                                "Devanagari",
                                font_size="20px",
                                font_weight="700",
                                margin_bottom="24px",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                color="#1a1a1a",
                            ),
                            rx.vstack(
                                rx.foreach(
                                    BGVerseState.devanagari_lines,
                                    lambda line: rx.text(
                                        line,
                                        font_size="26px",
                                        line_height="2.25",
                                        color="#000000",
                                        text_align="center",
                                        font_family="'Noto Serif Devanagari', serif",
                                        width="100%",
                                    )
                                ),
                                spacing="0",
                                width="100%",
                            ),
                            align="start",
                            width="100%",
                            padding_bottom="40px",
                            border_bottom="2px dashed rgba(150, 100, 50, 0.15)",
                        ),
                        
                        # Verse text section
                        rx.vstack(
                            rx.heading(
                                "Verse text",
                                font_size="20px",
                                font_weight="700",
                                margin_bottom="24px",
                                margin_top="40px",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                color="#1a1a1a",
                            ),
                            rx.vstack(
                                rx.foreach(
                                    BGVerseState.transliterated_lines,
                                    lambda line: rx.text(
                                        line,
                                        font_size="20px",
                                        line_height="2.125",
                                        color="#000000",
                                        text_align="center",
                                        font_style="italic",
                                        font_family="Georgia, 'Times New Roman', Times, serif",
                                        width="100%",
                                    )
                                ),
                                spacing="0",
                                width="100%",
                            ),
                            align="start",
                            width="100%",
                            padding_bottom="40px",
                            border_bottom="2px dashed rgba(150, 100, 50, 0.15)",
                        ),
                        
                        # Synonyms section - with colored HTML
                        rx.vstack(
                            rx.heading(
                                "Synonyms",
                                font_size="20px",
                                font_weight="700",
                                margin_bottom="24px",
                                margin_top="40px",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                color="#1a1a1a",
                            ),
                            rx.html(
                                BGVerseState.synonyms_html,
                                font_size="17px",
                                line_height="2",
                                color="#000000",
                                text_align="justify",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                width="100%",
                            ),
                            align="start",
                            width="100%",
                            padding_bottom="40px",
                            border_bottom="2px dashed rgba(150, 100, 50, 0.15)",
                        ),
                        
                        # Translation section
                        rx.vstack(
                            rx.heading(
                                "Translation",
                                font_size="20px",
                                font_weight="700",
                                margin_bottom="24px",
                                margin_top="40px",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                color="#1a1a1a",
                            ),
                            rx.text(
                                BGVerseState.content["translation"],
                                font_size="19px",
                                line_height="2",
                                color="#000000",
                                text_align="justify",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                            ),
                            align="start",
                            width="100%",
                            padding_bottom="40px",
                            border_bottom="2px dashed rgba(150, 100, 50, 0.15)",
                        ),
                        
                        # Purport section - with left border
                        rx.vstack(
                            rx.heading(
                                "Purport",
                                font_size="20px",
                                font_weight="700",
                                margin_bottom="24px",
                                margin_top="40px",
                                font_family="Georgia, 'Times New Roman', Times, serif",
                                color="#1a1a1a",
                            ),
                            rx.box(
                                rx.foreach(
                                    BGVerseState.purport_paragraphs,
                                    lambda para: rx.text(
                                        para,
                                        font_size="17px",
                                        line_height="1.8",
                                        color="#000000",
                                        text_align="justify",
                                        font_family="Georgia, 'Times New Roman', Times, serif",
                                        margin_bottom="16px",
                                    )
                                ),
                                border_left="3px solid #d4a574",
                                padding_left="24px",
                                width="100%",
                            ),
                            align="start",
                            width="100%",
                            padding_bottom="32px",
                        ),
                        
                        spacing="0",
                        width="100%",
                    ),
                    # Show Vedabase link if content not available
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Content Not Available Locally",
                                size="6",
                                color="#333",
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "This verse hasn't been added to the local database yet.",
                                color="#666",
                                margin_bottom="2rem",
                            ),
                            rx.link(
                                rx.button(
                                    rx.hstack(
                                        rx.icon("external-link", size=16),
                                        rx.text(f"View BG {BGVerseState.chapter_num}.{BGVerseState.verse_num} on Vedabase.io"),
                                        spacing="2",
                                    ),
                                    color_scheme="brown",
                                    size="3",
                                ),
                                href=f"https://vedabase.io/en/library/bg/{BGVerseState.chapter_num}/{BGVerseState.verse_num}/",
                                is_external=True,
                            ),
                            spacing="4",
                            align="center",
                            padding="3rem",
                        ),
                        background="#ffffff",
                        border="1px solid #e0e0e0",
                        border_radius="8px",
                        padding="2rem",
                    ),
                ),
                
                # Footer Navigation Buttons - Vedabase style
                rx.hstack(
                    rx.cond(
                        BGVerseState.prev_verse_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("arrow-left", size=16),
                                    rx.text(BGVerseState.prev_verse_link["title"]),
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
                            href=BGVerseState.prev_verse_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no prev link
                    ),
                    rx.spacer(),
                    rx.cond(
                        BGVerseState.next_verse_link,
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text(BGVerseState.next_verse_link["title"]),
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
                            href=BGVerseState.next_verse_link["url"],
                            text_decoration="none",
                        ),
                        rx.box(), # Empty box if no next link
                    ),
                    width="100%",
                    padding_top="32px",
                    border_top="1px solid rgba(0,0,0,0.1)",
                    margin_top="32px",
                ),
                
                width="100%",
                max_width="896px",  # Exact Vedabase width
                padding="48px 40px",  # Exact Vedabase padding
                spacing="0",
            ),
            width="100%",
            display="flex",
            justify_content="center",
            background="#f5e6d3",  # Exact Vedabase cream
            min_height="100vh",
            padding_y="32px",
        ),
        
        width="100%",
        min_height="100vh",
        spacing="0",
    )
