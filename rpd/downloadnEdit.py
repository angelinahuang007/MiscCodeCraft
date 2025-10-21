import os
import pandas as pd
from yt_dlp import YoutubeDL
import subprocess
import tempfile

# ---- SETTINGS ----
OUTPUT_DIR = "cuts"
CSV_FILE = "songs.csv"  # Must include: Song, Artist, Link, Start, End

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- READ CSV ----
df = pd.read_csv(CSV_FILE)

# ---- BASE YT-DLP OPTIONS ----
base_opts = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": False,
}

def clean_filename(name: str):
    """Clean illegal characters for file naming (Windows/macOS safe)"""
    return name.translate(str.maketrans(r'\/:*?"<>|', "_________")).strip()

def time_to_seconds(t: str):
    """Convert 0:00:00 / 0:00 to seconds (float)"""
    parts = [float(p) for p in t.split(":")]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    else:
        return parts[0]

# ---- MAIN LOOP ----
for _, row in df.iterrows():
    song = str(row.get("Song", "")).strip()
    artist = str(row.get("Artist", "")).strip()
    url = str(row.get("Link", "")).strip()
    start = str(row.get("Start", "")).strip()
    end = str(row.get("End", "")).strip()

    safe_song = clean_filename(song)
    safe_artist = clean_filename(artist)
    filename = f"{safe_song} - {safe_artist}.mp3"
    clip_path = os.path.join(OUTPUT_DIR, filename)

    if not url or not start or not end:
        print(f"⚠️ Missing fields for: {song} - {artist}, skipped.\n")
        continue

    if os.path.exists(clip_path):
        print(f"✅ Already exists: {filename}")
        continue

    print(f"🎵 Processing: {song} - {artist} (fade-in/out, +1s end)")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_audio = os.path.join(tmpdir, "temp_audio.%(ext)s")
            opts = base_opts.copy()
            opts["outtmpl"] = temp_audio

            # ---- Download ----
            with YoutubeDL(opts) as ydl:
                ydl.download([url + "&no-playlist=1"])

            # ---- Find file ----
            downloaded_files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir)]
            if not downloaded_files:
                print(f"❌ No file downloaded for {song} - {artist}")
                continue
            input_file = downloaded_files[0]

            # ---- Compute time range ----
            start_sec = time_to_seconds(start)
            end_sec = time_to_seconds(end)
            total_duration = end_sec - start_sec + 1  # +1s at end
            fade_in_dur = 2
            fade_out_dur = 2
            fade_out_start = total_duration - fade_out_dur

            # ---- Apply fade in/out ----
            fade_filter = f"afade=t=in:st=0:d={fade_in_dur},afade=t=out:st={fade_out_start}:d={fade_out_dur}"

            subprocess.run([
                "ffmpeg", "-y",
                "-ss", start, "-to", str(end_sec + 1),
                "-i", input_file,
                "-vn",
                "-af", fade_filter,
                "-acodec", "libmp3lame", "-ab", "192k",
                clip_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        print(f"✅ Saved clip: {filename}\n")

    except Exception as e:
        print(f"❌ Failed to process {song} - {artist}: {e}\n")
