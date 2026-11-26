---
name: drawing-svg-cognitive-map
description: 从范式对照表制作一张适合汇报的认知类型—研究问题—任务总览图。
compatibility: Native SVG authoring and an SVG-capable renderer; source paradigm comparison table.
metadata:
  the-thing.category: drawing-modeling
---
# 范式对照总览图

- 用结构化列表保存分类、研究问题、任务 ID 和实现边界；从同一份数据生成 SVG 与 PNG，避免两版内容不一致。
- 16:9 画布按分类分列；每个问题独占一行，较长 ID 使用两行并动态增加行高。中文排版在 SVG 使用独立 `text`，PNG 使用 Pillow 和可用的中文字体。
- Pillow 文本若按 SVG 的基线坐标绘制，锚点用 `ls`／`rs`；`la` 是上缘锚点，会使标题和行说明重叠。
- 导出后检查文字宽度，再目视检查 PNG 的分类标题、双行 ID、状态说明和底边是否重叠；保留 SVG 供修改。
- 当研究问题与任务代码不逐项对应时，在分类卡片内并排放两个独立列表，分别加标题和“不逐项对应”说明；SVG 与 PNG 复用同一列表，并检查两栏各自的文字宽度。
- 已验证案例及源码：[本机案例 1](references/local-cases.md#case-1)，输出同目录的 `stage-report-cognitive-map.svg` 与 `.png`。图中状态和日期来自对应阶段报告，不作为通用固定参数。

- 全量改写保留每题原文/新文及每类任务/边界，按计数和SVG实际文本校验覆盖；任务独立置底或右栏以免暗示一题一任务。列表换行按完整任务名而非逐字符；SVG和PNG共享宽度测量。对比布局案例render_cognitive_map_variants.py，7类34题，原图保留。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
