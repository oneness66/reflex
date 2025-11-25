import os
from pathlib import Path
import reflex as rx
from ..components.header import tovp_header
from ..state import State

# Paths to scan for photos
ASSETS_ROOT = Path(__file__).parent.parent.parent / "assets"
PHOTO_DIRS = [
    ASSETS_ROOT / "bhu-mandala",
    ASSETS_ROOT / "bhu-mandala" / "fotos",
    ASSETS_ROOT / "bhu-mandala" / "img",
]

import json
from typing import List, Dict, Optional

class Article(rx.Base):
    id: Optional[str] = None
    title: str
    author: Optional[str] = None
    reading_time: str
    date: str
    image: Optional[str] = None
    category: Optional[str] = None
    path: Optional[str] = None
    description: Optional[str] = None
    is_premium: bool
    url: str
    content: str = ""

class Issue(rx.Base):
    issue: str
    cover_image: str
    articles: List[Article]

# Load magazine data
def load_magazine_data() -> List[Issue]:
    try:
        data_path = Path(__file__).parent.parent.parent / "btg_magazine_data.json"
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Issue(**item) for item in data]
    except Exception as e:
        print(f"Error loading magazine data: {e}")
    return []

class BTGState(State):
    """State for the BTG magazine page."""
    selected_photo: str = ""
    selected_issue: Optional[Issue] = None
    selected_article: Optional[Article] = None
    magazine_data: List[Issue] = load_magazine_data()

    def set_selected_photo(self, url: str):
        self.selected_photo = url

    def clear_selected_photo(self):
        self.selected_photo = ""
        
    def open_issue(self, issue: Issue):
        self.selected_issue = issue
        self.selected_article = None
        
    def close_issue(self):
        self.selected_issue = None
        self.selected_article = None
        
    def open_article(self, article: Article):
        if not article.content and article.path:
            try:
                # Construct absolute path
                project_root = Path(__file__).parent.parent.parent
                file_path = project_root / article.path.lstrip("/")
                
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # Try to extract only the article content wrapper
                        # Look for common WordPress/Elementor content containers
                        content_markers = [
                            ('class="tts_content_wrapper', '</div>'),
                            ('data-widget_type="theme-post-content', '</div>'),
                            ('class="elementor-widget-container"', '</div>'),
                        ]
                        
                        extracted = False
                        for start_marker, end_marker in content_markers:
                            if start_marker in content:
                                # Find the start of the content wrapper
                                start_idx = content.find(start_marker)
                                if start_idx != -1:
                                    # Find the opening tag's end
                                    opening_tag_end = content.find('>', start_idx) + 1
                                    # Try to find the next substantial paragraph or content
                                    # Look for <p> or <figure> tags after the opening
                                    content_start = content.find('<p', opening_tag_end)
                                    if content_start == -1:
                                        content_start = content.find('<figure', opening_tag_end)
                                    
                                    if content_start != -1:
                                        # Now find where this content wrapper ends
                                        # We need to carefully find the matching closing div
                                        # For simplicity, let's extract a large chunk and clean it
                                        temp_content = content[content_start:]
                                        
                                        # Remove all WordPress navigation menus and headers
                                        # Look for content until we hit social sharing or related articles
                                        stop_markers = [
                                            'class="heateor_sss_sharing_container',
                                            'Related Articles',
                                            'Table of Contents',
                                            'class="elementor-nav-menu',
                                            'class="elementor-element-778f4279',  # Table of contents element
                                        ]
                                        
                                        end_idx = len(temp_content)
                                        for marker in stop_markers:
                                            marker_pos = temp_content.find(marker)
                                            if marker_pos != -1 and marker_pos < end_idx:
                                                end_idx = marker_pos
                                        
                                        article.content = temp_content[:end_idx]
                                        extracted = True
                                        break
                        
                        # Fallback to body extraction if content wrapper not found
                        if not extracted:
                            if "<body" in content:
                                start = content.find("<body")
                                end = content.find("</body>")
                                if start != -1 and end != -1:
                                    body_tag_end = content.find(">", start) + 1
                                    article.content = content[body_tag_end:end]
                                else:
                                    article.content = content
                            else:
                                article.content = content
            except Exception as e:
                print(f"Error loading article content: {e}")
                article.content = "Error loading content."
                
        self.selected_article = article
        
    def close_article(self):
        self.selected_article = None

def get_photos():
    """Get list of BTG magazine cover images."""
    # This is now primarily used for the cover grid display
    # We'll merge file-based discovery with JSON data
    photos = []
    btg_images_dir = ASSETS_ROOT / "btg_magazine_images"
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    # Load JSON data to map filenames to issues
    # Note: calling load_magazine_data() here again might be redundant if we could access state, 
    # but get_photos is called at compile time/render time for the grid.
    # We'll just load it to get the mapping.
    issues = load_magazine_data()
    issue_map = {item.cover_image.split("/")[-1]: item for item in issues}
    
    # Fallback mapping
    month_year_map = {
        "C1": "November 2025",
        "C2": "October 2025",
        "C3": "September 2025",
        "C4": "August 2025",
        "C5": "July 2025",
        "C6": "June 2025",
        "C7": "May 2025",
        "C8": "April 2025",
        "C9": "March 2025",
        "C10": "February 2025",
        "C11": "January 2025",
        "C12": "December 2024",
    }
    
    if not btg_images_dir.exists():
        return []
    
    try:
        for filename in os.listdir(btg_images_dir):
            if Path(filename).suffix.lower() in valid_extensions:
                url = f"/btg_magazine_images/{filename}"
                issue_name = Path(filename).stem
                
                # Check if we have rich data for this issue
                issue_data = issue_map.get(filename)
                
                title = f"BTG Issue {issue_name}" if issue_name.startswith('C') else filename
                month_year = month_year_map.get(issue_name, title)
                
                if issue_data:
                    month_year = issue_data.issue
                
                photos.append({
                    "url": url,
                    "title": title,
                    "month_year": month_year,
                    "type": "image",
                    "issue_data": issue_data  # Attach full issue data if available
                })
    except Exception as e:
        print(f"Error reading BTG images directory: {e}")
    
    return sorted(photos, key=lambda x: x["title"])

def photo_card(photo: dict) -> rx.Component:
    """Render a BTG magazine cover card."""
    return rx.vstack(
        rx.image(
            src=photo["url"],
            width="100%",
            height="auto",
            max_width="400px",
            object_fit="contain",
            border_radius="4px",
            cursor="pointer",
            box_shadow="0 4px 12px rgba(0,0,0,0.15)",
            _hover={
                "transform": "scale(1.05)",
                "box_shadow": "0 8px 20px rgba(0,0,0,0.25)",
            },
            transition="all 0.3s ease",
            on_click=lambda: BTGState.open_issue(photo.get("issue_data")) if photo.get("issue_data") else State.set_selected_photo(photo["url"]),
        ),
        rx.text(
            photo.get("month_year", photo["title"]), 
            size="5",
            color="#FF6633",
            font_weight="600",
            trim="both",
            width="100%",
            text_align="center",
            margin_top="1rem"
        ),
        width="100%",
        align="center",
        spacing="2",
    )

def article_card(article: Article) -> rx.Component:
    """Render a card for a single article in the list view."""
    return rx.box(
        rx.vstack(
            rx.heading(article.title, size="5", color="#D35400", margin_bottom="0.5rem"),
            rx.cond(
                article.description,
                rx.text(article.description, color="#555", margin_bottom="0.5rem", font_size="0.95rem"),
            ),
            rx.hstack(
                rx.badge("English Premium", color_scheme="orange", variant="solid"),
                rx.text(f"⏱ {article.reading_time}", font_size="0.9rem", color="gray"),
                rx.text(f"📅 {article.date}", font_size="0.9rem", color="gray"),
                spacing="4",
                align_items="center",
            ),
            align_items="start",
            width="100%",
        ),
        padding="1.5rem",
        background="white",
        border_radius="8px",
        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
        width="100%",
        cursor="pointer",
        _hover={"box_shadow": "0 4px 12px rgba(0,0,0,0.1)", "transform": "translateY(-2px)"},
        transition="all 0.2s ease",
        on_click=lambda: BTGState.open_article(article),
    )

def article_list_view() -> rx.Component:
    """Display list of articles for the selected issue."""
    return rx.vstack(
        rx.button(
            "← Back to Issues",
            on_click=BTGState.close_issue,
            variant="ghost",
            color="#000099",
            margin_bottom="1rem",
        ),
        rx.heading(BTGState.selected_issue.issue, size="7", color="#000099", margin_bottom="2rem"),
        rx.vstack(
            rx.foreach(
                BTGState.selected_issue.articles,
                article_card
            ),
            width="100%",
            spacing="4",
        ),
        width="100%",
        max_width="800px",
        padding="2rem",
    )

def article_detail_view() -> rx.Component:
    """Display the full content of the selected article."""
    return rx.vstack(
        rx.button(
            "← Back to Articles",
            on_click=BTGState.close_article,
            variant="ghost",
            color="#000099",
            margin_bottom="1rem",
        ),
        rx.box(
            rx.heading(BTGState.selected_article.title, size="8", color="#2c3e50", margin_bottom="1rem"),
            rx.cond(
                BTGState.selected_article.author,
                rx.text(f"By {BTGState.selected_article.author}", font_style="italic", color="gray", margin_bottom="0.5rem"),
            ),
            rx.hstack(
                rx.text(f"📅 {BTGState.selected_article.date}", color="gray"),
                rx.text(f"⏱ {BTGState.selected_article.reading_time}", color="gray"),
                spacing="4",
                margin_bottom="2rem",
            ),
            rx.cond(
                BTGState.selected_article.image,
                rx.image(src=BTGState.selected_article.image, width="100%", max_height="400px", object_fit="cover", margin_bottom="2rem", border_radius="8px"),
            ),
            rx.cond(
                BTGState.selected_article.path,
                rx.html(BTGState.selected_article.content),
                rx.markdown(
                    BTGState.selected_article.content,
                    color="#333",
                    line_height="1.8",
                    font_size="1.1rem",
                ),
            ),
            padding="3rem",
            background="white",
            border_radius="12px",
            box_shadow="0 4px 20px rgba(0,0,0,0.08)",
            width="100%",
        ),
        width="100%",
        max_width="900px",
        padding="2rem",
        align_items="start",
    )

def lightbox() -> rx.Component:
    """Lightbox modal for viewing photos (fallback)."""
    return rx.cond(
        State.selected_photo != "",
        rx.box(
            rx.box(
                rx.image(
                    src=State.selected_photo,
                    max_height="90vh",
                    max_width="90vw",
                    object_fit="contain",
                ),
                rx.icon(
                    "close",
                    color="white",
                    size=30,
                    position="absolute",
                    top="20px",
                    right="20px",
                    cursor="pointer",
                    on_click=State.clear_selected_photo,
                ),
                position="relative",
                display="flex",
                justify_content="center",
                align_items="center",
                width="100%",
                height="100%",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background="rgba(0, 0, 0, 0.9)",
            z_index="9999",
            display="flex",
            justify_content="center",
            align_items="center",
            on_click=State.clear_selected_photo,
        ),
    )

def photos_page() -> rx.Component:
    """Page displaying the photo gallery."""
    photos = get_photos()
    
    return rx.vstack(
        tovp_header(),
        lightbox(),
        rx.box(
            rx.cond(
                BTGState.selected_article,
                article_detail_view(),
                rx.cond(
                    BTGState.selected_issue,
                    article_list_view(),
                    rx.vstack(
                        rx.heading("Back To Godhead", size="8", color="#000099", margin_bottom="1rem"),
                        rx.text("The Magazine of the Hare Krishna Movement", size="4", color="gray", margin_bottom="2rem"),
                        
                        rx.grid(
                            *[photo_card(photo) for photo in photos],
                            columns=rx.breakpoints(initial="1", sm="2", md="3"),
                            spacing="6",
                            width="100%",
                            justify_items="center",
                        ) if photos else rx.text("No magazine covers found.", color="gray", size="4"),
                        
                        align="center",
                        padding="4rem 2rem",
                        max_width="1400px",
                        margin="0 auto",
                    )
                )
            ),
            width="100%",
            background="#f0f2f5",
            min_height="100vh",
            display="flex",
            justify_content="center",
        ),
        width="100%",
    )
