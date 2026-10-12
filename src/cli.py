#!/usr/bin/env python3
"""
cli.py
FLOW 漫剧流水线统帅 CLI 入口
支持：
1. pipeline run --config <config.json>
2. pipeline assemble --video <raw.mp4> --subtitles <subtitles.ass> --output <final.mp4>
3. pipeline render-frame --image <raw.png> --text "..." --output <out.png>
"""

import os
import sys
import json
import argparse
from pathlib import Path

from subtitle_generator import generate_douyin_ass, render_frame_with_subtitles
from video_assembler import assemble_manju_video, generate_preview_gif

def main():
    parser = argparse.ArgumentParser(description="Google Flow 漫剧流水线 CLI (Veo 3.1 - Lite 原生音轨版)")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # assemble 子命令
    p_assemble = subparsers.add_parser("assemble", help="后期装配 12 秒成片与字幕")
    p_assemble.add_argument("--source", required=True, help="Flow 导出的原始合并长视频路径")
    p_assemble.add_argument("--ass", required=True, help="ASS 字幕文件路径")
    p_assemble.add_argument("--output", required=True, help="输出 MP4 成片路径")
    p_assemble.add_argument("--start", type=float, default=2.0, help="截取开始秒数")
    p_assemble.add_argument("--duration", type=float, default=12.0, help="输出时长秒数")

    # render-frame 子命令
    p_frame = subparsers.add_parser("render-frame", help="渲染短剧标准抽帧图片（含黑边白字与右侧声明）")
    p_frame.add_argument("--image", required=True, help="原始未标注抽帧 PNG 路径")
    p_frame.add_argument("--text", required=True, help="底部主台词文本")
    p_frame.add_argument("--output", required=True, help="输出渲染图片路径")

    # run 子命令
    p_run = subparsers.add_parser("run", help="根据 config.json 一键执行组装")
    p_run.add_argument("--config", required=True, help="项目配置文件路径")
    p_run.add_argument("--source-video", required=False, help="Flow 合并视频（若已下载）")
    p_run.add_argument("--output-dir", default="./output", help="输出目录")

    args = parser.parse_args()

    if args.command == "assemble":
        out = assemble_manju_video(args.source, args.ass, args.output, args.start, args.duration)
        gif_out = Path(args.output).with_suffix(".gif")
        generate_preview_gif(out, gif_out, args.duration)
        print(f"✅ 装配完成！成片: {out}, 动图: {gif_out}")

    elif args.command == "render-frame":
        out = render_frame_with_subtitles(args.image, args.output, args.text)
        print(f"✅ 抽帧渲染完成: {out}")

    elif args.command == "run":
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 生成 ASS 字幕
        ass_path = out_dir / f"{cfg.get('project_name', 'project')}.ass"
        generate_douyin_ass(cfg["subtitles"], ass_path, cfg.get("disclaimer", "故事纯属虚构  内容由AI生成"))
        print(f"✓ 字幕文件已就绪: {ass_path}")

        # 2. 如果提供了 source-video，则直接装配成片
        if args.source_video:
            final_mp4 = out_dir / f"{cfg.get('project_name', 'project')}_final.mp4"
            assemble_manju_video(
                args.source_video,
                ass_path,
                final_mp4,
                start_time=2.0,
                duration=cfg.get("target_duration_seconds", 12.0)
            )
            gif_path = out_dir / f"{cfg.get('project_name', 'project')}_preview.gif"
            generate_preview_gif(final_mp4, gif_path, cfg.get("target_duration_seconds", 12.0))
            print(f"🎉 项目出片成功！输出位于: {out_dir}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
