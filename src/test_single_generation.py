import json, time, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_PATH = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/config/flow_cookies.json")
OUTPUT_DIR = Path("/root/.agy-avisii/.gemini/production/ep01_flow_raw")
LOGS_DIR = Path("/root/.agy-gabor/.gemini/antigravity-cli/brain/aba683fa-a376-46a0-93b9-3717daeb52a2")

with open(COOKIES_PATH, "r", encoding="utf-8") as f:
    raw_cookies = json.load(f)

playwright_cookies = []
for c in raw_cookies:
    s = c.get("sameSite", "")
    s_val = "None" if str(s).lower() in ["no_restriction", "none"] else ("Strict" if str(s).lower() == "strict" else "Lax")
    playwright_cookies.append({
        "name": c.get("name"), "value": c.get("value"), "domain": c.get("domain"),
        "path": c.get("path", "/"), "secure": c.get("secure", True), "httpOnly": c.get("httpOnly", False),
        "sameSite": s_val
    })

def check_credit_exhaustion(text):
    keywords = [
        "点数不足", "点数已用完", "额度不足", "额度已用尽", "信用点不足", "没有足够的点数",
        "您已用完每日点数", "点数已耗尽", "insufficient credits", "out of credits", "no credits left", "quota exceeded"
    ]
    for kw in keywords:
        if kw in text.lower():
            return True, kw
    return False, None

prompt = (
    "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
    "Dramatic close-up shot: An aggressive debt collector in a dark suit furiously points his finger directly at the camera with a menacing snarl outside an overgrown rusty gate. "
    "+对话或独白: “一个月不还清，把你和这破动物园一起办了！” "
    "+环境音: 荒废动物园的冷风与生锈铁链撞击声 "
    "Cinematic lighting, photorealistic, 16:9 widescreen."
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    ctx.add_cookies(playwright_cookies)
    page = ctx.new_page()

    print("1. 打开 Google Flow...")
    page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)

    print("2. 进入项目...")
    page.mouse.click(160, 650)
    time.sleep(5)

    init_thumbs = page.locator('img.video-thumbnail').count()
    print(f"当前画布缩略图数量: {init_thumbs}")

    # 聚焦输入框
    input_box = page.locator('.ProseMirror, [contenteditable="true"]').first
    input_box.click()
    time.sleep(0.5)
    input_box.fill(prompt)
    time.sleep(1.5)

    # 点击提交
    gen_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button').first
    gen_btn.click()
    time.sleep(3)

    # 检查点数耗尽
    body_text = page.locator("body").inner_text()
    exhausted, kw = check_credit_exhaustion(body_text)
    if exhausted:
        print(f"🚨【报警】：点数耗尽错误 '{kw}'！立即停止任务并通知用户！")
        browser.close()
        sys.exit(42)

    # 自动批准点数 (若出现)
    for _ in range(6):
        time.sleep(1.5)
        active_approve = page.locator('.option-label:has-text("一律批准"):not(.dimmed), .option-label:has-text("批准"):not(.dimmed), button:has-text("批准")')
        if active_approve.count() > 0 and active_approve.last.is_visible():
            try:
                active_approve.last.click()
                print("   ✓ 点击批准消耗点数")
                break
            except:
                pass

    print("3. 等待渲染完成...")
    rendered = False
    for sec in range(0, 180, 5):
        time.sleep(5)
        curr_thumbs = page.locator('img.video-thumbnail').count()
        stop_btn = page.locator('button:has(mat-icon:has-text("stop")), mat-icon:has-text("stop")')
        is_generating = stop_btn.count() > 0 and stop_btn.first.is_visible()

        if curr_thumbs > init_thumbs and not is_generating:
            print(f"   ✓ 视频渲染就绪！(缩略图数从 {init_thumbs} 增至 {curr_thumbs}，耗时 ~{sec}s)")
            rendered = True
            break
        if sec % 20 == 0:
            print(f"   ... 渲染中 ({sec}s elapsed)")

    if rendered:
        print("4. 下载新生成的视频...")
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
            out_file = OUTPUT_DIR / "shot04_debt_shout.mp4"
            with page.expect_download(timeout=60000) as dl_info:
                p_opt.click()
            dl = dl_info.value
            dl.save_as(str(out_file))
            print(f"   🎉 下载成功: {out_file.name} ({out_file.stat().st_size / 1024 / 1024:.2f} MB)")
        else:
            print("   未找到下载按钮")
    else:
        print("   渲染超时或失败")

    browser.close()
