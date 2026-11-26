---
name: drawing-xlsx-spatial-preview
description: 将按精确坐标绘制的空间候选 PNG 嵌入 Excel，并附可筛选坐标和公式边界。
---
# XLSX 空间候选预览

- 依表格技能使用 artifact-tool：一个预览页、一个平面坐标表。矩形的左/右/上/下边界用简单单元格公式，保留中心坐标、尺寸和候选 ID。
- PNG 用 images.add(dataUrl, anchor) 嵌入，按像素宽高预留连续空白行；图是静态快照，明确改坐标不会自动更新。
- 固定坐标轴，长空间同时给全景与局部放大。保留生成种子和来源；不要将随机布局声称为已验证的同难度方案。
- 完成后重算、检查错误、渲染两页，最后检查 XLSX 包中图像数量与公式错误类型。加宽长随机种子列，避免数字挤在相邻列。
- 已验证例：/Users/heting/Documents/grip_psychopy/data_viewer/exports/outputs/grip-map-candidates-20261102/build.mjs。导出结构和渲染已验证，未据此宣称原生 Excel 应用交互已测试。
