---
name: drawing-png-print-table
description: 使用Pillow将长文本表格输出为固定纸张比例、带DPI的打印PNG。
compatibility: Python with Pillow and a font covering the output language.
metadata:
  the-thing.category: drawing-modeling
---
# 打印表格 PNG
- 工具：Pillow Image、ImageDraw、ImageFont；保留内容JSON和生成脚本。
- 按毫米/25.4×DPI计算像素。已验证A4横向400 DPI为4677×3307像素（整数舍入）。
- 按列宽用textlength测量换行；每行高度取该行所有单元格的最大行数，加内边距。迭代字体大小直到全表落在页内，记录实际字号：px×72/DPI。
- 检查每行文字宽度、全表底边及缩略图；不得仅靠缩略图认定实际打印字号足够大。长文单页可能需小字体，交付时说明。
- 保存PNG时设置dpi=(DPI,DPI)。交替浅灰底和深色文字用于分类排版，不代表数值映射。
- 已验证案例：[本机案例 1](references/local-cases.md#case-1)；其内容与布局参数分别在table_content.json和layout.json。
- Markdown 表格同步案例：[本机案例 2](references/local-cases.md#case-2) 从 README 按标题提取表格，配合 `table_sources.json` 保存输出名与列宽权重；用 `sync_if_readme_changed.py` 仅在来源比 PNG 新时重绘。macOS 中文字体可使用 `/System/Library/Fonts/Hiragino Sans GB.ttc`，生成后以原尺寸检查文字截断。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
