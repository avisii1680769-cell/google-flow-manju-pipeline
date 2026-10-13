#!/usr/bin/env python3
"""
generate_ep01_extended_flow.py
Sequentially generates the remaining 7 extended narrative shots (Shots 12 to 18)
for Episode 1 in Google Flow (Veo 3.1 - Lite).
Strict Rule: If credits are exhausted, IMMEDIATELY exit with 42 and notify user.
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

REMAINING_7_SHOTS = [
    {
        "id": 12,
        "filename": "shot12_peacock_complaint.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Humorous cinematic shot of a ragged peacock perched on a weathered wooden fence, comically fluffing its feathers and haughtily squawking. "
            "+环境音: 孔雀滑稽高亢的尖叫声与振翅扑棱声 "
            "Natural daylight, rich wildlife textures, 16:9 widescreen composition."
        )
    },
    {
        "id": 13,
        "filename": "shot13_raccoon_snack_heist.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Humorous wildlife shot of a fluffy raccoon poking its head out from an old metal trash can, holding a cookie tightly with its tiny paws and looking around guiltily. "
            "+环境音: 垃圾桶金属轻响与小爪子窸窸窣窣声 "
            "Cinematic depth of field, photorealistic animal fur, 16:9 widescreen."
        )
    },
    {
        "id": 14,
        "filename": "shot14_monkey_gossip.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Humorous dramatic shot of a small golden monkey sitting on an artificial rock, scratching its head and jumping up and down in frantic excitement. "
            "+环境音: 猴子急促恐慌的吱吱尖叫声与急躁蹦跳声 "
            "Natural lighting, expressive wildlife textures, 16:9 widescreen."
        )
    },
    {
        "id": 15,
        "filename": "shot15_heroine_turning_serious.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Dynamic tracking shot of 24-year-old Asian woman Jiang Jin with a black ponytail, turning sharply with an alert serious expression and running down an overgrown path towards the predator enclosure. "
            "+环境音: 急促的战靴奔跑脚步声与沉重紧张的低音 "
            "Cinematic motion blur, 16:9 widescreen."
        )
    },
    {
        "id": 16,
        "filename": "shot16_predator_tunnel_alarm.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Atmospheric suspense shot inside a concrete zoo corridor leading to the predator enclosure, spinning red emergency beacon lights flashing vivid crimson reflections across the damp walls. "
            "+声音效果: 旋转红灯警报蜂鸣声与深处沉闷的撞击轰鸣 "
            "Cinematic anamorphic lighting, psychological thrill, 16:9 widescreen."
        )
    },
    {
        "id": 17,
        "filename": "shot17_ground_shake_chains.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Dramatic macro shot of heavy rusted steel chains violently rattling and jerking against iron pillars, dust falling from cracked concrete walls as huge unseen force shakes the cage. "
            "+声音效果: 粗重铁链剧烈撞击铁柱的刺耳金属撞击声与地面震动声 "
            "Industrial cinematic aesthetic, dramatic lighting, 16:9 widescreen."
        )
    },
    {
        "id": 18,
        "filename": "shot18_heroine_approaching_cage.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Suspense shot of 24-year-old woman Jiang Jin stopping outside a massive reinforced steel gate under flashing red emergency lights, her hand on the heavy iron latch as smoke drifts through the bars. "
            "+环境音: 警报声中沉重急促的喘息声与门后极具压迫感的野兽喘息 "
            "Cinematic thriller climax, crimson rim lighting, 16:9 widescreen."
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

def main():
    print("🚀 启动 Google Flow (Veo 3.1 - Lite) 剩余 7 镜头全自动化渲染...")
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

        print("➤ 正在打开 Google Flow 官方工作区...")
        page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)

        if "about" in page.url:
            print("🚨【错误】：账号被重定向至 about 介绍页，会话可能失效！立即停止。")
            page.screenshot(path=str(LOGS_DIR / "session_expired_about.png"))
            browser.close()
            sys.exit(42)

        # 定位项目卡片并可靠点击
        proj_title = page.locator('text="10月 13 - 21:12"').first
        proj_title.scroll_into_view_if_needed()
        time.sleep(1)
        box = proj_title.bounding_box()
        page.mouse.click(box['x'] + 50, box['y'] - 50)
        time.sleep(6)

        input_box = page.locator('.ProseMirror, [contenteditable="true"]').first
        if not input_box.is_visible():
            print("❌ 无法定位 Flow 输入框，保存截图并停止。")
            page.screenshot(path=str(LOGS_DIR / "canvas_input_not_found.png"))
            browser.close()
            sys.exit(1)

        print("✓ 成功进入 Flow 项目画布，准备按顺序渲染剩余 7 个镜头！")

        for shot in REMAINING_7_SHOTS:
            shot_id = shot["id"]
            filename = shot["filename"]
            prompt = shot["prompt"]
            out_path = OUTPUT_DIR / filename

            if out_path.exists() and out_path.stat().st_size > 500000:
                print(f"⏭ [Shot {shot_id}] 已在本地磁盘就绪 ({out_path.stat().st_size / 1024 / 1024:.2f} MB)，跳过。")
                continue

            print(f"\n==================================================")
            print(f"🎬 [Shot {shot_id}] 开始在 Google Flow 中渲染: {filename}")
            print(f"==================================================")

            init_thumbs = page.locator('img.video-thumbnail').count()
            print(f"   当前画布缩略图基准数量: {init_thumbs}")

            # 聚焦并清空输入框
            input_box.click()
            time.sleep(0.5)
            input_box.fill(prompt)
            time.sleep(1.0)

            arrow_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button')
            if arrow_btn.count() > 0 and arrow_btn.first.is_visible():
                arrow_btn.first.click()
                print("   ➤ 点击发送生成箭头")
            else:
                input_box.press("Enter")
                print("   ➤ 按回车发送生成指令")
            time.sleep(3)

            # 严格检查点数是否耗尽
            body_text = page.locator("body").inner_text()
            exhausted, kw = check_credit_exhaustion(body_text)
            if exhausted:
                print(f"\n🚨🚨🚨【点数警报】：检测到点数耗尽错误 '{kw}'！立即停止任务并通知用户！")
                page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_credit_exhausted.png"))
                browser.close()
                sys.exit(42)

            # 等待云端 Veo 3.1 - Lite 渲染完成 (最多 180 秒)
            print("   ➤ 正在等待 Google Flow (Veo 3.1 - Lite) 云端渲染完成...")
            rendered = False
            for sec in range(0, 180, 10):
                time.sleep(10)
                curr_thumbs = page.locator('img.video-thumbnail').count()
                stop_btn = page.locator('button:has(mat-icon:has-text("stop")), mat-icon:has-text("stop"), button:has-text("停止")')
                is_generating = stop_btn.count() > 0 and stop_btn.first.is_visible()

                body_text = page.locator("body").inner_text()
                exhausted, kw = check_credit_exhaustion(body_text)
                if exhausted:
                    print(f"\n🚨🚨🚨【点数警报】：渲染中检测到点数耗尽 '{kw}'！立即停止！")
                    page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_credit_exhausted.png"))
                    browser.close()
                    sys.exit(42)

                if curr_thumbs > init_thumbs and not is_generating:
                    print(f"   ✓ 视频已成功生成！(缩略图数从 {init_thumbs} 增至 {curr_thumbs}，耗时 ~{sec}s)")
                    rendered = True
                    break

                if sec % 30 == 0:
                    print(f"      ... 云端处理中 ({sec}s elapsed, thumbs={curr_thumbs})")

            if not rendered:
                print(f"   ⚠️ 未在预期时间内检测到新缩略图，检查是否有卡片生成...")
                page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_status.png"))
                curr_thumbs = page.locator('img.video-thumbnail').count()
                if curr_thumbs <= init_thumbs:
                    print(f"❌ Shot {shot_id} 未能生成视频卡片，停止任务。")
                    browser.close()
                    sys.exit(1)

            # 下载原画质视频
            print(f"   ➤ 正在下载 Shot {shot_id} 视频流...")
            thumbs = page.locator('img.video-thumbnail')
            last_thumb = thumbs.last
            box = last_thumb.bounding_box()
            page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
            time.sleep(3)

            dl_icon = page.locator('button:has(mat-icon:has-text("download")), mat-icon:has-text("download")').first
            if dl_icon.count() > 0:
                dl_icon.click()
                time.sleep(1.5)
                p_opt = page.locator('button:has-text("720p"), *:has-text("720p")').last
                with page.expect_download(timeout=60000) as dl_info:
                    p_opt.click()
                dl = dl_info.value
                dl.save_as(str(out_path))
                print(f"   🎉 Shot {shot_id} 下载完成: {out_path.name} ({out_path.stat().st_size / 1024 / 1024:.2f} MB)")
            else:
                print(f"   ❌ 未能找到下载按钮，保存截图并停止。")
                page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_no_dl.png"))
                browser.close()
                sys.exit(1)

            # 关闭播放器模态框返回画布
            done_btn = page.locator('button:has-text("完成"), button:has-text("Done")').first
            if done_btn.count() > 0 and done_btn.is_visible():
                done_btn.click()
            time.sleep(2)

        print("\n==================================================")
        print("🎉 全部 18 个镜头均已在 Google Flow 中渲染完成！")
        print("==================================================")
        browser.close()

if __name__ == "__main__":
    main()
