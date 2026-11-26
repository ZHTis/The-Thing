---
name: drawing-png-gesture-preview
description: 用参考手势图生成统一风格的透明或白底 PNG 手势候选图，供 PsychoPy cue 审核。
compatibility: Image-generation capability with reference images; macOS sips only for the documented crop example.
metadata:
  the-thing.category: drawing-modeling
---
# 手势 PNG 预览

用途：为 PsychoPy 的手势 cue 生成候选预览，不直接替换已验证的实验素材。

工具：内置 image generation，输入一张项目现有手势 PNG 作为风格参考；要求“单手、居中、腕部可见、蓝色线框网格、透明背景、无文字”。每个不同姿势单独生成。

检查：先目视确认手指数、姿势、裁切和透明底；尤其检查边缘是否出现青色光晕／散点。出现伪影的预览仅用于选型，选中后再清理并统一尺寸后才可写入 `assets/gesture_library/`。

已验证案例：`assets/gesture_library/06_open_hand.png` 作为参考，生成拇指上举、食指指向、V 手势、拇食指捏合的候选预览（2026-11-06）。

## 多姿势参考表拆图

若参考图是字母／数字手势拼版，先用 `sips -c 高 宽 --cropOffset 上 左 原图 --out 单姿势参考.jpg` 分别裁出每个手形，再逐张交给 image generation；同一提示写明蓝色网格、白底、单手、无文字，避免拼版邻格和标签混入。生成后用等比缩略总览检查手指数、指尖接触、方向与重复姿势；尺寸可不同，但不可把未经检查的图标成正式 cue。2026-11-14 的 36 张字母数字候选图按此法生成，总览见 `assets/gesture_library/asl_contact_sheet_preview.png`；细微手指关系仍待人工核验。

## PPT 手势总览

用途：将透明手势 PNG 做成可直接插入幻灯片的素材总览，不改动源图。用 Swift AppKit 绘制 16:9 画布、等宽卡片与标题；手势图等比缩放居中，标注名称，并用不同颜色区分现有素材与候选预览。底部注明候选状态，避免误作已启用任务条件。

检查：目视确认所有图像完整、卡片及标签无裁切；候选状态与素材说明一致。已验证 1920×1080 输出案例：[本机案例 1](references/local-cases.md#case-1)（2026-11-06）。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
