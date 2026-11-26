---
name: drawing-png-cad-preview
description: 将已有 CadQuery 实体用 Matplotlib 输出 PNG 工程模型预览；用于简易检查形状和布局，不用于照片级渲染或编辑用户图片。
compatibility: Python with CadQuery, NumPy and Matplotlib; STL reader for mesh comparisons.
metadata:
  the-thing.category: drawing-modeling
---
# PNG：CAD 模型预览

工具：CadQuery、NumPy、Matplotlib。

1. 对实体 tessellate()，将顶点与三角面转换为 NumPy 数组。
2. 用 Poly3DCollection 加入三维坐标轴，设置零件颜色；按模型实际长宽高设置 box_aspect，避免比例失真。
3. 设置视角、标题和留白，用 savefig(..., dpi=170) 导出 PNG。
4. 打开图片检查遮挡、轮廓、裁切和可读性；图片仅作预览，尺寸以 CAD 文件为准。

已遇问题：shade=True 时与 edgecolors='none' 的组合曾触发广播错误；可省略 edgecolors 并用 linewidths=0。不要随意关闭 computed_zorder，可能产生错误遮挡；Matplotlib 三维排序仍有限，复杂模型如出现穿透，应改用具备深度缓冲的 CAD 渲染器。

字体或缓存目录不可写时，指定可写缓存目录。临时 Python 环境可能被清理，复用前检查依赖。

已验证案例：[本机案例 1](references/local-cases.md#case-1)


## 已有 STL 网格对比

可直接读取 STL 顶点/面，不必先转 CadQuery。原版与候选使用相同坐标变换、正交视角、包围盒比例与法线光照着色；保留面片阴影以免仅视觉平滑冒充几何修改。中文可用已存在的 STHeiti 字体。打开最终 PNG 检查两个角度与标题。
案例：[本机案例 2](references/local-cases.md#case-2) 的 preview()。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
