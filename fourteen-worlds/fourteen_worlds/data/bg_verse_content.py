import json
import os

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "bg_data")
VERSES_CONTENT_FILE = os.path.join(DATA_DIR, "bg_verses_content.json")

# Load Verse Content
bg_verse_content = {}
try:
    if os.path.exists(VERSES_CONTENT_FILE):
        with open(VERSES_CONTENT_FILE, "r", encoding="utf-8") as f:
            bg_verse_content = json.load(f)
except Exception as e:
    print(f"Error loading BG verse content: {e}")
