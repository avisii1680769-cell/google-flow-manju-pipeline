#!/usr/bin/env python3
"""
video_assembler.py
负责高保真音视频合成：
1. 100% 保留 Google Flow 原生立体声音轨，微淡入淡出消除剪切噪点。
2. 压制短剧经典纯黑边白字与右侧声明 ASS 字幕。
3. 电影级 CRF=17 无损编码，生成超清 1080P MP4。
4. 输出高质量 12s 预览 GIF。
"""

import os
import sys
import subprocess
from pathlib import Path

def assemble_manju_video(
    source_video_path,
    ass_subtitle_path,
    output_video_path,
    start_time=2.0,
    duration=12.0,
    resolution="1920:1080",
    crf=17
):
    """
    高精度装配成片
    """
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-t", str(duration),
        "-i", str(source_video_path),
        "-vf", f"scale={resolution}:flags=lanczos,ass={Path(ass_subtitle_path).resolve()}",
        "-af", f"afade=t=in:ss=0:d=0.2,afade=t=out:st={duration - 0.3:.2f}:d=0.3",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        str(output_video_path)
    ]
    print(f"🎬 正在渲染合成: {output_video_path} (时长: {duration}s, 画质: {resolution})")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg 压制失败: {res.stderr.decode('utf-8')[:300]}")
    
    print(f"🎉 视频合成成功！文件大小: {Path(output_video_path).stat().st_size / (1024*1024):.2f} MB")
    return output_video_path


def generate_preview_gif(video_path, output_gif_path, duration=12.0, fps=10, width=640):
    """
    从成片中生成轻量化动态预览 GIF
    """
    cmd = [
        "ffmpeg", "-y",
        "-ss", "0",
        "-t", str(duration),
        "-i", str(video_path),
        "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        str(output_gif_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✓ 动图预览已生成: {output_gif_path}")
    return output_gif_path

if __name__ == "__main__":
    print("Video Assembler module ready.")
