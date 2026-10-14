#!/usr/bin/env python3
"""
flow_episode2_producer.py
Automated Google Flow (Veo 3.1 - Lite) generator for Episode 2 of 《继承动物园后，我通兽语成为国家团宠》.

Adheres strictly to all production rules:
1. 100% Pure Google Flow (Veo 3.1 - Lite) Native Audio & Video.
2. Zero external TTS. Subtitles and audio are 100% Flow native.
3. Multi-account automatic rotation (prioritizing daily 50 bonus credits).
4. Policy-safe prompts (celebrity-free character descriptions).
5. Safe failover: If accounts expire or credits run out, immediately pauses and notifies user.
"""

import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

from flow_account_manager import FlowAccountManager

PIPELINE_ROOT = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline")
RAW_OUTPUT_DIR = Path("/root/.agy-avisii/.gemini/production/ep02_flow_raw")
RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR = Path("/root/.agy-gabor/.gemini/antigravity-cli/brain/aba683fa-a376-46a0-93b9-3717daeb52a2")

EPISODE_02_SHOTS = [
    {
        "id": 1,
        "filename": "ep02_shot01_lion_charge.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Golden 5 seconds high stakes thriller opening: Close-up low angle shot looking up at a colossal, scarred male African lion (Golden Mane / 金鬃). "
            "The lion ferociously charges forward, slamming directly against the camera lens/cage bars with massive lethal fangs bared in a terrifying deafening roar, saliva spraying under flashing emergency lights. "
            "+对话或独白: “吼——！！” "
            "+声音效果: 狂暴雄狮震耳欲聋的咆哮与铁笼剧烈震动撞击声 "
            "Cinematic horror suspense, shallow depth of field, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 2,
        "filename": "ep02_shot02_heroine_push_gate.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Medium shot of a spirited 24-year-old Asian female zoo director, neat high black ponytail, wearing an olive cargo utility jacket. "
            "She stands completely calm before the shaking lion cage. "
            "With firm resolute movement, she calmly unlatches the heavy rusted iron lock and pushes the heavy iron gate wide open, stepping directly inside without flinching. "
            "+对话或独白: “别叫了，我来帮你。” "
            "+环境音: 沉重生锈铁锁咔哒弹开声与铁门吱呀摩擦声 "
            "Cinematic drama, cool shadow lighting, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 3,
        "filename": "ep02_shot03_lion_shock_pause.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Extreme close-up of the giant golden lion: Having missed its charge, the lion freezes mid-motion, amber eyes widening with comedic utter shock and bewilderment, staring at the slender human woman who walked straight in. "
            "+对话或独白: “呜……嗷？人类不怕我？” "
            "+环境音: 雄狮困惑低沉的呜咽声与沉重的粗气喷吐 "
            "Photorealistic animal expression, rich golden fur textures, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 4,
        "filename": "ep02_shot04_lion_whining_wire.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Medium close-up: The massive golden lion suddenly slumps its front paws onto the ground, tilting its head with a comically pitiful, teary-eyed expression, pawing desperately at its swollen left jaw. "
            "+对话或独白: “疼死老子了！牙缝卡了根破铁丝，快帮我拔了啊！” "
            "+环境音: 委屈幼兽般的悲鸣哼唧声与爪子在干草地抓挠声 "
            "Humorous cinematic contrast, natural soft lighting, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 5,
        "filename": "ep02_shot05_heroine_hand_in_mouth.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Tense macro shot: The young female zoo director crouches fearlessly right in front of the giant lion. Her slender hand reaches gently between the lion's razor-sharp white canines, grasping a thick twisted rusty steel wire jammed deep between its teeth. "
            "+对话或独白: “忍一下，马上就好。” "
            "+环境音: 狮子口鼻喷出的滚烫呼吸声与微弱金属卡擦动静 "
            "Extreme cinematic suspense, shallow focus on hands and lion teeth, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 6,
        "filename": "ep02_shot06_wire_extracted.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Close-up tracking shot: With a swift, clean motion, the young female zoo director pulls out a long, blood-stained barbed wire and tosses it onto the concrete floor. The lion instantly relaxes its tense jaw with a deep, relieved sigh. "
            "+对话或独白: “搞定！以后别乱嚼铁笼了。” "
            "+环境音: 金属铁丝当啷掉落水泥地脆响与野兽释然长叹 "
            "Cinematic relief, crisp lighting, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 7,
        "filename": "ep02_shot07_lion_giant_golden_retriever.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Humorous wide medium shot: The gigantic adult male lion lies happily on its back in the hay, acting just like an affectionate giant pet cat. "
            "The lion rolls playfully in the straw, vigorously rubbing its huge golden mane against the young female zoo director's legs, purring loudly and waving its large paws in the air. "
            "+对话或独白: “呜呜呜恩人！太舒服了！还要摸摸下巴！” "
            "+环境音: 震耳欲聋如拖拉机引擎般的狮子愉悦呼噜声 "
            "Heartwarming comedy, natural daylight, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 8,
        "filename": "ep02_shot08_heroine_pat_lion_ears.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Close-up overhead angle: The young female zoo director smiles warmly, her hands affectionately scratching behind the lion's round golden ears and under its chin. The lion squints in sheer ecstasy, front paws paddling the air. "
            "+对话或独白: “堂堂万兽之王，怎么跟个大猫一样。” "
            "+环境音: 惬意打呼噜声与微风拂动发丝 "
            "Gentle warm cinematic lighting, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 9,
        "filename": "ep02_shot09_system_million_reward.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Sci-fi fantasy medium shot: A dazzling neon-gold holographic interface erupts in front of the young woman director, glowing particles floating like sparkling gold coins, displaying system text 'A级猛兽亲和度满级，千倍救赎返现到账：1,000,000元！' "
            "+对话或独白: “叮！成功救助安抚成年雄狮！触发千倍救赎返现，奖励启动资金100万！” "
            "+声音效果: 清脆爆裂的数码全息激活音效与金币连环落袋音 "
            "Futuristic cinematic lighting, high-tech glow, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 10,
        "filename": "ep02_shot10_setup_livestream.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Medium shot: The young female zoo director sets up an old smartphone onto a tripod in the courtyard outside the open lion cage, facing the camera with a confident, bright smile and starting a live stream titled 'Miracle Zoo: Dancing with Lions'. "
            "+对话或独白: “家人们，欢迎来到濒临破产的奇迹动物园。” "
            "+环境音: 手机点触清脆提示音与微风鸟鸣 "
            "Bright natural lighting, dynamic composition, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 11,
        "filename": "ep02_shot11_danmaku_shock.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Macro close-up on the smartphone screen: Live chat comments frantically flood the screen at lightning speed: 'Holy crap is that a real lion?!', 'Run streamer you're gonna get eaten!', 'Fake CGI surely!'. "
            "+环境音: 手机直播间密集疯狂的弹幕刷新提示音与急促警报心跳声 "
            "Crisp modern digital screen display, vibrant colors, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 12,
        "filename": "ep02_shot12_lion_belly_rub_business.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Hilarious medium tracking shot: In the background of the live camera, the giant lion actively trots over, obediently flips onto its back right before the lens, waving its huge black pads and giving a clumsy lion wink. "
            "+对话或独白: “看什么看，本王也是要恰饭的，快给园长点赞！” "
            "+环境音: 雄厚热烈的大鼻子喷气声与大尾巴拍地噗噗声 "
            "Humorous dynamic framing, photorealistic fur, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 13,
        "filename": "ep02_shot13_rocket_carnival_gifts.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Close-up of smartphone interface: Extravagant virtual gift rockets and carnivals explode across the screen with spectacular 3D animations, viewer count skyrocketing past 1,000,000, hitting Rank 1 trending nationwide! "
            "+对话或独白: “感谢老铁的十个嘉年华！金鬃，给大家比个心！” "
            "+环境音: 狂轰滥炸的虚拟嘉年华礼物音效与热烈喝彩 "
            "Vibrant festive lighting, dynamic digital graphics, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 14,
        "filename": "ep02_shot14_sparrows_flabbergasted.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Hilarious wildlife shot: Perched on a nearby tree branch, the scruffy sparrow from Episode 1 and three baby sparrows sit in a row, beaks hanging completely open in disbelief, watching the terrifying lion act like a pet kitten. "
            "+对话或独白: “卧槽！狮子老大疯了！它居然在向人类撒娇卖萌？！” "
            "+环境音: 叽叽喳喳慌乱尖锐的麻雀叫声与振翅扑棱声 "
            "Photorealistic bird feathers, shallow depth of field, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 15,
        "filename": "ep02_shot15_heroine_sunset_smile.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Cinematic medium portrait: Warm golden sunset backlighting the young woman director's silhouette and black ponytail. She looks down at the substantial livestream donation earnings on her phone, smiling with renewed determination. "
            "+对话或独白: “一个月还清一千万？看来也不是不可能。” "
            "+环境音: 温暖的傍晚微风与远山林海涛声 "
            "Warm golden hour cinematography, filmic grade, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 16,
        "filename": "ep02_shot16_distant_police_sirens.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Dramatic wide establishing shot: Down the winding mountain road leading to the abandoned zoo, three police SUVs and wildlife emergency enforcement vans race up with flashing red and blue strobe lights piercing the dusk shadows. "
            "+声音效果: 尖锐凄厉由远及近破空而来的多重警笛警报蜂鸣声 "
            "Moody dusk lighting, motion blur of speeding emergency vehicles, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 17,
        "filename": "ep02_shot17_swat_surround_gate.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Low-angle dynamic action shot: Police vehicles screech to a halt outside the zoo gate. Armed wildlife enforcement officers and tranquilizer rifle handlers jump out swiftly, boots hitting gravel, forming an aggressive tactical perimeter. "
            "+环境音: 急刹车轮胎摩擦尖叫声与沉重战术靴踏地声 "
            "High adrenaline action cinematography, dust and headlights, 16:9 widescreen, 1080p."
        )
    },
    {
        "id": 18,
        "filename": "ep02_shot18_cliffhanger_freeze.mp4",
        "prompt": (
            "Generate a 16:9 widescreen cinematic video using Veo 3.1 - Lite: "
            "Climax cliffhanger medium close-up: A handsome, stern-faced 28-year-old detective in a black tactical windbreaker steps forward holding up a gold police badge, while behind the young female director, the giant lion Golden Mane leaps up protective with a fierce defensive snarl! Sudden freeze frame! "
            "+对话或独白: “我们接到紧急举报有人非法虐待野生猛兽！所有人不许动，举起手来！” "
            "+声音效果: 严厉呵斥声伴随猛兽威慑低吼与骤停悬念重音 "
            "Intense cinematic drama, dramatic split contrast lighting, 16:9 widescreen, 1080p."
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

def render_shot_with_retry(page, shot, account_mgr, browser):
    shot_id = shot["id"]
    filename = shot["filename"]
    prompt = shot["prompt"]
    out_path = RAW_OUTPUT_DIR / filename

    if out_path.exists() and out_path.stat().st_size > 500000:
        print(f"⏭ [Shot {shot_id}] 本地已就绪 ({out_path.stat().st_size / 1024 / 1024:.2f} MB)，跳过。")
        return True

    for attempt in range(1, 3):
        print(f"\n==================================================")
        print(f"🎬 [Shot {shot_id}/18] (第 {attempt} 次尝试) 开始在 Google Flow 中渲染: {filename}")
        print(f"==================================================")

        input_box = page.locator('.ProseMirror, [contenteditable="true"]').first
        if not input_box.is_visible():
            print(f"❌ 找不到输入框，尝试重新定位...")
            return False

        init_thumbs = page.locator('img.video-thumbnail').count()
        print(f"   当前画布缩略图基准数量: {init_thumbs}")

        input_box.click()
        time.sleep(0.5)
        input_box.fill(prompt)
        time.sleep(1.0)

        arrow_btn = page.locator('button:has(mat-icon:has-text("arrow_forward")), button.generate-icon-button')
        if arrow_btn.count() > 0 and arrow_btn.first.is_visible():
            arrow_btn.first.click()
            print("   ➤ 点击发送生成指令")
        else:
            input_box.press("Enter")
            print("   ➤ 按回车发送生成指令")
        time.sleep(3)

        # 检查点数耗尽
        body_text = page.locator("body").inner_text()
        exhausted, kw = check_credit_exhaustion(body_text)
        if exhausted:
            print(f"\n🚨🚨🚨【点数告警】：账号点数已耗尽 '{kw}'！正在尝试自动切换下一账号...")
            next_idx = account_mgr.switch_to_next_account()
            if next_idx is None:
                print("🚨【熔断暂停】：所有账号点数均已耗尽！立即停止任务并通知用户！")
                page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_credit_exhausted.png"))
                sys.exit(42)
            return False

        # 监控渲染完成
        print("   ➤ 正在等待 Google Flow (Veo 3.1 - Lite) 云端渲染完成...")
        rendered = False
        for sec in range(0, 180, 10):
            time.sleep(10)
            curr_thumbs = page.locator('img.video-thumbnail').count()
            stop_btn = page.locator('button:has(mat-icon:has-text("stop")), mat-icon:has-text("stop"), button:has-text("停止")')
            is_generating = stop_btn.count() > 0 and stop_btn.first.is_visible()

            # 检查是否渲染中抛出点数耗尽
            body_text = page.locator("body").inner_text()
            exhausted, kw = check_credit_exhaustion(body_text)
            if exhausted:
                print(f"\n🚨🚨🚨【点数告警】：渲染等待中检测到点数耗尽 '{kw}'！")
                sys.exit(42)

            if curr_thumbs > init_thumbs and not is_generating:
                print(f"   ✓ 视频已成功生成！(缩略图数从 {init_thumbs} 增至 {curr_thumbs}，耗时 ~{sec}s)")
                rendered = True
                break
            if sec % 30 == 0:
                print(f"      ... 云端处理中 ({sec}s elapsed, thumbs={curr_thumbs}, is_generating={is_generating})")

        if not rendered:
            curr_thumbs = page.locator('img.video-thumbnail').count()
            if curr_thumbs > init_thumbs:
                print(f"   ✓ 视频在超时前已生成成功 (thumbs={curr_thumbs})！")
                rendered = True

        if not rendered:
            print(f"   ⚠️ 第 {attempt} 次生成未能在 180s 内完成或遇到偶发失败，保存截图排查...")
            page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_attempt_{attempt}_status.png"))
            if attempt == 1:
                print("   🔄 准备进行第 2 次重试...")
                time.sleep(5)
                continue
            return False

        # 下载视频
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
            done_btn = page.locator('button:has-text("完成"), button:has-text("Done")').first
            if done_btn.count() > 0 and done_btn.is_visible():
                done_btn.click()
            time.sleep(2)
            return True
        else:
            print(f"   ❌ 未能找到下载按钮，保存截图排查。")
            page.screenshot(path=str(LOGS_DIR / f"shot_{shot_id}_no_dl.png"))
            return False

    return False

def main():
    print("🎬 [Episode 2] 启动第 2 集 Google Flow (Veo 3.1 - Lite) 工业化生产流水线...")
    account_mgr = FlowAccountManager()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            accept_downloads=True
        )

        cookies = account_mgr.get_playwright_cookies(0)
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        print("➤ 正在进入 Flow 项目画布...")
        page.goto("https://flow.google.com/", wait_until="domcontentloaded")
        time.sleep(4)

        proj_title = page.locator('text="10月 13 - 21:12"').first
        proj_title.scroll_into_view_if_needed()
        time.sleep(1)
        box = proj_title.bounding_box()
        page.mouse.click(box['x'] + 50, box['y'] - 50)
        time.sleep(6)

        # Check if Shot 2 is currently already finished on canvas
        # Earlier we submitted Shot 2 retry, let's see if thumbs increased to 19!
        curr_thumbs = page.locator('img.video-thumbnail').count()
        print(f"当前画布缩略图数: {curr_thumbs}")
        out_shot02 = RAW_OUTPUT_DIR / "ep02_shot02_heroine_push_gate.mp4"
        if not out_shot02.exists() and curr_thumbs >= 19:
            print("检测到 Shot 2 已经在云端生成完成，正在下载...")
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
                dl.save_as(str(out_shot02))
                print(f"🎉 Shot 2 下载完成: {out_shot02.name} ({out_shot02.stat().st_size / 1024 / 1024:.2f} MB)")
                done_btn = page.locator('button:has-text("完成"), button:has-text("Done")').first
                if done_btn.count() > 0 and done_btn.is_visible():
                    done_btn.click()
                time.sleep(2)

        for shot in EPISODE_02_SHOTS:
            success = render_shot_with_retry(page, shot, account_mgr, browser)
            if not success:
                print(f"⚠️ Shot {shot['id']} 未能顺利完成，检查状态并退出。")
                break

        print("\n==================================================")
        print("🎉 第 2 集分镜生成循环处理完成！")
        print("==================================================")
        browser.close()

if __name__ == "__main__":
    main()
