#!/usr/bin/env python3
"""
🎵 Spotify Playlist & Album Downloader

Complete Spotify Downloader with High-Quality Audio & Metadata

This downloader provides robust playlist and album downloading with comprehensive error handling.

Features:
- Playlist & Album support - Download both playlists and full albums
- High-quality audio downloads (up to 320kbps)
- Complete metadata including album art and lyrics
- Flexible fallback options for maximum success rate
- Smart error handling and recovery

💡 Download your favorite Spotify playlists and albums with ease!
"""

import os
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
import tempfile
import time


def get_value(obj: Any, key: str, default: Any = None) -> Any:
    """Safely get values from objects with fallback support"""
    try:
        if isinstance(obj, dict):
            return obj.get(key, default)
        elif hasattr(obj, key):
            return getattr(obj, key, default)
        else:
            return default
    except:
        return default


def get_nested_value(obj: Any, *keys: str, default: Any = None) -> Any:
    """Get nested values with safe navigation"""
    try:
        current = obj
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, {})
            elif hasattr(current, key):
                current = getattr(current, key, {})
            else:
                return default
        return current if current != {} else default
    except:
        return default


def format_list_as_string(obj: Any, separator: str = ", ") -> str:
    """Convert objects to readable string format"""
    try:
        if isinstance(obj, list):
            return separator.join(str(item) for item in obj if item)
        elif isinstance(obj, str):
            return obj
        else:
            return str(obj) if obj else "Unknown"
    except:
        return "Unknown"


class SpotifyPlaylistDownloader:
    def __init__(self, output_dir: str = "Downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        print(f"🎵 Spotify Playlist & Album Downloader initialized!")
    
    def clean_filename(self, filename: str) -> str:
        """Clean filename for filesystem compatibility"""
        try:
            filename = re.sub(r'[<>:"/\\|?*]', '_', str(filename))
            filename = re.sub(r'[^\w\s\-_\.]', '_', filename)
            return filename.strip()[:200]
        except:
            return "unknown_file"
    
    def is_valid_spotify_url(self, url: str) -> bool:
        """Validate Spotify playlist or album URL"""
        try:
            url_lower = str(url).lower()
            return ('spotify.com/playlist/' in url_lower or 
                    'spotify.com/album/' in url_lower)
        except:
            return False
    
    def get_url_type(self, url: str) -> str:
        """Determine if URL is playlist or album"""
        try:
            url_lower = str(url).lower()
            if 'spotify.com/playlist/' in url_lower:
                return "playlist"
            elif 'spotify.com/album/' in url_lower:
                return "album"
            else:
                return "unknown"
        except:
            return "unknown"
    
    def fetch_playlist_data(self, spotify_url: str) -> Optional[Dict]:
        """Fetch playlist or album metadata using spotdl"""
        try:
            url_type = self.get_url_type(spotify_url)
            print(f"🔍 Fetching {url_type} metadata...")
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.spotdl', delete=False)
            temp_file.close()
            
            cmd = ['spotdl', 'save', str(spotify_url), '--save-file', temp_file.name]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            with open(temp_file.name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            os.unlink(temp_file.name)
            
            # Handle both dictionary and list formats from spotdl
            if isinstance(data, dict):
                print("✅ Metadata loaded successfully (dictionary format)")
                return data
            elif isinstance(data, list):
                print("🔧 Converting list format to expected structure")
                collection_name = self.extract_collection_name(spotify_url)
                converted_data = {
                    'name': collection_name,
                    'songs': data,
                    'url': spotify_url,
                    'type': url_type
                }
                print(f"✅ Processed {len(data)} songs successfully")
                return converted_data
            else:
                print(f"⚠️ Warning: Unexpected data format: {type(data)}")
                return None
            
        except Exception as e:
            print(f"❌ Error fetching metadata: {e}")
            return None
    
    def extract_collection_name(self, url: str) -> str:
        """Extract or generate collection name from URL (playlist or album)"""
        try:
            url_type = self.get_url_type(url)
            if 'playlist/' in url:
                playlist_id = url.split('playlist/')[-1].split('?')[0]
                return f"Spotify_Playlist_{playlist_id[:8]}"
            elif 'album/' in url:
                album_id = url.split('album/')[-1].split('?')[0]
                return f"Spotify_Album_{album_id[:8]}"
            else:
                return f"Spotify_{url_type.title()}"
        except:
            return "Downloaded_Collection"
    
    def extract_track_details(self, track: Any) -> tuple:
        """Extract track information from various data structures"""
        try:
            title = "Unknown"
            artists = []
            spotify_url = ""
            
            # Handle different track data structures
            if isinstance(track, dict):
                title = get_value(track, 'name', 'Unknown')
                artists = get_value(track, 'artists', [])
                spotify_url = get_value(track, 'url', '')
                
            elif isinstance(track, list) and len(track) > 0:
                first_item = track[0] if track else {}
                if isinstance(first_item, dict):
                    title = get_value(first_item, 'name', 'Unknown')
                    artists = get_value(first_item, 'artists', [])
                    spotify_url = get_value(first_item, 'url', '')
                else:
                    title = format_list_as_string(track)
            
            # Ensure valid title
            if not title or title == "Unknown":
                title = f"Track_{id(track)}"
            
            artist_str = format_list_as_string(artists)
            return title, artist_str, spotify_url
            
        except Exception as e:
            print(f"⚠️ Error extracting track details: {e}")
            return "Unknown", "Unknown", ""
    
    def download_with_ytdlp_fallback(self, video_url: str, output_path: str, track_info: tuple) -> bool:
        """Fallback download with yt-dlp for high quality audio"""
        try:
            title, artist_str, _ = track_info
            
            cmd = [
                'yt-dlp',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--audio-quality', '320K',
                '--embed-metadata',
                '--add-metadata',
                '--no-warnings',
                '--write-thumbnail',
                '--embed-thumbnail',
                '-o', str(output_path),
                str(video_url)
            ]
            
            print(f"⬇️ Fallback download: {artist_str} - {title}")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
            
        except Exception:
            return False
    
    def download_with_spotdl_primary(self, track_url: str, output_dir: str, track_info: tuple) -> bool:
        """Primary download method using spotdl"""
        try:
            title, artist_str, _ = track_info
            
            cmd = [
                'spotdl', 'download', str(track_url),
                '--output', str(output_dir),
                '--format', 'mp3',
                '--bitrate', '320k',
                '--embed-metadata',
                '--generate-lrc',
                '--save-cover'  # This should include album art
            ]
            
            print(f"⬇️ Downloading: {artist_str} - {title}")
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
            
        except Exception:
            # Try with fallback options
            try:
                cmd_fallback = [
                    'spotdl', 'download', str(track_url),
                    '--output', str(output_dir),
                    '--format', 'mp3',
                    '--bitrate', '320k'
                ]
                subprocess.run(cmd_fallback, capture_output=True, text=True, check=True)
                return True
            except Exception:
                return False
    
    def search_youtube_track(self, artist: str, title: str) -> Optional[str]:
        """Search YouTube for track using yt-dlp"""
        try:
            search_query = f"ytsearch3:{artist} - {title}"
            cmd = ['yt-dlp', '--quiet', '--dump-json', '--playlist-end', '3', search_query]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        video = json.loads(line)
                        return get_value(video, 'webpage_url')
                    except:
                        continue
            return None
        except:
            return None
    
    def download_collection(self, spotify_url: str) -> bool:
        """Download complete playlist or album with error handling"""
        try:
            url_type = self.get_url_type(spotify_url)
            print(f"🎵 Processing {url_type}: {spotify_url}")
            
            # Get metadata
            metadata = self.fetch_playlist_data(spotify_url)
            if not metadata:
                print(f"❌ Failed to fetch {url_type} metadata")
                return False
            
            # Extract collection information
            collection_name = get_value(metadata, 'name', f'Unknown {url_type.title()}')
            tracks = get_value(metadata, 'songs', [])
            
            if not tracks:
                print(f"❌ No tracks found in {url_type}")
                return False
            
            print(f"📂 {url_type.title()}: {collection_name}")
            print(f"🎵 Total tracks: {len(tracks)}")
            
            # Create output folder
            folder = self.output_dir / self.clean_filename(collection_name)
            folder.mkdir(exist_ok=True)
            
            # Save metadata
            try:
                metadata_filename = f"{url_type}_info.json"
                with open(folder / metadata_filename, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
            except:
                print("⚠️ Could not save metadata file")
            
            success_count = 0
            failed_count = 0
            
            # Process each track
            for i, track in enumerate(tracks, 1):
                try:
                    # Extract track information
                    title, artist_str, spotify_url = self.extract_track_details(track)
                    
                    current_track = f"{artist_str} - {title}"
                    print(f"[{i}/{len(tracks)}] Processing: {current_track}")
                    
                    filename = self.clean_filename(f"{artist_str} - {title}")
                    output_path = folder / f"{filename}.%(ext)s"
                    
                    # Check if file already exists
                    existing_files = list(folder.glob(f"{filename}.*"))
                    if existing_files:
                        success_count += 1
                        print("⏭️ Already exists, skipping...")
                        continue
                    
                    # Try download methods
                    success = False
                    track_info = (title, artist_str, spotify_url)
                    
                    # Primary: spotdl download
                    if spotify_url:
                        success = self.download_with_spotdl_primary(spotify_url, str(folder), track_info)
                    
                    # Fallback: yt-dlp search and download
                    if not success:
                        youtube_url = self.search_youtube_track(artist_str, title)
                        if youtube_url:
                            success = self.download_with_ytdlp_fallback(youtube_url, str(output_path), track_info)
                    
                    if success:
                        success_count += 1
                        print("✅ Downloaded successfully")
                    else:
                        failed_count += 1
                        print("❌ Download failed")
                
                except Exception as e:
                    print(f"⚠️ Error processing track {i}: {e}")
                    failed_count += 1
                    continue
            
            print(f"\n🎵 Download Complete!")
            print(f"📊 Summary: {success_count} successful, {failed_count} failed")
            print(f"📁 Files saved to: {folder}")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Critical error in {url_type} download: {e}")
            return False
    
    # Keep the old method name for backwards compatibility
    def download_playlist(self, playlist_url: str) -> bool:
        """Download playlist (wrapper for download_collection)"""
        return self.download_collection(playlist_url)


def interactive_playlist_download():
    """Interactive interface for downloading playlists and albums"""
    
    print("🎵 SPOTIFY PLAYLIST & ALBUM DOWNLOADER")
    print("=" * 50)
    print("Download your favorite Spotify playlists and albums with high-quality audio!")
    print()
    print("📝 Supported URLs:")
    print("   • Spotify Playlists: https://open.spotify.com/playlist/...")
    print("   • Spotify Albums: https://open.spotify.com/album/...")
    print()
    
    while True:
        print("🎯 Enter Spotify Playlist or Album URL (or 'done' to finish):")
        user_input = input("URL: ").strip()
        
        if user_input.lower() in ['done', 'exit', 'quit', '']:
            break
        
        if not downloader.is_valid_spotify_url(user_input):
            print("❌ Invalid Spotify URL! Please enter a valid playlist or album URL.")
            continue
        
        url_type = downloader.get_url_type(user_input)
        print(f"🎵 Starting {url_type} download...")
        
        try:
            success = downloader.download_collection(user_input)
            
            if success:
                print(f"\n✅ {url_type.title()} download completed successfully!")
            else:
                print(f"\n❌ {url_type.title()} download failed!")
                
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
        
        print("\n" + "="*50)
    
    print("🎵 Download session complete!")


def browse_downloaded_playlists():
    """Browse and display downloaded files"""
    downloads_dir = Path("Downloads")
    
    if not downloads_dir.exists():
        print("❌ No downloads folder found")
        print("📝 Run the download function first to create some downloads!")
        return
    
    collections = [p for p in downloads_dir.iterdir() if p.is_dir()]
    
    if not collections:
        print("📭 No playlists or albums downloaded yet")
        print("📝 Run the download function to start downloading playlists and albums!")
        return
    
    print("📂 YOUR DOWNLOADED PLAYLISTS & ALBUMS")
    print("=" * 50)
    
    total_songs = 0
    total_size = 0
    
    for i, collection_folder in enumerate(collections, 1):
        try:
            # Determine collection type from folder name or metadata
            collection_type = "Collection"
            if "playlist" in collection_folder.name.lower():
                collection_type = "🎵 Playlist"
            elif "album" in collection_folder.name.lower():
                collection_type = "💿 Album"
            else:
                # Check for metadata files to determine type
                if (collection_folder / "playlist_info.json").exists():
                    collection_type = "🎵 Playlist"
                elif (collection_folder / "album_info.json").exists():
                    collection_type = "💿 Album"
                else:
                    collection_type = "📁 Collection"
            
            # Count songs (exclude metadata file)
            songs = [f for f in collection_folder.iterdir() 
                    if f.suffix.lower() in ['.mp3', '.flac', '.m4a'] and f.is_file()]
            
            # Count additional files (lyrics, covers)
            lrc_files = [f for f in collection_folder.iterdir() if f.suffix.lower() == '.lrc']
            cover_files = [f for f in collection_folder.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
            
            # Calculate folder size
            folder_size = 0
            try:
                folder_size = sum(f.stat().st_size for f in collection_folder.rglob('*') if f.is_file())
            except:
                pass
            folder_size_mb = folder_size / (1024 * 1024) if folder_size > 0 else 0
            
            print(f"{collection_type} {i}. {collection_folder.name}")
            print(f"   📊 Songs: {len(songs)}")
            print(f"   📜 Lyrics: {len(lrc_files)} files")
            print(f"   🖼️ Album art: {len(cover_files)} covers")
            print(f"   💾 Size: {folder_size_mb:.1f} MB")
            
            # Show sample tracks
            if songs:
                print("   🎶 Sample tracks:")
                for song in songs[:3]:
                    song_name = song.name
                    if len(song_name) > 60:
                        song_name = song_name[:57] + "..."
                    print(f"      • {song_name}")
                if len(songs) > 3:
                    print(f"      ... and {len(songs) - 3} more")
            else:
                print("   ⚠️ No audio files found")
            
            total_songs += len(songs)
            total_size += folder_size_mb
            print()
            
        except Exception as e:
            print(f"⚠️ Error processing {collection_folder.name}: {e}")
            continue
    
    print("📊 DOWNLOAD SUMMARY:")
    print(f"   📁 Total collections: {len(collections)}")
    print(f"   🎶 Total songs: {total_songs}")
    print(f"   💾 Total size: {total_size:.1f} MB")
    print(f"   📍 Location: {downloads_dir.absolute()}")
    print("=" * 50)


def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing required packages...")
        subprocess.run(['pip', 'install', 'spotdl', 'yt-dlp'], check=True, capture_output=True)
        print("✅ Package installation complete!")
        
        print("🔧 Installing FFmpeg...")
        subprocess.run(['spotdl', '--download-ffmpeg'], check=True, capture_output=True)
        print("✅ FFmpeg installation complete!")
        
        print("✅ All dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        print("💡 Please install manually: pip install spotdl yt-dlp")
        return False


def main():
    """Main function to run the downloader"""
    print("🎵 Spotify Playlist & Album Downloader by Makuguren")
    print("=" * 50)
    
    # Check if dependencies are available
    try:
        subprocess.run(['spotdl', '--version'], check=True, capture_output=True)
        subprocess.run(['yt-dlp', '--version'], check=True, capture_output=True)
        print("✅ Dependencies are available!")
    except:
        print("📦 Dependencies not found. Installing...")
        if not install_dependencies():
            print("❌ Could not install dependencies. Please install manually.")
            return
    
    # Initialize downloader
    global downloader
    downloader = SpotifyPlaylistDownloader()
    
    # Menu loop
    while True:
        print("\n🎵 MAIN MENU")
        print("=" * 30)
        print("1. Download Playlist/Album")
        print("2. Browse Downloads")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            interactive_playlist_download()
        elif choice == '2':
            browse_downloaded_playlists()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main() 