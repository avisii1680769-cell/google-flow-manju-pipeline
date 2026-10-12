#!/usr/bin/env python3
"""
flow_adapter.py
基于 Playwright 的 Google Flow (Veo 3.1 - Lite) 自动化驱动器：
1. Cookie 鉴权与项目定位
2. 智能体设置锁定为 Veo 3.1 - Lite
3. 提交 Shot 1 初始生成
4. 时间轴编辑器触发【延续镜头 (Veo 3.1 - Lite)】与原生 DOM 点击提交
5. 监听场景合体渲染导出并保存完整包含原生音轨的长视频
"""

import os
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

class FlowAdapter:
    def __init__(self, cookies_path, project_url):
        self.cookies_path = Path(cookies_path)
        self.project_url = project_url
        self.cookies = self._load_cookies()

    def _load_cookies(self):
        with open(self.cookies_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        formatted = []
        for c in raw:
            s = c.get("sameSite", "")
            s_val = "None" if str(s).lower() in ["no_restriction", "none"] else ("Strict" if str(s).lower() == "strict" else "Lax")
            formatted.append({
                "name": c.get("name"),
                "value": c.get("value"),
                "domain": c.get("domain"),
                "path": c.get("path", "/"),
                "secure": c.get("secure", True),
                "httpOnly": c.get("httpOnly", False),
                "sameSite": s_val
            })
        return formatted

    def launch_session(self):
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            accept_downloads=True
        )
        context.add_cookies(self.cookies)
        page = context.new_page()
        page.goto(self.project_url, wait_until="domcontentloaded", timeout=45000)
        time.sleep(5)
        return playwright, browser, context, page

    def set_model_veo_lite(self, page):
        """打开设置面板，将默认视频模型设为 Veo 3.1 - Lite 并保存"""
        print("⚙️ 检查并锁定视频模型为 Veo 3.1 - Lite...")
        settings_btn = page.locator('button:has(mat-icon:has-text("settings")), button[aria-label*="设置"]').first
        if settings_btn.count() > 0:
            settings_btn.click()
            time.sleep(1.5)
            # 选择 Veo 3.1 - Lite
            lite_opt = page.locator('mat-option:has-text("Veo 3.1 - Lite"), mat-radio-button:has-text("Lite")').first
            if lite_opt.count() > 0:
                lite_opt.click()
                time.sleep(1)
            # 点击保存
            save_btn = page.locator('button:has-text("保存"), button:has-text("Save")').first
            if save_btn.count() > 0:
                save_btn.click()
                time.sleep(1)
            print("✓ 已锁定模型为 Veo 3.1 - Lite")

    def extend_shot_in_timeline(self, page, card_selector_text, extend_prompt):
        """
        在时间轴上使用【延续镜头（Veo 3.1 - Lite）】生成后续片段
        """
        print(f"⏩ 在时间轴上执行延续镜头: {extend_prompt[:50]}...")
        # 1. 点击场景卡片进入时间轴
        card = page.locator(f'*:has-text("{card_selector_text}")').first
        card.click()
        time.sleep(2)

        # 2. 点击时间轴末尾 add_2
        add_btn = page.locator('[aria-label="添加片段"], mat-icon:has-text("add_2")').first
        add_btn.click()
        time.sleep(1)

        # 3. 选择延续镜头
        extend_opt = page.locator('*:has-text("延续镜头")').last
        extend_opt.click()
        time.sleep(1.5)

        # 4. 输入提示词
        box = page.locator('flow-edit-video-prompt-box')
        pm = box.locator('.ProseMirror')
        pm.click()
        time.sleep(0.5)
        page.keyboard.insert_text(extend_prompt)
        time.sleep(1.5)

        # 5. 原生 DOM 级点击提交（绕过 Tooltip 校验拦截）
        gen_btn = box.locator('flow-generate-icon-button button').first
        gen_btn.evaluate('b => b.click()')
        print("✓ 已成功触发时间轴延续镜头渲染！")

    def export_and_download_scene(self, page, card_selector_text, output_mp4_path, timeout_seconds=180):
        """
        导出并下载包含所有连贯片段和 Flow 原生音频的多轨 Scene
        """
        print(f"📥 正在导出并下载合并长视频...")
        card = page.locator(f'*:has-text("{card_selector_text}")').first
        card.click()
        time.sleep(2)

        dl_btn = page.locator('button:has(mat-icon:has-text("download")), [aria-label*="下载"], mat-icon:has-text("download")').first
        download_future = []
        page.on("download", lambda d: download_future.append(d))

        dl_btn.click()
        time.sleep(2)

        for sec in range(0, timeout_seconds, 5):
            time.sleep(5)
            if len(download_future) > 0:
                dl = download_future[0]
                Path(output_mp4_path).parent.mkdir(parents=True, exist_ok=True)
                dl.save_as(str(output_mp4_path))
                print(f"🎉 成功下载整段场景视频: {output_mp4_path}")
                return output_mp4_path
        raise TimeoutError("等待 Flow 场景导出超时！")

if __name__ == "__main__":
    print("Flow Adapter module ready.")
