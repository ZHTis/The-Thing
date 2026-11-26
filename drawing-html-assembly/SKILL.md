---
name: drawing-html-assembly
description: 用内嵌 SVG 的 HTML 绘制机械连接原理剖面，切换分解与装配状态；适用于说明连接关系，不用于加工图或精确 CAD。
compatibility: HTML/SVG-capable browser; JavaScript runtime for optional logic checks.
metadata:
  the-thing.category: drawing-modeling
---
# HTML 装配剖面

- 用容器实际宽度计算 SVG 坐标；将固定件坐标与移动件位移分开，按钮只改变盖子和螺钉位置。
- 剖面明确画出孔的空白、螺母实体及螺丝柱，避免把轴线或透视重叠误画成材料；剖面仅解释连接顺序，未设计尺寸标为不按比例。
- 可用 Node 的最小 DOM/ResizeObserver 替身执行内嵌脚本，在 320/736 px 调用两种状态处理器，检查生成坐标没有 NaN/undefined。此法已验证脚本与状态切换，不代替浏览器视觉检查。
- 案例代码：[盖盒螺钉连接](references/local-cases.md#case-1)。本例是通用原理示意，无厂家尺寸依据。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
