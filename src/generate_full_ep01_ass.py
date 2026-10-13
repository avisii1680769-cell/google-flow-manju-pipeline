#!/usr/bin/env python3
"""
generate_full_ep01_ass.py
Generates the complete 18-shot short-drama ASS subtitle file for Episode 1 (total duration: ~136.8s).
Follows:
- 16:9 1920x1080 resolution
- Extra Black bold white text with 9px pure black outline
- Right side vertical disclaimer: 故事纯属虚构 内容由AI生成
- MarginV=83 to cover any native watermark artifact
"""

from pathlib import Path

ASS_PATH = Path("/root/.agy-avisii/.gemini/production/ep01_full_flow.ass")

ass_content = """[Script Info]
Title: Zoo Pet Ep01 Full Flow Master (18 Shots, ~136.8s)
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BottomSub,Noto Sans CJK SC,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,9,3,2,60,60,83,1
Style: RightDisclaimer,Noto Sans CJK SC,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,9,60,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 1,0:00:00.00,0:02:30.00,RightDisclaimer,,0,0,0,,{\\pos(1856,238)}故\\N事\\N纯\\N属\\N虚\\N构\\N \\N内\\N容\\N由\\NAI\\N生\\N成
Dialogue: 0,0:00:00.00,0:00:02.80,BottomSub,,0,0,0,,卧槽！两脚兽成精了！她真能听懂我骂她？！
Dialogue: 0,0:00:02.80,0:00:08.80,BottomSub,,0,0,0,,小家伙，你刚才在叫唤什么？再废话拿你烤了抵债。
Dialogue: 0,0:00:08.80,0:00:16.80,BottomSub,,0,0,0,,【奇迹动物园】……这就是老头子留给我的全部遗产？
Dialogue: 0,0:00:16.80,0:00:24.80,BottomSub,,0,0,0,,连本带息整整一千万！一个月不还，连人带动物园全被法拍！
Dialogue: 0,0:00:24.80,0:00:32.80,BottomSub,,0,0,0,,小姑娘，拿不出钱，明天就派挖掘机来推平这里！
Dialogue: 0,0:00:32.80,0:00:40.80,BottomSub,,0,0,0,,合同期还有三十天。三十天后，一千万我一分不少给你。现在，滚。
Dialogue: 0,0:00:40.80,0:00:48.80,BottomSub,,0,0,0,,好！有种！一个月后老子亲自带人来收尸！走！
Dialogue: 0,0:00:48.80,0:00:56.80,BottomSub,,0,0,0,,【奇迹动物园救赎系统】绑定成功！已解锁万兽通识语感！
Dialogue: 0,0:00:56.80,0:01:04.80,BottomSub,,0,0,0,,【系统提示】检测到园区极度濒危濒死级神兽，好感度提升将获得十倍资金返利！
Dialogue: 0,0:01:04.80,0:01:12.80,BottomSub,,0,0,0,,等等……这是什么声音？我能听见它们的心声？！
Dialogue: 0,0:01:12.80,0:01:20.80,BottomSub,,0,0,0,,【秃毛孔雀】看什么看！没见过掉毛的美男子吗？老子三天没吃纯牛肉了！
Dialogue: 0,0:01:20.80,0:01:28.80,BottomSub,,0,0,0,,【小浣熊】呜呜……这半块饼干是本干脆面的，谁也别想抢走！
Dialogue: 0,0:01:28.80,0:01:36.80,BottomSub,,0,0,0,,【金丝小猴】两脚兽快跑啊！猛兽区那头金毛大猫要疯了！它要冲破牢笼了！
Dialogue: 0,0:01:36.80,0:01:44.80,BottomSub,,0,0,0,,猛兽区？难道是那头快要狂暴安乐死的百兽之王……？！
Dialogue: 0,0:01:44.80,0:01:52.80,BottomSub,,0,0,0,,【警报蜂鸣】红灯急促爆闪！特级禁区重型防暴闸门即将崩溃！
Dialogue: 0,0:01:52.80,0:02:00.80,BottomSub,,0,0,0,,轰隆——！重型铁链崩断！整座地下兽舍剧烈震颤！
Dialogue: 0,0:02:00.80,0:02:08.80,BottomSub,,0,0,0,,姜瑾一把推开防暴门！迷雾中一对凶残血红的兽瞳骤然睁开！
Dialogue: 0,0:02:08.80,0:02:16.80,BottomSub,,0,0,0,,【狂暴金鬃雄狮】吼——！！两脚兽全都该死！滚出我的领地——！！
"""

ASS_PATH.write_text(ass_content, encoding="utf-8")
print(f"Generated full ASS subtitles at {ASS_PATH}")
