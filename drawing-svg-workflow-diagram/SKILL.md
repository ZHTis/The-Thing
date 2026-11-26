---
name: drawing-svg-workflow-diagram
description: 用原生 SVG 绘制适合报告或幻灯片的横向工作流图，尤其适用于需要突出人工审核、退回重算和人在环路的流程。
---

# SVG 人在环路工作流图

## 画法

- 用显式 `viewBox`、`width`、`height` 固定画布；宽屏半页图可采用约 2.46:1。已验证示例为 `1600 × 650 px`。
- 主计算流程放在上方，用等宽卡片和单向箭头；人工审核单独放在下方，用不同分类色和虚线回路连接到需返工的步骤。
- 用原生 SVG `marker-end` 定义箭头，避免字符箭头在导入 PowerPoint 后错位。
- 中文使用系统字体回退栈；在 1600 px 宽画布上，正文不小于 14 px、步骤标题约 23 px、总标题约 34 px。
- 颜色只表示流程类别时必须写图例，不要让分类颜色看起来像连续数值色标。
- 对失败分支写明返回位置，例如“配准未通过 → 返回重新配准”，体现人在环路而不是只画人工确认框。
- 面向通用展示时，标题、正文和交付文件名都使用中性术语，避免在可复用图中保留机构、数据来源或病例特有名称。

## 检查

- 用 `sharp` 将 SVG 渲染成 PNG，再以原始尺寸检查中文、裁切、箭头方向、文字与连线是否重叠。
- 导出前确认主流程可从左到右独立读懂，人工回路可从下方反向追踪。
- 保留 SVG 作为交付文件；PNG 仅作视觉检查或兼容性预览。

## 已验证案例

- `/Users/heting/Documents/readGripData/analysis_outputs/results/electrode_localization_workflow/electrode_localization_workflow.svg`
- 内容采用五步主流程、四个人工检查点及一条退回重配准的虚线闭环；不使用脑影像也能表达数据、计算、审核与交付关系。

## 任务逻辑图补充（2026-10-30）

- 对同一来源的一组任务图，用 Python 的结构化步骤表生成各 SVG，避免多张图的卡片尺寸、配色和箭头样式漂移；同时输出总览图与单任务图。
- 生成后用 `xml.etree.ElementTree` 逐一解析 SVG；在本机用 `sips -s format png source.svg --out preview.png` 保留宽屏原始比例后目视检查。`qlmanage -t` 会生成正方形缩略图并裁切宽图，不用于布局判断。
- macOS `sips` 预览中 `marker-end` 可能不显示；对需要稳定可见的箭头，在 SVG 内追加三角形 `path` 箭头头部，而非用 Unicode 箭头字符。
- macOS `sips` 对同一 `<text>` 内多个 `<tspan>` 的换行定位可能重叠；需要可靠多行正文时，为每一行生成独立 `<text x="…" y="…">` 元素，再用 `sips` 检查。
- 已验证案例：`/Users/heting/Documents/paradigm/paradigm-atlas/mengcode-workflows/render_workflows.py`。

## 定时任务流程图补充（2026-11-04）

- 对包含 `→` 的阶段串，换行器除按箭头分组外，还必须再次切分单个超长末尾子句；否则中文时长说明会越过固定宽度的 SVG 卡片。生成后用 `sips` 渲染 PNG 目视确认。
- 已验证案例：`/Users/heting/Documents/paradigm/experiments/flow_contract/render_flows.py` 生成的 `generated/t03_flow.svg`。

## 默认实验时间轴补充（2026-11-06）

- 对同一批默认 demo，时间轴图和同步／保存契约图应分开生成：前者只呈现被试可见阶段、时长、重复次数、行为要求与数据边界，避免把后端实现细节挤进实验流程。
- 固定画布 `1600 × 760 px`；用等高圆角阶段块放在水平时间轴上。阶段时长适合比较时按比例分配宽度；含大量重复 trial 时保留一个完整 trial 加虚线“下一 trial × N”，比压缩几十个小块更可读。
- 用 `xml.etree.ElementTree` 解析生成结果，再以 `sips -s format png` 渲染原尺寸 PNG 逐张检查；正文区域须给 marker 名称和 JSON 文件名预留足够宽度，避免在 `screen_flip`、`events.jsonl` 等标识符中间换行。
- 已验证案例：`/Users/heting/Documents/paradigm/experiments/flow_contract/render_default_demo_timelines.py`。

## PPT 纯时间轴补充（2026-11-06）

- 当用户只要可粘贴 PPT 的流程图片时，使用 `1920 × 1080` 的 16:9 SVG/PNG，移除任务标题、图例、说明和边界框，仅保留阶段块、块内名称／时长与水平箭头；留出上下面白，便于与幻灯片其他元素组合。
- 已验证案例：`/Users/heting/Documents/paradigm/experiments/flow_contract/render_m05_ppt_timeline.py`，用 `sips` 导出并确认 PNG 为 `1920 × 1080`。

## 多任务 PPT 总览补充（2026-11-06）

- 在一张 16:9 图中汇总多个实验时间轴时，每个任务占一行，只保留左侧任务 ID、阶段块、时长、重复虚线块和右向箭头；不要加总标题、图例或行为／数据说明。阶段块的宽度可按时长比例绘制，重复 trial 用虚线续段避免压缩所有重复块。
- 已验证案例：`/Users/heting/Documents/paradigm/experiments/flow_contract/render_default_demo_ppt_overview.py`，输出 `1920 × 1080` SVG/PNG，并逐张原尺寸检查。

## macOS宽屏预览补充（2026-11-17）
- SVG可用Swift AppKit的`NSImage(contentsOfFile:)`载入，再画入指定宽高的`NSBitmapImageRep`并导出PNG，避免Quick Look方形缩略图裁切。中文显示已目视验证。
- 沙箱中Swift缓存目录不可写时，使用`swift -module-cache-path /tmp/任务缓存 ...`。
- 已验证代码：`/Users/heting/Documents/ChatGPT/范式是假设的验证/output/slide-01/render_svg.swift`（1600×900预览；画布像素尺寸，不表示实物尺寸）。
