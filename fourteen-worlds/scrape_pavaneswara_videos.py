"""
Script to extract video URLs from Pavaneswara Das YouTube playlist using yt-dlp
Playlist: https://www.youtube.com/playlist?list=PLstzwZvVxLU1u2OysLliY5faZVOCwe4R9
"""
import yt_dlp
import json
import os

# Pavaneswara Das Playlist
playlist_id = "PLstzwZvVxLU1u2OysLliY5faZVOCwe4R9"
playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
output_file = "pavaneswara_videos.json"

print(f"Extracting playlist: {playlist_url}")
print("This may take a moment...\n")

# Configure yt-dlp options
ydl_opts = {
    'quiet': True,
    'extract_flat': 'in_playlist',  # Extract all videos in playlist
    'skip_download': True,
    'no_warnings': False,
    'ignoreerrors': True,
}

videos = []

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract playlist info
        result = ydl.extract_info(playlist_url, download=False)
        
        if result and 'entries' in result:
            playlist_title = result.get('title', 'Pavaneswara Das Videos')
            print(f"Playlist: {playlist_title}")
            print(f"Found {len(result['entries'])} videos\n")
            
            for i, entry in enumerate(result['entries'], 1):
                if entry:
                    video_id = entry.get('id', '')
                    title = entry.get('title', 'Unknown')
                    url = entry.get('url', '') or f"https://www.youtube.com/watch?v={video_id}"
                    
                    # If URL is still in form of just ID, construct full URL
                    if not url.startswith('http'):
                        url = f"https://www.youtube.com/watch?v={url}"
                    
                    videos.append({
                        'number': i,
                        'title': title,
                        'url': url,
                        'video_id': video_id,
                        'thumbnail': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                    })
                    
                    print(f"{i}. {title}")
            
            if videos:
                # Save to JSON file
                output_data = {
                    'playlist_id': playlist_id,
                    'playlist_title': playlist_title,
                    'playlist_url': playlist_url,
                    'video_count': len(videos),
                    'videos': videos
                }
                
                # Save to data directory if it exists, otherwise current directory
                save_path = os.path.join("fourteen_worlds", "data", output_file)
                if not os.path.exists(os.path.dirname(save_path)):
                    save_path = output_file
                
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                print(f"\n✓ Success! Saved {len(videos)} video URLs to: {save_path}")
            else:
                print("No videos were extracted from the playlist")
        else:
            print("Could not extract playlist information")
            
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
