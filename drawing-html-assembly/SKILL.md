---
name: drawing-html-assembly
description: 用内嵌 SVG 的 HTML 绘制机械连接原理剖面，切换分解与装配状态；适用于说明连接关系，不用于加工图或精确 CAD。
---
# HTML 装配剖面

- 用容器实际宽度计算 SVG 坐标；将固定件坐标与移动件位移分开，按钮只改变盖子和螺钉位置。
- 剖面明确画出孔的空白、螺母实体及螺丝柱，避免把轴线或透视重叠误画成材料；剖面仅解释连接顺序，未设计尺寸标为不按比例。
- 可用 Node 的最小 DOM/ResizeObserver 替身执行内嵌脚本，在 320/736 px 调用两种状态处理器，检查生成坐标没有 NaN/undefined。此法已验证脚本与状态切换，不代替浏览器视觉检查。
- 案例代码：[盖盒螺钉连接](/Users/heting/.codex/visualizations/2026/10/12/01a12f6e-019d-7d30-85a2-293058f0498b/box-lid-screw.html)。本例是通用原理示意，无厂家尺寸依据。
