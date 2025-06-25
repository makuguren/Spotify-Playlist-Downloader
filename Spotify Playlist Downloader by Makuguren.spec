# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Add current directory to path
sys.path.append('.')

block_cipher = None

a = Analysis(
    ['spotify_playlist_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Include any data files if needed
    ],
    hiddenimports=[
        'spotdl',
        'yt_dlp',
        'youtube_dl',
        'mutagen',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'spotipy',
        'pytube',
        'eyed3',
        'ffmpeg',
        'ffmpeg_python',
        'json',
        'tempfile',
        'subprocess',
        'pathlib',
        'typing',
        're',
        'os',
        'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Spotify Playlist Downloader by Makuguren',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one
)
