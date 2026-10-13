#!/usr/bin/env python3
"""
flow_episode1_producer.py
Automated Google Flow (Veo 3.1 - Lite) generator for Episode 1 of 《继承动物园后，我通兽语成为国家团宠》.
Strict Rule: If credits run out, immediately halt and alert user to replace account.
"""

import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_PATH = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/config/flow_cookies.json")
OUTPUT_DIR = Path("/root/.agy-avisii/.gemini/production/ep01_flow_raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR = Path("/root/.agy-gabor/.gemini/antigravity-cli/brain/aba683fa-a376-46a0-93b9-3717daeb52a2")

with open(COOKIES_PATH, "r", encoding="utf-8") as f:
    raw_cookies = json.load(f)

playwright_cookies = []
for c in raw_cookies:
    s = c.get("sameSite", "")
    s_val = "None" if str(s).lower() in ["no_restriction", "none"] else ("Strict" if str(s).lower() == "strict" else "Lax")
    playwright_cookies.append({
        "name": c.get("name"),
        "value": c.get("value"),
        "domain": c.get("domain"),
        "path": c.get("path", "/"),
        "secure": c.get("secure", True),
        "httpOnly": c.get("httpOnly", False),
        "sameSite": s_val
    })

SHOTS = [
    {
        "id": 2,
        "name": "shot02_jiang_jin_smirk",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Medium close-up of a sharp spirited 24-year-old Asian female zoo director (Jiang Jin), neat high black ponytail, wearing an olive cargo utility jacket. "
            "She turns her head looking up towards the camera with a playful teasing smirk, holding a vintage brass key in her hand. "
            "+对话或独白: “再废话，今晚就拿你烤了抵债。” "
            "+环境音: 荒废动物园的风声与生锈铁门吱呀声 "
            "Photorealistic 8k, cinematic lighting, shallow depth of field, 16:9 widescreen."
        )
    },
    {
        "id": 3,
        "name": "shot03_debt_contract",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Dramatic medium shot: At the rusted desolate iron gate of an overgrown abandoned zoo, two aggressive debt collectors in suits confront a young woman, violently slamming a white legal debt contract folder onto the hood of an old off-road car. "
            "+对话或独白: “姜小姐！这是一千万债务合同！一个月不还清，动物园全被法拍！” "
            "+环境音: 纸张重重拍击声与汽车引擎怠速轰鸣 "
            "Cinematic dramatic tension, overcast autumn daylight, 16:9 widescreen."
        )
    },
    {
        "id": 4,
        "name": "shot04_system_awakening",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Suspense close-up: In the overgrown dilapidated zoo courtyard, 24-year-old woman Jiang Jin looks stunned as a glowing translucent neon-cyan holographic UI system screen materializes in the air before her eyes. "
            "+对话或独白: “叮！奇迹动物园救赎系统绑定中，解锁万兽通识语感！” "
            "+声音效果: 清脆的高科技全息数码启动提示音与科幻脉冲 "
            "Photorealistic sci-fi cinematic drama, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 5,
        "name": "shot05_lion_climax_hook",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Climax cliffhanger horror shot: Inside the ruined predator enclosure of the zoo at dusk, a gigantic terrifying adult male lion with a scarred nose violently lunges against a heavy steel wire fence, bending the metal bars, roaring with massive fangs bared, amber eyes burning with savage fury. Red emergency alarm lights flash through smoke. "
            "+对话或独白: “吼——！！” "
            "+声音效果: 震耳欲聋的狂暴雄狮咆哮伴随刺耳警报警笛声 "
            "Cinematic suspense thriller, dramatic crimson and amber lighting, 16:9 widescreen."
        )
    }
]

def check_credit_exhaustion(text):
    keywords = [
        "点数不足", "点数已用完", "额度不足", "额度已用尽", "信用点不足", "没有足够的点数",
        "您已用完每日点数", "点数已耗尽", "insufficient credits", "out of credits", "no credits left", "quota exceeded"
    ]
    for kw in keywords:
        if kw in text.lower():
            return True, kw
    return False, None

def generate_shot(page, shot):
    shot_id = shot["id"]
    shot_name = shot["name"]
    prompt = shot["prompt"]
    target_mp4 = OUTPUT_DIR / f"{shot_name}.mp4"

    if target_mp4.exists() and target_mp4.stat().st_size > 500000:
        print(f"⏭ [Shot {shot_id}] 已存在 ({target_mp4.stat().st_size} bytes)，跳过。")
        return True

    print(f"\n==================================================")
    print(f"🎬 [Shot {shot_id}] 开始生成: {shot_name}")
    print(f"==================================================")

    # 1. 检查是否已有等待批准的请求
    active_approve = page.locator('.option-label:has-text("一律批准"):not(.dimmed), .option-label:has-text("批准"):not(.dimmed)')
    if active_approve.count() > 0:
        print("   ✓ 发现已有未确认的批准请求，直接点击批准！")
        active_approve.last.click()
        time.sleep(2)
    else:
        # 聚焦输入框并填入提示词
        input_box = page.locator('.ProseMirror, [contenteditable="true"]').first
        input_box.wait_for(state="visible", timeout=15000)
        input_box.click()
        time.sleep(0.5)

        input_box.fill(prompt)
        time.sleep(1.5)

        # 点击提交
        gen_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button, button[aria-label*="生成"]').first
        gen_btn.click()
        time.sleep(3)

    # 3. 检查是否有额度不足弹窗或提示
    body_text = page.locator("body").inner_text()
    exhausted, reason = check_credit_exhaustion(body_text)
    if exhausted:
        print(f"🚨【重要报警】：检测到 Google Flow 账号点数已耗尽！原因: '{reason}'")
        page.screenshot(path=str(LOGS_DIR / f"credit_exhausted_shot_{shot_id}.png"))
        return "OUT_OF_CREDITS"

    # 4. 批准点数消耗
    print("   ➤ 监听审批弹窗...")
    for _ in range(12):
        time.sleep(1.5)
        active_approve = page.locator('.option-label:has-text("一律批准"):not(.dimmed), .option-label:has-text("批准"):not(.dimmed), button:has-text("一律批准"), button:has-text("批准")')
        if active_approve.count() > 0:
            target_btn = active_approve.last
            try:
                target_btn.click()
                print("   ✓ 成功点击批准消耗点数！")
                break
            except Exception as e:
                print("   重试点击批准:", e)

    # 再次检查点数是否在点击批准后提示不足
    time.sleep(2)
    body_text = page.locator("body").inner_text()
    exhausted, reason = check_credit_exhaustion(body_text)
    if exhausted:
        print(f"🚨【重要报警】：批准后检测到点数不足！原因: '{reason}'")
        page.screenshot(path=str(LOGS_DIR / f"credit_exhausted_shot_{shot_id}.png"))
        return "OUT_OF_CREDITS"

    # 5. 监控生成进程
    print("   ➤ 云端 Veo 3.1 - Lite 渲染中 (预计 40-120 秒)...")
    rendered = False
    for sec in range(0, 180, 5):
        time.sleep(5)
        stop_btn = page.locator('button:has(mat-icon:has-text("stop")), mat-icon:has-text("stop")')
        is_generating = stop_btn.count() > 0 and stop_btn.first.is_visible()
        if not is_generating and sec >= 25:
            print(f"   ✓ 渲染完成 (耗时 ~{sec}s)！")
            rendered = True
            break
        if sec % 20 == 0:
            print(f"      ... 渲染中已等待 {sec}s")

    if not rendered:
        print(f"❌ [Shot {shot_id}] 渲染超时！")
        page.screenshot(path=str(LOGS_DIR / f"timeout_shot_{shot_id}.png"))
        return False

    # 6. 下载生成的视频
    time.sleep(3)
    print("   ➤ 正在下载视频文件...")
    chat_thumb = page.locator('img.video-thumbnail').last
    box = chat_thumb.bounding_box()
    page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
    time.sleep(3)

    dl_icon = page.locator('button:has(mat-icon:has-text("download")), mat-icon:has-text("download")').first
    dl_icon.click()
    time.sleep(1.5)

    p_opt = page.locator('button:has-text("720p"), *:has-text("720p")').last
    with page.expect_download(timeout=60000) as dl_info:
        p_opt.click()

    dl = dl_info.value
    dl.save_as(str(target_mp4))
    print(f"🎉 [Shot {shot_id}] 成功下载并保存: {target_mp4.name} ({target_mp4.stat().st_size / 1024 / 1024:.2f} MB)")

    # 点击完成或返回
    done_btn = page.locator('button:has-text("完成"), button:has-text("Done")').first
    if done_btn.count() > 0 and done_btn.is_visible():
        done_btn.click()
    time.sleep(2)
    return True

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            accept_downloads=True
        )
        context.add_cookies(playwright_cookies)
        page = context.new_page()

        print("访问 Google Flow 项目...")
        page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        page.mouse.click(160, 650)
        time.sleep(5)

        for shot in SHOTS:
            res = generate_shot(page, shot)
            if res == "OUT_OF_CREDITS":
                print("\n" + "!"*80)
                print("🛑 任务立即停止：FLOW账号点数已用完！正在通知用户更换账号。严禁用其他方式去生成！")
                print("!"*80 + "\n")
                browser.close()
                sys.exit(42)  # 特殊退出码 42 表示点数耗尽
            elif not res:
                print(f"❌ Shot {shot['id']} 生成失败！")
                browser.close()
                sys.exit(1)

        print("\n🎉 所有分镜视频均已通过 Google Flow Veo 3.1 - Lite 生产完毕！")
        browser.close()

if __name__ == "__main__":
    main()
