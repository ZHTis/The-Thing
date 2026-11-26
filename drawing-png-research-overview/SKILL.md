---
name: drawing-png-research-overview
description: 用 Pillow 绘制适合 PPT 的“文献任务—研究问题”清单图，任务代码另列，避免暗示逐项对应。
compatibility: Python with Pillow and a CJK-capable font; factual source table required.
metadata:
  the-thing.category: drawing-modeling
---
# 文献问题与任务代码总览图

- 用结构化行分别保存文献任务、研究方向、具体问题和已核实的原文假设；没有明确假设的行留空，不把结果倒写成预测。
- 用 Pillow 在 3200×1800 像素画布绘制左侧问题行和右侧独立代码清单；可传入同尺寸模板背景。像素尺寸是输出画布设置，不代表物理显示尺寸。
- 每行按内容决定高度，绘制前用 `textlength` 检查左右栏宽度，导出后缩到 1280×720 目视检查可读性及底部遮挡。
- 已验证源码：[render_motor_questions.py](references/local-cases.md#case-1)；输出：[stage-report-motor-questions.png](references/local-cases.md#case-1)；内容来源：[运动解码调研](references/local-cases.md#case-1)。文献依据与具体任务属于项目内容，不写成通用绘图规则。


## 分类词表卡片

- 用原始词序清单与分类词清单双向核对集合及总数，防止遗漏、重复或无意改词；分类来源与原始材料来源分开声明。
- Pillow 按完整词项测量 textlength 后换行，保留词内字符连续；每卡显示类别及真实项数，验证最后一行底边不越界。面积仅作排版，不声称数量比例。
- 已验证案例：[本机案例 2](references/local-cases.md#case-2)；61项、8类、3200×1800 PNG，已目视检查。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
