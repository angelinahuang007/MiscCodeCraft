import os
import pandas as pd
from yt_dlp import YoutubeDL

# ---- SETTINGS ----
OUTPUT_DIR = "downloads"
CSV_FILE = "songs.csv"  # Your CSV with columns: Song, Artist, Link

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- READ CSV ----
df = pd.read_csv(CSV_FILE)

# ---- BASE YT-DLP OPTIONS ----
base_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': False,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# ---- DOWNLOAD LOOP ----
with YoutubeDL(base_opts) as ydl:
    for _, row in df.iterrows():
        song = str(row['Song']).strip()
        artist = str(row['Artist']).strip()
        url = str(row['Link']).strip()

        # Clean filename (remove illegal chars for Windows/macOS)
        safe_name = f"{song} - {artist}".replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace("*", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
        target_path = os.path.join(OUTPUT_DIR, f"{safe_name}.mp3")

        # Skip already downloaded files
        if os.path.exists(target_path):
            print(f"✅ Already downloaded: {safe_name}.mp3")
            continue

        # Customize output filename for this song
        ydl.params['outtmpl'] = os.path.join(OUTPUT_DIR, f"{safe_name}.%(ext)s")

        print(f"🎵 Downloading: {safe_name}")
        try:
            ydl.download([url + "&no-playlist=1"])
            print(f"✅ Finished: {safe_name}.mp3\n")
        except Exception as e:
            print(f"❌ Failed to download {url}: {e}\n")
