import json
import os

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "bg_data")
CHAPTERS_FILE = os.path.join(DATA_DIR, "bg_chapters.json")
VERSES_METADATA_FILE = os.path.join(DATA_DIR, "bg_verses_metadata.json")

# Load Chapters
bg_chapters = []
try:
    if os.path.exists(CHAPTERS_FILE):
        with open(CHAPTERS_FILE, "r", encoding="utf-8") as f:
            bg_chapters = json.load(f)
except Exception as e:
    print(f"Error loading BG chapters: {e}")

# Load Verse Metadata
bg_verses_metadata = {}
try:
    if os.path.exists(VERSES_METADATA_FILE):
        with open(VERSES_METADATA_FILE, "r", encoding="utf-8") as f:
            # The JSON keys are strings ("1", "2"), but we might want ints
            data = json.load(f)
            for k, v in data.items():
                bg_verses_metadata[int(k)] = v
except Exception as e:
    print(f"Error loading BG verse metadata: {e}")
