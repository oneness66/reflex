"""
Script to extract videos from multiple Sri Sampati Dasa playlists for BG
"""
import yt_dlp
import json

playlists = [
    {
        "name": "Bhagavad Gita Chapter Summary",
        "url": "https://www.youtube.com/watch?v=FjqmOE-pGmw&list=PLR9NxMJ4tXf3_ICriMu_FmZJsWwcZWZKM",
        "playlist_id": "PLR9NxMJ4tXf3_ICriMu_FmZJsWwcZWZKM"
    },
    {
        "name": "What Happens after Death",
        "url": "https://www.youtube.com/watch?v=EdIy-Y4BRfA&list=PLR9NxMJ4tXf2tKSq9wCHkyS1qvIVtKzx9",
        "playlist_id": "PLR9NxMJ4tXf2tKSq9wCHkyS1qvIVtKzx9"
    }
]

# Configure yt-dlp options
ydl_opts = {
    'quiet': True,
    'extract_flat': 'in_playlist',
    'skip_download': True,
    'no_warnings': False,
    'ignoreerrors': True,
}

all_videos = []

for playlist_info in playlists:
    playlist_url = f"https://www.youtube.com/playlist?list={playlist_info['playlist_id']}"
    
    print(f"\nExtracting: {playlist_info['name']}")
    print(f"URL: {playlist_url}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            
            if result and 'entries' in result:
                playlist_title = result.get('title', playlist_info['name'])
                print(f"Found {len(result['entries'])} videos\n")
                
                videos = []
                for i, entry in enumerate(result['entries'], 1):
                    if entry:
                        video_id = entry.get('id', '')
                        title = entry.get('title', 'Unknown')
                        url = entry.get('url', '') or f"https://www.youtube.com/watch?v={video_id}"
                        
                        if not url.startswith('http'):
                            url = f"https://www.youtube.com/watch?v={url}"
                        
                        video_data = {
                            'title': title,
                            'url': url,
                            'video_id': video_id,
                            'playlist': playlist_info['name'],
                            'duration': '',
                            'description': f"From {playlist_info['name']} series by Sri Sampati Dasa"
                        }
                        
                        videos.append(video_data)
                        all_videos.append(video_data)
                        
                        print(f"{i}. {title}")
                
                print(f"\n✓ Extracted {len(videos)} videos from {playlist_info['name']}")
            else:
                print("Could not extract playlist information")
                
    except Exception as e:
        print(f"Error: {e}")

# Save all videos to JSON
if all_videos:
    output_data = {
        'total_videos': len(all_videos),
        'playlists': [p['name'] for p in playlists],
        'videos': all_videos
    }
    
    with open('bg_sampati_videos.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Success! Saved {len(all_videos)} total videos to bg_sampati_videos.json")
else:
    print("\nNo videos were extracted")
