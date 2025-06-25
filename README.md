# 🎵 Spotify Playlist & Album Downloader by Makuguren

![Spotify Logo](https://www.scdn.co/i/_global/open-graph-default.png)

A comprehensive Spotify downloader that supports **playlists and albums** with up to **320kbps audio quality**, complete metadata, album art, and lyrics using advanced download methods.

## ✨ Features

- 🎵 **Playlist Support** - Download complete Spotify playlists
- 💿 **Album Support** - Download full Spotify albums
- 🔊 **High-Quality Audio** - Up to 320kbps MP3 downloads
- 🖼️ **Album Art** - Embedded and separate cover images
- 📜 **Lyrics** - Download .lrc lyric files when available
- 📝 **Complete Metadata** - Artist, title, album, track number embedding
- 🔄 **Smart Fallback System** - spotdl → yt-dlp for maximum success
- ⏭️ **Skip Existing** - Automatically skip already downloaded tracks
- 📊 **Progress Tracking** - Real-time download statistics
- 🗂️ **Organized Structure** - Clean folder organization

## 📋 Requirements

- **Python 3.8+** (tested with Python 3.9-3.11)
- **Internet connection** for downloads
- **FFmpeg** (automatically installed by spotdl)

## 🚀 Quick Start

### Option 1: Download Official Release (Recommended)
Get the pre-built executable from the **[Releases](../../releases)** tab:

1. **Go to Releases** - Click the "Releases" tab on the GitHub repository
2. **Download Latest** - Download `Spotify Playlist Downloader by Makuguren.exe`
3. **Run Directly** - No Python installation required, just double-click to run
4. **Windows Ready** - Works on any Windows 10+ system

### Option 2: Auto-Install Dependencies
The application will automatically install missing dependencies on first run:

```bash
python spotify_playlist_downloader.py
```

### Option 3: Manual Installation
Install dependencies manually:

```bash
pip install spotdl yt-dlp
spotdl --download-ffmpeg
python spotify_playlist_downloader.py
```

### Option 4: Google Colab (No Installation Required)
Run directly in your browser using Google Colab:

1. **Open Google Colab**: Go to [colab.research.google.com](https://colab.research.google.com)
2. **Upload Notebook**: 
   - Click "Upload" tab
   - Select `Spotify_Playlist_Downloader.ipynb` from this repository
3. **Run All Cells**: Click `Runtime` → `Run all`
4. **Download Results**: Files will be available in Colab's file browser

**Available Notebooks:**
- `Spotify_Playlist_Downloader.ipynb` - Full-featured version with all options
- `Spotify_Downloader_SafeMode.ipynb` - Simplified version for basic downloading

## 🎯 Usage

### Interactive Mode (Recommended)
Run the application with a user-friendly menu interface:

```bash
python spotify_playlist_downloader.py
```

**Features:**
- 🎵 Menu-driven interface
- 📝 Step-by-step guidance
- 📊 Real-time progress tracking
- 📂 Browse downloaded content

### Supported URLs

```bash
# Spotify Playlists
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M

# Spotify Albums  
https://open.spotify.com/album/4aawyAB9vmqN3uQ7FjRGTy
```

### Menu Options
1. **Download Playlist/Album** - Enter Spotify URLs to download
2. **Browse Downloads** - View your downloaded music library
3. **Exit** - Close the application

## 📘 Google Colab Usage

### 🌐 **Running in Google Colab (Browser-Based)**

For users who don't want to install Python locally, you can run the downloader directly in your browser:

#### **Step-by-Step Guide:**

1. **📱 Open Google Colab**
   - Go to [colab.research.google.com](https://colab.research.google.com)
   - Sign in with your Google account

2. **📁 Upload the Notebook**
   ```
   • Click "Upload" tab in Colab
   • Drag and drop the .ipynb file
   • Or click "Choose Files" and select the notebook
   ```

3. **🚀 Run the Downloader**
   - Click `Runtime` → `Run all` (or use Ctrl+F9)
   - Follow the on-screen prompts
   - Enter your Spotify URLs when requested

4. **📥 Download Your Music**
   - Files will appear in Colab's file browser (left sidebar)
   - Right-click files/folders to download
   - Or use the built-in Google Drive backup feature

#### **📝 Available Notebook Versions:**

| Notebook | Description | Best For |
|----------|-------------|----------|
| `Spotify_Playlist_Downloader.ipynb` | **Full-featured version** with Google Drive backup, ZIP download, and all advanced options | Power users who want all features |
| `Spotify_Downloader_SafeMode.ipynb` | **Simplified version** focused on basic downloading without extra features | Beginners who want simple downloading |

#### **🔧 Colab Advantages:**
- ✅ **No Installation** - Works in any web browser
- ✅ **Free GPU/CPU** - Google provides computing resources
- ✅ **Google Drive Integration** - Easy backup and sharing
- ✅ **Pre-installed Libraries** - Most dependencies already available
- ✅ **Mobile Friendly** - Works on tablets and phones

## ⚙️ How It Works

1. **URL Validation** - Checks if the provided URL is a valid Spotify playlist or album
2. **Metadata Extraction** - Uses spotdl to fetch complete metadata from Spotify API
3. **Primary Download** - Downloads using spotdl with high-quality settings (320kbps)
4. **Fallback System** - If primary fails, uses yt-dlp with YouTube search
5. **Quality Processing** - Ensures maximum audio quality and proper formatting
6. **Metadata Embedding** - Embeds complete metadata (artist, title, album, track number)
7. **Album Art & Lyrics** - Downloads and embeds album artwork and lyric files
8. **Organization** - Creates clean folder structure with proper naming

## 📁 Output Structure

```
Downloads/
├── Spotify_Playlist_12345678/          # Playlist downloads
│   ├── playlist_info.json              # Playlist metadata
│   ├── Artist - Song Title 1.mp3       # Audio files (320kbps)
│   ├── Artist - Song Title 1.lrc       # Lyrics files
│   ├── Artist - Song Title 2.mp3
│   ├── cover.jpg                       # Album artwork
│   └── ...
├── Spotify_Album_87654321/             # Album downloads
│   ├── album_info.json                 # Album metadata
│   ├── Artist - Track 01.mp3
│   ├── Artist - Track 01.lrc
│   ├── Artist - Track 02.mp3
│   ├── cover.jpg
│   └── ...
```

### File Types Generated
- **📱 Audio**: `.mp3` files (up to 320kbps)
- **📜 Lyrics**: `.lrc` files (when available)
- **🖼️ Artwork**: `.jpg` cover images
- **📄 Metadata**: `.json` information files

## 🔊 Audio Quality & Features

### High-Quality Downloads
- **Primary**: spotdl downloads at up to 320kbps MP3
- **Fallback**: yt-dlp with YouTube search and download
- **Format**: MP3 for maximum compatibility
- **Metadata**: Complete ID3 tags embedded

### Advanced Features
- **🎨 Album Art**: Embedded in audio files + separate cover images
- **📜 Lyrics**: Downloads .lrc lyric files when available
- **📊 Progress Tracking**: Real-time download status and statistics
- **⏭️ Smart Skip**: Automatically skips existing files
- **🔄 Error Recovery**: Continues downloading despite individual failures
- **🗂️ Auto-Organization**: Clean folder structure with proper naming

### Fallback System
1. **Primary Method**: spotdl (direct Spotify metadata + YouTube audio)
2. **Fallback Method**: yt-dlp (YouTube search + high-quality extraction)
3. **Error Handling**: Graceful handling of failed downloads
4. **Resume Support**: Skip already downloaded tracks

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **FFmpeg not found** | Run `spotdl --download-ffmpeg` or restart the application (auto-installs) |
| **Permission errors** | Ensure write permissions in Downloads folder |
| **Network timeouts** | Check internet connection, restart download (skips existing files) |
| **Invalid URL** | Ensure URL is from open.spotify.com and publicly accessible |
| **Download failures** | Application continues with other tracks, check individual error messages |

### Supported Content
- ✅ **Public Playlists** - Any publicly accessible Spotify playlist
- ✅ **Public Albums** - Any Spotify album available in your region
- ✅ **Collaborative Playlists** - If publicly accessible
- ❌ **Private Content** - Private playlists and region-locked content


## 📦 Dependencies

- **spotdl** - Spotify metadata extraction and primary downloading
- **yt-dlp** - Fallback YouTube downloading and search
- **FFmpeg** - Audio processing (auto-installed)
- **Python 3.8+** - Runtime environment

## ⚖️ Legal Notice

This tool is for **personal use only**. Users are responsible for:
- Respecting copyright laws and terms of service
- Only downloading content they have legal access to
- Not distributing copyrighted material
- Complying with local laws and regulations

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Credits

**Created by  Mark Glen Miguel (Makuguren)**
- Based on the excellent [spotDL](https://spotdl.readthedocs.io/) project
- Enhanced with advanced features and user interface
- Built for high-quality audio downloading with complete metadata 