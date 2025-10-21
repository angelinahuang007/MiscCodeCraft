import os
import random
from pydub import AudioSegment

# --- 路径设置 ---
CUTS_DIR = "cuts"
COUNTDOWN_FILE = "Countdown.mp3"
OUTPUT_FILE = "final_mix.mp3"
TIMESTAMP_FILE = "timestamps.txt"

# --- 随机种子（可改成任意整数，保持结果可复现） ---
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# --- 读取 Countdown ---
countdown = AudioSegment.from_file(COUNTDOWN_FILE)
countdown = countdown.fade_in(1000)  # countdown 渐入 1 秒

# --- 获取所有片段文件 ---
files = [f for f in os.listdir(CUTS_DIR) if f.lower().endswith(".mp3")]

# -------------------------------
# 🔧 自定义固定顺序（可修改）
# -------------------------------
FIXED_START = []                   # 例: ["intro.mp3"]
FIXED_END = ["Gnarly - Katseye.mp3"]  # 例: ["ending.mp3"]
# -------------------------------

# 去掉已固定的文件并随机打乱剩余
remaining_files = [f for f in files if f not in FIXED_START + FIXED_END]
random.shuffle(remaining_files)
play_order = FIXED_START + remaining_files + FIXED_END

print("🎵 播放顺序:")
for i, f in enumerate(play_order, 1):
    print(f"{i:02d}. {f}")

# --- 合成 ---
final_audio = AudioSegment.silent(duration=0)
timestamps = []
current_time_ms = 0

# 先加一个 countdown（前导）
final_audio += countdown
current_time_ms += len(countdown)

for i, f in enumerate(play_order):
    clip_path = os.path.join(CUTS_DIR, f)
    clip = AudioSegment.from_file(clip_path)

    # 记录 clip 的实际开始时间（不含 countdown）
    timestamps.append((current_time_ms / 1000, f))

    # 添加 clip
    final_audio += clip
    current_time_ms += len(clip)

    # 如果不是最后一个 clip，添加 countdown（clip 和 countdown 重叠 1s）
    if i < len(play_order) - 1:
        overlap_ms = 1000
        final_audio = final_audio.append(countdown, crossfade=overlap_ms)
        current_time_ms += len(countdown) - overlap_ms

# --- 导出 ---
final_audio.export(OUTPUT_FILE, format="mp3")
print(f"✅ Exported audio to {OUTPUT_FILE}")

# --- 导出时间戳 ---
def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

with open(TIMESTAMP_FILE, "w", encoding="utf-8") as f:
    for t, name in timestamps:
        f.write(f"{format_time(t)} - {name}\n")

print(f"🕒 Exported timestamps to {TIMESTAMP_FILE}")
