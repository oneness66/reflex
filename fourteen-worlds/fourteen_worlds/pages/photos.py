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

def get_photos():
    """Get list of photo dictionaries from all directories."""
    photos = []
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    seen_files = set()
    
    for directory in PHOTO_DIRS:
        if not directory.exists():
            continue
            
        try:
            for filename in os.listdir(directory):
                if Path(filename).suffix.lower() in valid_extensions:
                    if filename in seen_files:
                        continue
                    
                    # Determine relative URL path
                    # If dir is .../bhu-mandala, url is /bhu-mandala/filename
                    # If dir is .../bhu-mandala/fotos, url is /bhu-mandala/fotos/filename
                    rel_path = directory.relative_to(ASSETS_ROOT).as_posix()
                    url = f"/{rel_path}/{filename}"
                    
                    photos.append({
                        "url": url,
                        "title": filename,
                        "type": "image"
                    })
                    seen_files.add(filename)
        except Exception as e:
            print(f"Error reading directory {directory}: {e}")
            
    return sorted(photos, key=lambda x: x["title"])

def photo_card(photo: dict) -> rx.Component:
    """Render a single photo card."""
    return rx.vstack(
        rx.image(
            src=photo["url"],
            width="100%",
            height="200px",
            object_fit="cover",
            border_radius="8px",
            cursor="pointer",
            _hover={
                "transform": "scale(1.02)",
                "filter": "brightness(1.1)",
            },
            transition="all 0.3s ease",
            on_click=lambda: State.set_selected_photo(photo["url"]),
        ),
        rx.text(
            photo["title"], 
            size="1", 
            color="gray", 
            trim="both",
            width="100%",
            text_align="center",
            margin_top="0.5rem"
        ),
        width="100%",
        align="center",
    )

def lightbox() -> rx.Component:
    """Lightbox modal for viewing photos."""
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
            rx.vstack(
                rx.heading("Photo Gallery", size="8", color="#000099", margin_bottom="1rem"),
                rx.text("Visual journey through the Fourteen Worlds.", size="4", color="gray", margin_bottom="2rem"),
                
                rx.grid(
                    *[photo_card(photo) for photo in photos],
                    columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4", xl="5"),
                    spacing="4",
                    width="100%",
                ) if photos else rx.text("No photos found.", color="red"),
                
                align="center",
                padding="4rem 2rem",
                max_width="1600px",
                margin="0 auto",
            ),
            width="100%",
            background="#f0f2f5",
            min_height="100vh",
        ),
        width="100%",
    )
