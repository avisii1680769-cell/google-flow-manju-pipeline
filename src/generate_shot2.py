#!/usr/bin/env python3
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_PATH = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/config/flow_cookies.json")
OUTPUT_PATH = Path("/root/.agy-avisii/.gemini/production/ep01_flow_raw/shot02_heroine_smirk.mp4")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
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

PROMPT_SHOT2 = (
    "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
    "Medium close-up shot of an attractive fictional 24-year-old Asian woman zoo keeper with a high black ponytail, wearing an olive cargo utility jacket. "
    "She turns her head looking towards the camera with a playful confident smirk, holding an antique brass key in a sunny ruined zoo. "
    "+对话或独白: “小家伙，你刚才在叫唤什么？” "
    "+环境音: 动物园清晨的微风与树叶沙沙声 "
    "Photorealistic 8k, soft cinematic daylight, shallow depth of field, 16:9 widescreen."
)

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

    print("Opening Google Flow...")
    page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)
    
    # Click first project
    page.mouse.click(160, 650)
    time.sleep(5)
    
    # 聚焦并输入提示词
    print("Typing prompt for Shot 2...")
    input_box = page.locator('.ProseMirror, [contenteditable="true"]').first
    input_box.click()
    time.sleep(0.5)
    input_box.fill(PROMPT_SHOT2)
    time.sleep(1.5)
    
    # 点击生成按钮
    print("Clicking generate button...")
    gen_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button').first
    gen_btn.click()
    time.sleep(3)
    
    # 监听确认批准
    for i in range(8):
        time.sleep(1.5)
        approve_btn = page.locator('.option-label:has-text("一律批准"):not(.dimmed), .option-label:has-text("批准"):not(.dimmed), button:has-text("批准")')
        if approve_btn.count() > 0 and approve_btn.last.is_visible():
            approve_btn.last.click()
            print("✓ Clicked approve button!")
            break
            
    # 等待渲染完成 (最多 180 秒)
    print("Monitoring rendering progress (waiting up to 180s)...")
    rendered = False
    for sec in range(0, 180, 5):
        time.sleep(5)
        stop_btn = page.locator('button:has(mat-icon:has-text("stop")), mat-icon:has-text("stop")')
        is_generating = stop_btn.count() > 0 and stop_btn.first.is_visible()
        if not is_generating and sec >= 30:
            print(f"✓ Rendering finished at ~{sec}s!")
            rendered = True
            break
        if sec % 20 == 0:
            print(f"   ... Rendering in progress ({sec}s elapsed)")
            
    page.screenshot(path=str(LOGS_DIR / "shot2_rendered_canvas.png"))
    
    # 检查视频缩略图并下载
    print("Locating video thumbnail to download...")
    chat_thumbs = page.locator('img.video-thumbnail')
    if chat_thumbs.count() > 0:
        last_thumb = chat_thumbs.last
        box = last_thumb.bounding_box()
        page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        time.sleep(3)
        
        dl_icon = page.locator('button:has(mat-icon:has-text("download")), mat-icon:has-text("download")').first
        dl_icon.click()
        time.sleep(1.5)
        
        p_opt = page.locator('button:has-text("720p"), *:has-text("720p")').last
        with page.expect_download(timeout=60000) as dl_info:
            p_opt.click()
            
        dl = dl_info.value
        dl.save_as(str(OUTPUT_PATH))
        print(f"🎉 Shot 2 downloaded successfully: {OUTPUT_PATH.name} ({OUTPUT_PATH.stat().st_size / 1024 / 1024:.2f} MB)")
    else:
        print("❌ No video thumbnail found, inspecting chat text:")
        print(page.locator('body').inner_text()[-1000:])
        
    browser.close()
