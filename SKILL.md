---
name: flow-manju-pipeline
description: >-
  google flow制作短剧完整流水线，喂小说就能出成片。支持小说剧本自动分镜、视觉一致性四视图故事板生成、
  Google Flow (Veo 3.1 - Lite) 自动化视频生成、官方时间轴【延续镜头】无缝顺承长场景渲染、
  100% 保留 Flow 原生音轨与人声台词毫秒级对齐（拒绝生硬 TTS 覆盖）、短剧经典粗黑边白字字幕与右侧合规声明压制，全流程一键出片并全球托管于 GitHub。
---

# Google Flow 制作短剧/漫剧完整流水线 (FLOW漫剧流水线)

本 Skill 封装了从**输入小说原文**到**输出超清电影级漫剧成片**的工业化全链路标准作业程序（SOP）。核心攻克了传统 AI 视频生产中“多镜头人物漂移”、“音频生硬假喉咙”、“散片剪接无连贯性”、“人声与字幕脱节”、“字幕无短剧质感”五大行业痛点。

---

## 🏗️ 核心架构与七大核心原则

1. **统一模型基准 (Unified Model Benchmark)**：全链路统一锁定 Google Flow **Veo 3.1 - Lite**，禁止多模型混用，保证底层画面质感、物理渲染与运镜风格统一。
2. **多视角故事板锚定 (Visual Anchor Board)**：视频生成前必须严格建立人物 4 视图（正/侧/背/特写）与场景 3 视角氛围板（全景/中景工位/微距特写），形成强一致性视觉约束基准。
3. **官方时间轴延续镜头 (Flow Timeline Extend Video)**：彻底摒弃在侧边栏独立生成多段散片的伪连贯方案。必须在 Flow 画布的时间轴编辑器中，通过片段末尾的 **`>> 延续镜头（Veo 3.1 - Lite）`** 进行顺承延展，生成真正时空连续的长场景。
4. **100% 原生音轨保真与人声对齐 (Flow Native Audio & Speech-Subtitle Sync)**：
   - 严禁剥离视频音轨并用粗糙 gTTS/伪配音覆盖！完整提取并保留 Google Flow 内部原生 48kHz 立体声音轨（包含真实空间低频电磁轰鸣、高频数码脉冲、微弱电流杂音与环境混响）。
   - 通过 ASR (Vosk / Whisper) 提取高精度单词时码，字幕内容必须与 Flow 视频中角色真实说出的台词字字一致，出现与消失时间毫秒级贴合角色发音。角色未说话或仅喘息的段落纯净留白，严禁伪造不存在的对白字幕。
5. **短剧标准字幕与合规声明 (Short-Drama Subtitling & Disclaimer)**：
   - **底部主台词字幕**：采用思源黑体 Extra Black / Heavy，纯白字身 + 8px 纯黑饱满外描边 + 微投射阴影，居中饱满呈现。
   - **右侧合规声明**：右侧边缘纵排单列「**故事纯属虚构  内容由AI生成**」，英文缩写“AI”采用纵中横水平排版。
6. **无损装配与流式秒开 (Lossless Assembly & Streaming Optimization)**：基于 FFmpeg CRF=18 电影级无损压制，加入 `-movflags +faststart` 保证在线秒开，同步生成 1080P MP4 成片与高保真预览动图 GIF。
7. **GitHub 官方托管交付 (GitHub-Hosted Delivery)**：成品严禁依赖临时或自建服务器！全量依托 GitHub 基础设施（GitHub Pages 交互播放器 + GitHub Releases 全球 CDN 下载 + 仓库直链嵌入），实现永久可用、全球高速交付。

---

## 🔄 全流程详细 SOP 步骤

### 第一步：小说改编与分镜时码规划 (Script Breakdown)

- **输入**：小说文本片段（如《三体》幽灵倒计时）。
- **处理**：
  1. 提炼核心戏剧冲突，按 12 秒黄金三幕结构划分时码：
     - **Shot 1 (00:00 - 00:02.1)**：伏案初见（建立镜头，慢推特写，悬念浮现）。
     - **Shot 2 (00:02.4 - 00:04.4)**：惊疑残影（绿光映照钛金镜片，神色骇然困惑）。
     - **Shot 3 (00:04.7 - 00:06.6)**：惊骇跳动（数字跳动加速，失声惊呼，倒吸冷气）。
     - **Shot 4 (00:07.0 - 00:12.0)**：视网膜烙印（高潮爆发，摘镜抱头闭眼，数字在漆黑深处永恒燃烧）。
  2. 提取固定角色特征约束（例如：38岁消瘦学者汪淼、黑发微卷、钛合金眼镜、深灰高领衫配微皱白大褂）。
  3. 提取固定场景特征约束（例如：昏暗国家纳米物理实验室、机柜冷光、控制台屏幕波形图、翠绿色数码管倒计时）。

### 第二步：视觉一致性基准故事板生成 (Storyboard Anchor)

在进入视频生成前，先由文生图引擎渲染生成 16:9 多宫格故事板：
1. **人物 4 视图转面图**：[正面] [侧面] [背面] [半身特写]。
2. **场景 3 视角氛围板**：[全景视角] [中景操作台] [细节微距视角]。
3. **分镜关键帧画面**：Shot 1、Shot 2、Shot 3 核心参考图。
4. 人工确认故事板无误后，将其作为 Google Flow 提示词中场景与人物的视觉基准。

### 第三步：Google Flow 设置锁定与 Shot 1 基准生成

1. **设置锁定**：
   - 通过 Playwright 自动化登录并打开 Flow 项目。
   - 打开智能体设置面板 (`flow-agent-settings-panel`)。
   - 将视频生成模型统一选择为 **`Veo 3.1 - Lite`** 并点击保存生效。
2. **Shot 1 视频渲染**：
   - 注入包含完整角色外貌、实验室环境与准确台词的提示词（如 `+对话或独白: “这……这是什么？实验仪器的残影？……不对，它在跳动……”`）。
   - 提交生成初始基准视频。

### 第四步：时间轴【延续镜头 (Veo 3.1 - Lite)】延展长场景

1. **打开时间轴**：在 Flow 画布上点击已生成的 Shot 1 场景卡片，进入底部多轨时间轴编辑器。
2. **触发延续菜单**：
   - 定位并点击时间轴末尾的添加按钮 `[aria-label="添加片段"], mat-icon:has-text("add_2")`。
   - 在弹出菜单中选择 **`keyboard_double_arrow_right 延续镜头（Veo 3.1 - Lite）`**。
3. **输入顺承提示词**：
   - 聚焦底部 `flow-edit-video-prompt-box .ProseMirror` 输入框。
   - 填入动作顺承提示词（例如汪淼惊恐探身，倒计时漂浮逼近，紧闭双眼，倒计时烙印在视网膜上）。
4. **DOM 级原生提交（避坑指南）**：
   > [!IMPORTANT]
   > 绝不能使用 Playwright 普通的 `button.click()`，会被 Angular Material 的 Tooltip 浮层拦截提示“必须提供提示”！
   > 必须使用 JavaScript 原生事件：`gen_btn.evaluate('b => b.click()')` 绕过拦截，即可成功触发后端 `Creating scene...`。
5. **导出完整连贯长视频**：
   - 等待 Veo 3.1 - Lite 延续渲染完成，画布上卡片角标增加至 2（形成 15s+ 多轨合体长视频）。
   - 在场景预览界面右上角点击下载按钮，监听并保存包含完整前后镜头的 `flow_scene_complete.mp4`。

### 第五步：100% 原生音轨提取与 ASR 毫秒级人声对齐

> [!CAUTION]
> 绝对不要粗暴剥离或覆盖 Flow 原生音轨！
> 剪辑起点必须从 `00:00:00.000` 开始，严禁误裁开首人声导致全片声画脱节。

1. **音频提取与语音对齐 (Vosk ASR)**：
   - 提取 16kHz WAV 单声道音频。
   - 运行 Vosk / Whisper 获取每个字的起始与结束时间戳（Start -> End）。
   - 核验台词文本与视频角色说话口型与发音完全吻合。
2. **音频微淡入淡出**：
   - `-af "afade=t=in:ss=0:d=0.05,afade=t=out:st=11.8:d=0.2"` 消除剪辑接缝杂音。

### 第六步：标准短剧字幕与右侧合规声明压制

1. **设计标准**：
   - **底部台词字幕**：思源黑体 Extra Black / Heavy，62px，`#FFFFFF` 纯白填充，8px 纯黑饱满描边，底部边距 95px，居中。
   - **右侧合规声明**：思源黑体 Extra Black / Heavy，28px，纵排单列：
     `故\N事\N纯\N属\N虚\N构\N \N内\N容\N由\NAI\N生\N成`
     英文“AI”水平并排，纵中横居中嵌入，右边缘边距 60px。
2. **压制命令 (FFmpeg + libass + faststart)**：
   ```bash
   ffmpeg -y -ss 00:00:00.000 -t 12.000 -i flow_scene_complete.mp4 \
     -vf "scale=1920:1080:flags=lanczos,ass=three_body_perfect_align.ass" \
     -af "afade=t=in:ss=0:d=0.05,afade=t=out:st=11.8:d=0.2" \
     -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart \
     -c:a aac -b:a 320k three_body_12s_final.mp4
   ```

### 第七步：GitHub 官方托管交付与质检

1. 抽取 4 张关键时码高保真抽帧（01.0s, 03.2s, 05.5s, 11.0s）进行声画一致实质检。
2. 压制 12s 高清动图预览 GIF（640x360, 10fps, 双通道调色板优化）。
3. 部署资产至 `docs/` 目录并配置 GitHub Pages：
   `gh api -X POST repos/<user>/<repo>/pages -F "source[branch]=main" -F "source[path]=/docs"`
4. 发布 GitHub Release (如 `v1.0.0`) 附带超清视频成品与动图。

---

## 🛠️ 自动化工具与执行脚本清单

- `src/flow_adapter.py`: Playwright 自动化调度 Google Flow（登录、切模型、生成首镜、延续镜头、监听导出）。
- `src/storyboard_renderer.py`: 多宫格人物四视图与场景板图像生成与拼合。
- `src/subtitle_generator.py`: 生成经典粗黑边白字 + 右侧竖排“故事纯属虚构 内容由AI生成”的 ASS 与图像层。
- `src/video_assembler.py`: 黄金 12 秒精剪、原生音频保真混录、超清压制与动图生成。
- `docs/index.html`: GitHub Pages 官方在线影院播放器。

---

## 💡 常见故障排查 (Troubleshooting)

1. **人声与字幕对不上 / 说话内容不一样**：
   - 核心原因：剪辑截取时间偏离（如使用 `-ss 00:00:02.000` 裁掉了起首台词），或使用了假台词文本。
   - 解决方案：严禁裁切开头，使用 Vosk/Whisper 实测音频波形与发音时码，精确对齐每一句实际台词。
2. **Flow 提交按钮点击无效 / 弹出 Tooltip 拦截**：
   - 解决方案：切勿使用 Playwright 坐标模拟点击，改用 DOM evaluate 点击：`btn.evaluate('b => b.click()')`。
3. **字幕字体偏细或描边有锯齿**：
   - 解决方案：必须安装 `fonts-noto-cjk-extra` 并指定 `Noto Sans CJK SC Black`，描边宽度设为 7-8px。
4. **生成的视频人物前后不连贯**：
   - 解决方案：检查是否在时间轴末尾点击了 `延续镜头（Veo 3.1 - Lite）`。延续镜头生成的视频会在原视频轨道向后延伸，并在卡片上显示切片数量角标（如 `2`）。

---

## 💬 创作者交流与联系 (Contact & Community)

- **作者**：Gabor Lu
- **微信**：见项目主页二维码 (`assets/wechat_qrcode.png`)
- **Telegram**：[@GABORLU](https://t.me/GABORLU)
- **在线影院**：[GitHub Pages 官方影院](https://avisii1680769-cell.github.io/google-flow-manju-pipeline/)
- **开源仓库**：[google-flow-manju-pipeline](https://github.com/avisii1680769-cell/google-flow-manju-pipeline)

