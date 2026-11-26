---
name: drawing-svg-analysis-workflow
description: Draw analysis workflows that distinguish evidence paths, exploratory branches, and forbidden result feedback.
---

# SVG 分析工作流

- 用途：整理多阶段数据分析时，区分主证据链、补充探索、方法反馈和不得由结果改变的上游决策。
- 实现：原生 SVG；主流程用实线，补充分支用橙色虚线，禁止的结果倒灌用红色虚线；配图例，颜色只表达流程语义。
- 内容规则：每个特征/模型分支标出窗口、特征集合、训练测试边界；结果反馈仅连到候选、模型或下一轮特征设计，不连回 QC、对齐、切片或基线。
- 检查：使用系统中文字体回退；用 SVG 原尺寸查看流程可从左至右读通，避免把不同窗口或数据版本无标记合并。
- 双语导出：保持同一 SVG 几何结构，只替换展示层 `text` 节点输出 `*_en.svg`；英文文本更长时应压缩文案、独立调小字体并以全尺寸 PNG 复查，不能只做直译替换。导出后检查英文版没有残留 CJK 字符。
- 已验证案例：`/Users/heting/Documents/readGripData/analysis_outputs/results/analysis_workflow/seeg_force_analysis_workflow_detailed.svg`。
