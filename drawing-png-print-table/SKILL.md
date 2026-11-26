---
name: drawing-png-print-table
description: 使用Pillow将长文本表格输出为固定纸张比例、带DPI的打印PNG。
---
# 打印表格 PNG
- 工具：Pillow Image、ImageDraw、ImageFont；保留内容JSON和生成脚本。
- 按毫米/25.4×DPI计算像素。已验证A4横向400 DPI为4677×3307像素（整数舍入）。
- 按列宽用textlength测量换行；每行高度取该行所有单元格的最大行数，加内边距。迭代字体大小直到全表落在页内，记录实际字号：px×72/DPI。
- 检查每行文字宽度、全表底边及缩略图；不得仅靠缩略图认定实际打印字号足够大。长文单页可能需小字体，交付时说明。
- 保存PNG时设置dpi=(DPI,DPI)。交替浅灰底和深色文字用于分类排版，不代表数值映射。
- 已验证案例：/Users/heting/Documents/readGripData/analysis_outputs/results/stage_reports/paired_summary_table/render_table.py；其内容与布局参数分别在table_content.json和layout.json。
- Markdown 表格同步案例：`/Users/heting/Downloads/素材/范式表格PNG/render_experiment_tables.py` 从 README 按标题提取表格，配合 `table_sources.json` 保存输出名与列宽权重；用 `sync_if_readme_changed.py` 仅在来源比 PNG 新时重绘。macOS 中文字体可使用 `/System/Library/Fonts/Hiragino Sans GB.ttc`，生成后以原尺寸检查文字截断。
