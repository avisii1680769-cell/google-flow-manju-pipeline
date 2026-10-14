#!/usr/bin/env python3
"""
flow_account_manager.py
Multi-account rotation and credit management engine for Google Flow (Veo 3.1 - Lite).

Key Capabilities:
1. Multi-account pool management (supporting N Google Pro accounts).
2. Priority Policy: Always prioritize consuming the daily 50 bonus points first (since daily points do not accumulate).
3. Automated Account Switching: Seamlessly switches to the next account when current account runs out of credits.
4. Cookie Expiration Detection & Failover: Detects expired cookies (redirect to login), logs the issue, and moves to the next valid account.
5. Strict Halt Rule: If all available accounts are exhausted or expired, pauses execution and directly requests updated cookies from the user without skipping steps.
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

PIPELINE_ROOT = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline")
CONFIG_DIR = PIPELINE_ROOT / "config"
ACCOUNTS_POOL_FILE = CONFIG_DIR / "accounts_pool.json"

class FlowAccountManager:
    def __init__(self, pool_file: Path = ACCOUNTS_POOL_FILE):
        self.pool_file = pool_file
        self.config_dir = pool_file.parent
        self.accounts: List[Dict] = []
        self.current_index = 0
        self.load_pool()

    def load_pool(self):
        """Loads account configurations and cookies from pool file."""
        if not self.pool_file.exists():
            self._init_default_pool()
        else:
            with open(self.pool_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.accounts = data.get("accounts", [])
                self.current_index = data.get("current_index", 0)

    def _init_default_pool(self):
        """Initializes default pool structure from existing cookie files."""
        self.accounts = [
            {
                "id": "acc_01",
                "name": "Google Pro 主账号 (Account 1)",
                "cookie_file": "flow_cookies.json",
                "daily_credits_claimed": True,
                "credits_remaining": 50,
                "status": "UNKNOWN",
                "note": "每日50点优先消耗"
            },
            {
                "id": "acc_02",
                "name": "Google Pro 备用账号 (Account 2)",
                "cookie_file": "flow_cookies_acc2.json",
                "daily_credits_claimed": True,
                "credits_remaining": 50,
                "status": "UNKNOWN",
                "note": "每日50点优先消耗"
            }
        ]
        self.save_pool()

    def save_pool(self):
        """Persists pool state to disk."""
        data = {
            "policy": "PRIORITIZE_DAILY_50_POINTS",
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "current_index": self.current_index,
            "accounts": self.accounts
        }
        with open(self.pool_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_playwright_cookies(self, account_index: int) -> List[Dict]:
        """Reads cookie file and converts to Playwright format."""
        if account_index >= len(self.accounts):
            return []
        acc = self.accounts[account_index]
        cookie_path = self.config_dir / acc["cookie_file"]
        if not cookie_path.exists():
            return []

        with open(cookie_path, "r", encoding="utf-8") as f:
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
        return playwright_cookies

    def verify_account(self, page, account_index: int) -> Tuple[bool, str]:
        """
        Navigates to Flow and verifies login & credit status.
        Returns (is_valid, reason).
        """
        acc = self.accounts[account_index]
        print(f"🔍 [AccountManager] 正在验证账号 [{acc['name']}]...")

        try:
            page.goto("https://flow.google.com/", wait_until="domcontentloaded", timeout=45000)
            time.sleep(3)

            # Check if redirected to landing page or signin
            create_btn = page.locator('text="Create with Google Flow"').first
            if create_btn.is_visible():
                print(f"⚠️ [{acc['name']}] 检测到落地页登录按钮，正在验证会话有效性...")
                create_btn.click()
                time.sleep(4)

            if "accounts.google.com" in page.url or "signin" in page.url:
                acc["status"] = "EXPIRED"
                acc["last_error"] = "Session expired, redirected to Google Sign-in"
                self.save_pool()
                return False, "COOKIE_EXPIRED"

            # Check credits / canvas access
            body_text = page.locator("body").inner_text()
            exhausted_keywords = [
                "点数不足", "点数已用完", "额度不足", "额度已用尽", "信用点不足", "没有足够的点数",
                "您已用完每日点数", "点数已耗尽", "insufficient credits", "out of credits", "quota exceeded"
            ]
            for kw in exhausted_keywords:
                if kw in body_text:
                    acc["status"] = "CREDITS_EXHAUSTED"
                    acc["credits_remaining"] = 0
                    self.save_pool()
                    return False, f"CREDITS_EXHAUSTED ({kw})"

            acc["status"] = "ACTIVE"
            self.save_pool()
            return True, "ACTIVE"

        except Exception as e:
            acc["status"] = "ERROR"
            acc["last_error"] = str(e)
            self.save_pool()
            return False, f"EXCEPTION: {e}"

    def switch_to_next_account(self) -> Optional[int]:
        """Finds next eligible account in the pool."""
        for i in range(len(self.accounts)):
            idx = (self.current_index + 1 + i) % len(self.accounts)
            if self.accounts[idx]["status"] not in ["EXPIRED", "CREDITS_EXHAUSTED"]:
                self.current_index = idx
                self.save_pool()
                print(f"🔄 [AccountManager] 成功切换至账号: {self.accounts[idx]['name']}")
                return idx
        print("⚠️ [AccountManager] 所有账号点数均已耗尽或 Cookie 已过期！")
        return None

if __name__ == "__main__":
    mgr = FlowAccountManager()
    print(f"Loaded {len(mgr.accounts)} accounts.")
    print(json.dumps(mgr.accounts, ensure_ascii=False, indent=2))
