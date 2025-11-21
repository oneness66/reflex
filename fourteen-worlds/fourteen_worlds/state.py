import reflex as rx
import re
from pathlib import Path
from .data.worlds_data import get_world_by_id

# Path to bhu-mandala HTML files
BHU_MANDALA_PATH = Path(__file__).parent.parent / "assets" / "bhu-mandala"

class State(rx.State):
    """The app state."""
    selected_world_id: int = 0
    show_detail: bool = False
    
    # For dynamic article routing
    article_content: str = ""
    article_name: str = ""
    
    # For Vedic Science topics
    vedic_topic: str = ""
    
    def select_world(self, world_id: int):
        """Select a world to view details."""
        self.selected_world_id = world_id
        self.show_detail = True
    
    def close_detail(self):
        """Close the detail view."""
        self.show_detail = False
        self.selected_world_id = 0
    
    def load_article_content(self, filename: str):
        """Load article content based on the current article_id from URL."""
        if not filename:
            return
            
        # Ensure filename ends with .html if not present (though links should include it)
        if not filename.endswith('.html'):
            filename += '.html'
            
        article_path = BHU_MANDALA_PATH / filename
        if article_path.exists():
            with open(article_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Remove conflicting elements
                # Remove the background stretch div which obscures content
                content = re.sub(r'<div id="bg-stretch">.*?</div>', '', content, flags=re.DOTALL)
                # Remove original header and nav as we use our own
                content = re.sub(r'<div id="header">.*?</div>', '', content, flags=re.DOTALL)
                content = re.sub(r'<ul id="nav">.*?</ul>', '', content, flags=re.DOTALL)
                
                # Fix relative paths to work with Reflex asset serving
                content = content.replace('src="img/', 'src="/bhu-mandala/img/')
                content = content.replace('href="img/', 'href="/bhu-mandala/img/')
                content = content.replace('src="fotos/', 'src="/bhu-mandala/fotos/')
                content = content.replace('href="fotos/', 'href="/bhu-mandala/fotos/')
                content = content.replace('href="css/', 'href="/bhu-mandala/css/')
                content = content.replace('src="js/', 'src="/bhu-mandala/js/')
                # Fix links to other articles to use the new route structure
                content = content.replace('href="jambudvipa', 'href="/article/jambudvipa')
                content = content.replace('href="articles-overview.html"', 'href="/articles"')
                content = content.replace('href="chapter-index.html"', 'href="/chapters"')
                
                # Inject styles to ensure readability (fix for missing background images)
                style_override = """
                <style>
                .box .content { background: white !important; }
                body { background: none !important; }
                </style>
                """
                content = content.replace('</head>', style_override + '</head>')
                
                self.article_content = content
                self.article_name = filename.replace('.html', '').replace('-', ' ').title()
        else:
            self.article_content = f"<h1>Article not found: {filename}</h1>"

    def load_article_from_url(self):
        """Load article content using the filename from the URL router params."""
        args = self.router.page.params
        filename = args.get("filename", "")
        if filename:
            self.load_article_content(filename)

    def load_vedic_topic(self):
        """Load the vedic topic from the URL."""
        topic = self.router.page.params.get("topic", "")
        if topic:
            self.vedic_topic = topic.replace("-", " ").title()
        else:
            self.vedic_topic = "Vedic Science Topic"

    
    @rx.var
    def selected_world(self) -> dict:
        """Get the currently selected world data."""
        if self.selected_world_id > 0:
            return get_world_by_id(self.selected_world_id)
        return {}

    # Photo Gallery State
    selected_photo: str = ""

    def set_selected_photo(self, url: str):
        """Set the selected photo for the lightbox."""
        self.selected_photo = url

    def clear_selected_photo(self):
        """Clear the selected photo to close the lightbox."""
        self.selected_photo = ""
