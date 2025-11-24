"""
Script to extract video URLs from YouTube playlist using yt-dlp with direct playlist URL
"""
import yt_dlp
import json

# Try with direct playlist URL
playlist_id = "PLR9NxMJ4tXf30EWwBe1HX692JzBDdIRIq"
playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

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
            playlist_title = result.get('title', 'Unknown Playlist')
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
                        'video_id': video_id
                    })
                    
                    print(f"{i}. {title}")
                    print(f"   {url}\n")
            
            if videos:
                # Save to JSON file
                output_data = {
                    'playlist_id': playlist_id,
                    'playlist_title': playlist_title,
                    'playlist_url': playlist_url,
                    'video_count': len(videos),
                    'videos': videos
                }
                
                with open('youtube_playlist_urls.json', 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2, ensure_ascii=False)
                
                # Save as plain text file with just URLs
                with open('youtube_playlist_urls.txt', 'w', encoding='utf-8') as f:
                    for video in videos:
                        f.write(f"{video['url']}\n")
                
                print(f"\n✓ Success! Saved {len(videos)} video URLs to:")
                print("  - youtube_playlist_urls.json (detailed info)")
                print("  - youtube_playlist_urls.txt (URLs only)")
            else:
                print("No videos were extracted from the playlist")
        else:
            print("Could not extract playlist information")
            print("This might be because:")
            print("  - The playlist is private or unlisted")
            print("  - The playlist ID is incorrect")
            print("  - There's a network issue")
            
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
