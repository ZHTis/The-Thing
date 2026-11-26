---
name: drawing-svg-analysis-workflow
description: Draw analysis workflows that distinguish evidence paths, exploratory branches, and forbidden result
  feedback.
compatibility: Native SVG authoring and an SVG-capable renderer; source analysis workflow required.
metadata:
  the-thing.category: drawing-modeling
---
# SVG 分析工作流

- 用途：整理多阶段数据分析时，区分主证据链、补充探索、方法反馈和不得由结果改变的上游决策。
- 实现：原生 SVG；主流程用实线，补充分支用橙色虚线，禁止的结果倒灌用红色虚线；配图例，颜色只表达流程语义。
- 内容规则：每个特征/模型分支标出窗口、特征集合、训练测试边界；结果反馈仅连到候选、模型或下一轮特征设计，不连回 QC、对齐、切片或基线。
- 检查：使用系统中文字体回退；用 SVG 原尺寸查看流程可从左至右读通，避免把不同窗口或数据版本无标记合并。
- 双语导出：保持同一 SVG 几何结构，只替换展示层 `text` 节点输出 `*_en.svg`；英文文本更长时应压缩文案、独立调小字体并以全尺寸 PNG 复查，不能只做直译替换。导出后检查英文版没有残留 CJK 字符。
- 已验证案例：[本机案例 1](references/local-cases.md#case-1)。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
