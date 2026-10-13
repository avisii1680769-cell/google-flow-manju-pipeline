#!/usr/bin/env python3
"""
assemble_full_ep01.py
Assembles all 18 Google Flow native shots into the complete 2m17s (136.8s) Episode 1 master.
Burns in full ASS subtitles and TV compliance disclaimer.
Preserves 48kHz native stereo audio.
"""

import subprocess
from pathlib import Path

BASE_DIR = Path("/root/.agy-avisii/.gemini/production")
RAW_DIR = BASE_DIR / "ep01_flow_raw"
DOCS_DIR = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/docs")
ASS_PATH = BASE_DIR / "ep01_full_flow.ass"
OUTPUT_MP4 = DOCS_DIR / "zoo_pet_ep01_final.mp4"

SHOTS_CONFIG = [
    ("shot01_sparrow_shock.mp4", 0.0, 2.8),
    ("shot02_heroine_smirk.mp4", 0.0, 6.0),
    ("shot06_zoo_gate_ruins.mp4", 0.0, 8.0),
    ("shot03_debt_contract.mp4", 0.0, 8.0),
    ("shot07_debt_thugs_intimidation.mp4", 0.0, 8.0),
    ("shot08_heroine_unyielding_gaze.mp4", 0.0, 8.0),
    ("shot09_debt_cars_leaving.mp4", 0.0, 8.0),
    ("shot04_system_awakening.mp4", 0.0, 8.0),
    ("shot10_system_interface_hud.mp4", 0.0, 8.0),
    ("shot11_heroine_hearing_voices.mp4", 0.0, 8.0),
    ("shot12_peacock_complaint.mp4", 0.0, 8.0),
    ("shot13_raccoon_snack_heist.mp4", 0.0, 8.0),
    ("shot14_monkey_gossip.mp4", 0.0, 8.0),
    ("shot15_heroine_turning_serious.mp4", 0.0, 8.0),
    ("shot16_predator_tunnel_alarm.mp4", 0.0, 8.0),
    ("shot17_ground_shake_chains.mp4", 0.0, 8.0),
    ("shot18_heroine_approaching_cage.mp4", 0.0, 8.0),
    ("shot05_lion_climax_hook.mp4", 0.0, 8.0),
]

def check_all_shots_ready():
    missing = []
    for fname, _, _ in SHOTS_CONFIG:
        p = RAW_DIR / fname
        if not p.exists() or p.stat().st_size < 100000:
            missing.append(fname)
    return missing

def main():
    missing = check_all_shots_ready()
    if missing:
        print(f"⏳ 尚有 {len(missing)} 个镜头等待 Flow 云端生成中: {missing}")
        return False

    print("🎉 所有 18 个镜头均已在本地就绪！开始母带组装与压制...")
    
    # 步骤 1: 逐个切片并转为统一流规范 (1280x720, 24fps, 48000Hz stereo)
    concat_list_lines = []
    for idx, (fname, start_t, dur_t) in enumerate(SHOTS_CONFIG, 1):
        in_p = RAW_DIR / fname
        clip_p = BASE_DIR / f"full_clip_{idx:02d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-ss", str(start_t), "-t", str(dur_t),
            "-i", str(in_p),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
            "-r", "24", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "320k",
            str(clip_p)
        ]
        subprocess.run(cmd, check=True)
        concat_list_lines.append(f"file '{clip_p}'")

    concat_file = BASE_DIR / "full_concat_list.txt"
    concat_file.write_text("\n".join(concat_list_lines), encoding="utf-8")

    # 步骤 2: 无损拼接全部 18 个镜头
    merged_raw = BASE_DIR / "ep01_full_merged_raw.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(merged_raw)
    ], check=True)

    # 步骤 3: 压制 1080p 超清母带并烧录精校 ASS 粗黑边白字字幕与合规声明
    print(f"➤ 正在执行 1080p Lanczos 升采样与精细黑边字幕压制...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(merged_raw),
        "-vf", f"scale=1920:1080:flags=lanczos,ass={ASS_PATH}",
        "-af", "afade=t=in:ss=0:d=0.08,afade=t=out:st=136.5:d=0.3",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "320k",
        str(OUTPUT_MP4)
    ], check=True)

    print(f"🏆 第 1 集 18 镜头完整正片母带压制完成: {OUTPUT_MP4} ({OUTPUT_MP4.stat().st_size / 1024 / 1024:.2f} MB)")
    return True

if __name__ == "__main__":
    main()
