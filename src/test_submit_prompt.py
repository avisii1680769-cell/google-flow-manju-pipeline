#!/usr/bin/env python3
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_PATH = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/config/flow_cookies.json")
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

TEST_PROMPT = (
    "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
    "A small comical scruffy Eurasian tree sparrow perched on a rusty weathered zoo signboard. "
    "The sparrow suddenly fluffs its feathers in utter comical disbelief and shock, chirping and squawking with cartoonish expressive wide eyes. "
    "+对话或独白: “卧槽！两脚兽成精了！她真能听懂我骂她？！” "
    "+环境音: 荒废动物园的风吹过杂草的沙沙声与远处微弱鸟鸣 "
    "Cinematic photorealistic 8k, shallow depth of field, 16:9 widescreen."
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

    page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(5)

    # Click last created project or 新建项目
    page.locator('*:has-text("新建项目")').last.click()
    time.sleep(5)

    # 检查输入框
    input_box = page.locator('.ProseMirror, textarea, [contenteditable="true"]').first
    print("Input box count:", input_box.count())
    input_box.click()
    time.sleep(1)

    print("Typing prompt...")
    input_box.fill(TEST_PROMPT)
    time.sleep(2)

    page.screenshot(path=str(LOGS_DIR / "flow_prompt_filled.png"))

    # 点击提交/生成
    gen_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button, button[aria-label*="生成"]').first
    print("Found gen_btn:", gen_btn.count())
    gen_btn.click()
    time.sleep(3)

    page.screenshot(path=str(LOGS_DIR / "flow_after_gen_click.png"))

    # 监控 60 秒：检测点数不足、审批弹窗、或生成状态
    print("Monitoring response and credit status...")
    credit_exhausted = False
    started_generation = False

    for sec in range(0, 60, 3):
        time.sleep(3)
        body_text = page.locator("body").inner_text()

        # 检查是否有点数不足或额度耗尽提示
        error_keywords = ["点数不足", "点数已用完", "额度不足", "额度已用尽", "信用点不足", "no credits", "insufficient credits", "out of credits", "quota exceeded"]
        for kw in error_keywords:
            if kw in body_text.lower():
                print(f"🚨 检测到点数耗尽错误: '{kw}'")
                credit_exhausted = True
                break

        if credit_exhausted:
            break

        # 检查批准弹窗
        approve_btn = page.locator('text=一律批准').or_(page.locator('text=批准')).or_(page.locator('button:has-text("批准")'))
        if approve_btn.count() > 0 and approve_btn.first.is_visible():
            print(f"   ✓ 捕获到审批弹窗，点击批准！(第 {sec}s)")
            approve_btn.first.click()
            time.sleep(2)

        # 检查生成中状态 / 卡片
        cards = page.locator("img.video-thumbnail, .media-wrapper, img.thumbnail, [class*='generating'], [class*='progress']").count()
        if cards > 0:
            print(f"   ✓ 检测到生成进度/媒体卡片 (第 {sec}s)！")
            started_generation = True
            break

    page.screenshot(path=str(LOGS_DIR / "flow_monitoring_status.png"))

    print(f"Result: credit_exhausted={credit_exhausted}, started_generation={started_generation}")
    print("Body text snippet (last 1000 chars):")
    print(page.locator("body").inner_text()[-1000:])

    browser.close()
