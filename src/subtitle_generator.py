#!/usr/bin/env python3
"""
subtitle_generator.py
生成短剧经典风格字幕：
1. 底部主字幕：思源黑体 Extra Black / Heavy，纯白字身 + 7px 纯黑外描边 + 柔和微投影，居中饱满。
2. 右侧合规声明：右边缘纵排单列「故事纯属虚构  内容由AI生成」，英文缩写“AI”采用纵中横水平排版。
支持导出 ASS 影视字幕文件与 PIL 抽帧画面渲染。
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DEFAULT_FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"

def generate_douyin_ass(subtitles_list, output_ass_path, disclaimer_text="故事纯属虚构  内容由AI生成"):
    """
    生成短剧标准 ASS 字幕文件
    :param subtitles_list: [{"start": 0.8, "end": 4.0, "text": "..."}]
    :param output_ass_path: 输出路径
    :param disclaimer_text: 右侧竖排声明
    """
    ass_header = """[Script Info]
Title: Flow Manju Pipeline Short-Drama Style
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BottomSub,Noto Sans CJK SC,60,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,7,3,2,60,60,110,1
Style: RightDisclaimer,Noto Sans CJK SC,30,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,9,60,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # 转换右侧声明为 ASS 竖排格式
    # 格式示例：故\N事\N纯\N属\N虚\N构\N \N内\N容\N由\NAI\N生\N成
    disc_lines = []
    tokens = disclaimer_text.split()
    for idx, part in enumerate(tokens):
        if idx > 0:
            disc_lines.append(" ")
        i = 0
        while i < len(part):
            if part[i:i+2].upper() == "AI":
                disc_lines.append("AI")
                i += 2
            else:
                disc_lines.append(part[i])
                i += 1
    disc_ass_str = "\\N".join(disc_lines)

    lines = [ass_header]
    # 右侧常驻声明（全程常驻）
    lines.append(f"Dialogue: 1,0:00:00.00,0:01:00.00,RightDisclaimer,,0,0,0,,{{\\pos(1856,238)}}{disc_ass_str}\n")

    # 底部主台词字幕
    for item in subtitles_list:
        s_sec = item["start"]
        e_sec = item["end"]
        s_time = f"{int(s_sec//3600):01d}:{int((s_sec%3600)//60):02d}:{s_sec%60:05.2f}"
        e_time = f"{int(e_sec//3600):01d}:{int((e_sec%3600)//60):02d}:{e_sec%60:05.2f}"
        lines.append(f"Dialogue: 0,{s_time},{e_time},BottomSub,,0,0,0,,{item['text']}\n")

    Path(output_ass_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return output_ass_path


def render_frame_with_subtitles(raw_image_path, output_image_path, sub_text, font_path=DEFAULT_FONT_PATH):
    """
    使用 Pillow 渲染具备 100% 像素级精度的短剧标准抽帧图片
    """
    img = Image.open(raw_image_path).convert("RGBA")
    w, h = img.size

    font_sub = ImageFont.truetype(font_path, 60)
    font_disc = ImageFont.truetype(font_path, 30)

    txt_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 1. 右侧声明
    disc_items = ["故", "事", "纯", "属", "虚", "构", "", "内", "容", "由", "AI", "生", "成"]
    disc_x = w - 64
    char_step = 40
    start_y = int(h * 0.22)

    for idx, ch in enumerate(disc_items):
        if not ch:
            continue
        y = start_y + idx * char_step
        bbox = draw.textbbox((0, 0), ch, font=font_disc)
        ch_w = bbox[2] - bbox[0]
        x = disc_x - ch_w // 2

        # 阴影 + 纯白黑描边
        draw.text((x + 2, y + 2), ch, font=font_disc, fill=(0, 0, 0, 200), stroke_width=4, stroke_fill=(0, 0, 0, 255))
        draw.text((x, y), ch, font=font_disc, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))

    # 2. 底部主字幕
    sub_bbox = draw.textbbox((0, 0), sub_text, font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_x = (w - sub_w) // 2
    sub_y = int(h * 0.86)

    draw.text((sub_x + 3, sub_y + 3), sub_text, font=font_sub, fill=(0, 0, 0, 180), stroke_width=7, stroke_fill=(0, 0, 0, 255))
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))

    final_img = Image.alpha_composite(img, txt_layer).convert("RGB")
    Path(output_image_path).parent.mkdir(parents=True, exist_ok=True)
    final_img.save(output_image_path, quality=95)
    return output_image_path

if __name__ == "__main__":
    print("Subtitle Generator module ready.")
