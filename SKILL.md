---
name: flow-manju-pipeline
description: >-
  google flow制作短剧完整流水线，喂小说就能出成片。支持小说剧本自动分镜、视觉一致性四视图故事板生成、
  Google Flow (Veo 3.1 - Lite) 自动化视频生成、官方时间轴【延续镜头】无缝顺承长场景渲染、
  100% 保留 Flow 原生音轨（拒绝生硬 TTS 覆盖）、短剧经典粗黑边白字字幕与右侧合规声明压制，全流程一键出片。
---

# Google Flow 制作短剧/漫剧完整流水线 (FLOW漫剧流水线)

本 Skill 封装了从**输入小说原文**到**输出超清电影级漫剧成片**的工业化全链路标准作业程序（SOP）。核心攻克了传统 AI 视频生产中“多镜头人物漂移”、“音频生硬假喉咙”、“散片剪接无连贯性”、“字幕无短剧质感”四大行业痛点。

---

## 🏗️ 核心架构与六大核心原则

1. **统一模型基准 (Unified Model Benchmark)**：全链路统一锁定 Google Flow **Veo 3.1 - Lite**，禁止多模型混用，保证底层画面质感、物理渲染与运镜风格统一。
2. **多视角故事板锚定 (Visual Anchor Board)**：视频生成前必须严格建立人物 4 视图（正/侧/背/特写）与场景 3 视角氛围板（全景/中景工位/微距特写），形成强一致性视觉约束基准。
3. **官方时间轴延续镜头 (Flow Timeline Extend Video)**：彻底摒弃在侧边栏独立生成多段散片的伪连贯方案。必须在 Flow 画布的时间轴编辑器中，通过片段末尾的 **`>> 延续镜头（Veo 3.1 - Lite）`** 进行顺承延展，生成真正时空连续的长场景。
4. **100% 原生音轨保护 (Flow Native Audio Preservation)**：严禁剥离视频音轨并用粗糙 gTTS/伪配音覆盖！必须完整提取并保留 Google Flow 内部原生 48kHz 立体声音轨（包含真实空间低频电磁轰鸣、高频数码脉冲、微弱电流杂音与环境混响）。
5. **短剧标准字幕与合规声明 (Short-Drama Subtitling & Disclaimer)**：
   - **底部主台词字幕**：采用思源黑体 Extra Black / Heavy，纯白字身 + 7px 纯黑饱满外描边 + 微投射阴影，居中饱满呈现。
   - **右侧合规声明**：右侧边缘纵排单列「**故事纯属虚构  内容由AI生成**」，英文缩写“AI”采用纵中横水平排版。
6. **无损装配与多渠道交付 (Lossless Assembly & Deployment)**：基于 FFmpeg CRF=17 电影级无损压制，同步生成 1080P MP4 成片、动图 GIF 预览，并自动部署至在线 HTML5 影院。

---

## 🔄 全流程详细 SOP 步骤

### 第一步：小说改编与分镜时码规划 (Script Breakdown)

- **输入**：小说文本片段（如《三体》幽灵倒计时）。
- **处理**：
  1. 提炼核心戏剧冲突，按 12 秒黄金三幕结构划分时码：
     - **Shot 1 (00:00 - 00:04)**：伏案初见（建立镜头，慢推特写，悬念浮现）。
     - **Shot 2 (00:04 - 00:08)**：凝视逼近（动作顺承，微距特写，惊恐探身）。
     - **Shot 3 (00:08 - 00:12)**：视网膜烙印（高潮爆发，抱头闭眼，漆黑中永恒燃烧）。
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
   - 注入包含完整角色外貌与实验室环境的英文核心提示词。
   - 提交生成初始 8 秒基准视频卡片。

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

### 第五步：100% 原生音轨提取与保护

> [!CAUTION]
> 绝对不要剥离 Flow 视频的伴音！
> Google Flow 生成的视频自带 **48000 Hz, stereo, 128 kb/s AAC 原生音轨**（实测平均音量 -15.7 dB），包含深沉的物理环境电磁轰鸣与高压脉冲音。任何第三方 TTS 覆盖都会破坏这种真实的沉浸感。

- 使用 FFmpeg 精准截取时间区间时，务必保留音频轨道 `-c:a aac -b:a 320k`，仅添加极短的 0.2s 平滑淡入淡出 (`afade=t=in:ss=0:d=0.2,afade=t=out:st=11.7:d=0.3`) 消除剪辑断点爆音。

### 第六步：标准短剧字幕与右侧合规声明压制

1. **设计标准**：
   - **底部台词字幕**：思源黑体 Extra Black / Heavy，60px，`#FFFFFF` 纯白填充，7px 纯黑饱满描边，底部边距 110px，居中。
   - **右侧合规声明**：思源黑体 Extra Black / Heavy，30px，纵排单列：
     `故\N事\N纯\N属\N虚\N构\N \N内\N容\N由\NAI\N生\N成`
     英文“AI”水平并排，纵中横居中嵌入，右边缘边距 64px。
2. **压制命令 (FFmpeg + libass)**：
   ```bash
   ffmpeg -y -ss 00:00:02.000 -t 12.000 -i flow_scene_16s_complete.mp4 \
     -vf "scale=1920:1080:flags=lanczos,ass=three_body_douyin_style.ass" \
     -af "afade=t=in:ss=0:d=0.2,afade=t=out:st=11.7:d=0.3" \
     -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
     -c:a aac -b:a 320k output_12s_final.mp4
   ```

### 第七步：一键在线影院交付与质检

1. 自动提取 2s, 6s, 10s 抽帧图片供视觉质检。
2. 输出 12s 预览 GIF 动图。
3. 部署至 Web 服务器，提供在线交互播放器（支持镜头秒级跳转、原片下载、动图预览、故事板对照）。

---

## 🛠️ 自动化工具与执行脚本清单

- `src/flow_adapter.py`: Playwright 自动化调度 Google Flow（登录、切模型、生成首镜、延续镜头、监听导出）。
- `src/storyboard_renderer.py`: 多宫格人物四视图与场景板图像生成与拼合。
- `src/subtitle_generator.py`: 生成经典粗黑边白字 + 右侧竖排“故事纯属虚构 内容由AI生成”的 ASS 与图像层。
- `src/video_assembler.py`: 黄金 12 秒精剪、原生音频保真混录、超清压制与动图生成。
- `web_player/index.html`: 开箱即用的暗黑风格漫剧在线影院模版。

---

## 💡 常见故障排查 (Troubleshooting)

1. **Flow 提交按钮点击无效 / 弹出 Tooltip 拦截**：
   - 解决方案：切勿使用 Playwright 坐标模拟点击，改用 DOM evaluate 点击：`btn.evaluate('b => b.click()')`。
2. **字幕字体偏细或描边有锯齿**：
   - 解决方案：必须安装 `fonts-noto-cjk-extra` 并指定 `Noto Sans CJK SC Black`，描边宽度设为 6-7px。
3. **生成的视频人物前后不连贯**：
   - 解决方案：检查是否在时间轴末尾点击了 `延续镜头（Veo 3.1 - Lite）`。延续镜头生成的视频会在原视频轨道向后延伸，并在卡片上显示切片数量角标（如 `2`）。
