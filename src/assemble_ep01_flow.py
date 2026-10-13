#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

RAW_DIR = Path("/root/.agy-avisii/.gemini/production/ep01_flow_raw")
OUTPUT_DIR = Path("/root/.agy-avisii/.gemini/production")
DOCS_DIR = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/docs")
ASS_PATH = OUTPUT_DIR / "ep01_flow.ass"
CONCAT_TXT = OUTPUT_DIR / "concat_list.txt"
MERGED_RAW = OUTPUT_DIR / "ep01_merged_raw.mp4"
FINAL_MP4 = DOCS_DIR / "zoo_pet_ep01_final.mp4"
PREVIEW_GIF = DOCS_DIR / "zoo_pet_ep01_preview.gif"

# 1. 准备镜头剪辑切片 (基于 Flow 原生视频)
# Shot 1: 麻雀炸毛 0 - 2.8s
# Shot 2: 姜瑾冷笑反杀 2.0 - 7.5s (5.5s)
# Shot 3: 债务合同 0 - 8.0s
# Shot 4: 系统觉醒 0 - 8.0s
# Shot 5: 狂暴雄狮绝命钩 0 - 8.0s
clips = [
    {"src": RAW_DIR / "shot01_sparrow_shock.mp4", "ss": 0.0, "t": 2.8, "name": "clip01.mp4"},
    {"src": RAW_DIR / "shot02_heroine_smirk.mp4", "ss": 1.5, "t": 6.0, "name": "clip02.mp4"},
    {"src": RAW_DIR / "shot03_debt_contract.mp4", "ss": 0.0, "t": 8.0, "name": "clip03.mp4"},
    {"src": RAW_DIR / "shot04_system_awakening.mp4", "ss": 0.0, "t": 8.0, "name": "clip04.mp4"},
    {"src": RAW_DIR / "shot05_lion_climax_hook.mp4", "ss": 0.0, "t": 8.0, "name": "clip05.mp4"}
]

print("1. 剪辑各切片...")
clip_files = []
for c in clips:
    out_clip = OUTPUT_DIR / c["name"]
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(c["ss"]),
        "-t", str(c["t"]),
        "-i", str(c["src"]),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        str(out_clip)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    clip_files.append(out_clip)
    print(f"   ✓ {c['name']} (时长: {c['t']}s)")

# 2. 拼接为原始合集
with open(CONCAT_TXT, "w", encoding="utf-8") as f:
    for cf in clip_files:
        f.write(f"file '{cf.resolve()}'\n")

print("2. 无损拼接所有 Flow 镜头...")
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(CONCAT_TXT),
    "-c", "copy",
    str(MERGED_RAW)
]
subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# 计算总时长
probe = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(MERGED_RAW)],
    stdout=subprocess.PIPE, text=True
)
total_dur = float(probe.stdout.strip())
print(f"   ✓ 拼接完成，总时长: {total_dur:.2f}s")

# 3. 生成经典短剧 ASS 字幕 (加粗黑边白字 + 右侧纵排声明)
# 时码规划:
# 00:00 - 02.80: 麻雀炸毛 “卧槽！两脚兽成精了！她真能听懂我骂她？！”
# 02.80 - 08.80: 姜瑾冷笑 “小家伙，你刚才在叫唤什么？再废话拿你烤了抵债。”
# 08.80 - 16.80: 催债人 “连本带息整整一千万！一个月不还，连人带动物园全被法拍！”
# 16.80 - 24.80: 系统觉醒 “【奇迹动物园救赎系统】绑定成功！已解锁万兽通识语感！”
# 24.80 - 32.80: 狂暴雄狮留钩 “【狂暴金鬃雄狮】吼——！！两脚兽全都该死！滚出我的领地——！！”

ass_content = f"""[Script Info]
Title: Zoo Pet Ep01 Short-Drama Style
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BottomSub,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,9,3,2,60,60,83,1
Style: BottomSub,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,9,3,2,60,60,83,1
Style: RightDisclaimer,Noto Sans CJK SC,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,9,60,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:01:00.00,RightDisclaimer,,0,0,0,,{{\\pos(1856,238)}}故\\N事\\N纯\\N属\\N虚\\N构\\N \\N内\\N容\\N由\\NAI\\N生\\N成
Dialogue: 0,0:00:00.00,0:00:02.80,BottomSub,,0,0,0,,卧槽！两脚兽成精了！她真能听懂我骂她？！
Dialogue: 0,0:00:02.80,0:00:08.80,BottomSub,,0,0,0,,小家伙，你刚才在叫唤什么？再废话拿你烤了抵债。
Dialogue: 0,0:00:08.80,0:00:16.80,BottomSub,,0,0,0,,连本带息整整一千万！一个月不还，连人带动物园全被法拍！
Dialogue: 0,0:00:16.80,0:00:24.80,BottomSub,,0,0,0,,【奇迹动物园救赎系统】绑定成功！已解锁万兽通识语感！
Dialogue: 0,0:00:24.80,0:00:32.80,BottomSub,,0,0,0,,【狂暴金鬃雄狮】吼——！！两脚兽全都该死！滚出我的领地——！！
"""

with open(ASS_PATH, "w", encoding="utf-8") as f:
    f.write(ass_content)
print("3. ASS 字幕生成完毕。")

# 4. 压制最终成片 (1920x1080 16:9, CRF=18, 100% Flow 原生音轨微淡入淡出)
print(f"4. 正在压制电影级母带成片: {FINAL_MP4} ...")
cmd_burn = [
    "ffmpeg", "-y",
    "-i", str(MERGED_RAW),
    "-vf", f"scale=1920:1080:flags=lanczos,ass={ASS_PATH.resolve()}",
    "-af", f"afade=t=in:ss=0:d=0.08,afade=t=out:st={total_dur - 0.2:.2f}:d=0.2",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    "-c:a", "aac", "-b:a", "320k",
    str(FINAL_MP4)
]
subprocess.run(cmd_burn, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(f"   🎉 成片压制成功！大小: {FINAL_MP4.stat().st_size / (1024*1024):.2f} MB")

# 5. 生成 10fps 高清动图预览 GIF
print("5. 正在生成 10fps 双通道优化动图预览...")
cmd_gif = [
    "ffmpeg", "-y",
    "-ss", "0", "-t", "10",
    "-i", str(FINAL_MP4),
    "-vf", "fps=10,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    str(PREVIEW_GIF)
]
subprocess.run(cmd_gif, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(f"   ✓ 动图预览已生成: {PREVIEW_GIF.name} ({PREVIEW_GIF.stat().st_size / (1024*1024):.2f} MB)")

# 6. 抽帧质检 (01.5s, 05.0s, 12.0s, 20.0s, 28.0s)
qc_times = [1.5, 5.0, 12.0, 20.0, 28.0]
for idx, qt in enumerate(qc_times, 1):
    qc_frame = DOCS_DIR / f"shot{idx}_qc_frame.png"
    cmd_qc = [
        "ffmpeg", "-y",
        "-ss", str(qt),
        "-i", str(FINAL_MP4),
        "-vframes", "1",
        str(qc_frame)
    ]
    subprocess.run(cmd_qc, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"   ✓ 抽帧质检 {qc_frame.name} (时码 {qt}s)")

print("\n全流程装配完成！")
