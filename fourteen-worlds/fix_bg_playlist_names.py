"""
Script to update playlist names in bg_sampati_videos.json
"""
import json

# Read the JSON file
with open('bg_sampati_videos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mapping from old playlist names to new ones
playlist_mapping = {
    'Bhagavad Gita Chapter Summary': 'Bhagavad Gita',
    'What Happens after Death': 'Bhagavad Gita Chapter Summary'
}

# Update each video's playlist name and description
for video in data['videos']:
    old_playlist = video.get('playlist', '')
    if old_playlist in playlist_mapping:
        new_playlist = playlist_mapping[old_playlist]
        video['playlist'] = new_playlist
        video['description'] = f"From {new_playlist} series by Sri Sampati Dasa"

# Save updated data
with open('bg_sampati_videos.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Updated {len(data['videos'])} videos")
print(f"  - 'Bhagavad Gita Chapter Summary' → 'Bhagavad Gita'")
print(f"  - 'What Happens after Death' → 'Bhagavad Gita Chapter Summary'")
