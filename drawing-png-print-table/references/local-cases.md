# 本机历史案例与来源

以下为整理前已记录的案例及代码位置，原样保留以便追溯。它们不是随技能安装的依赖；其他机器需定位自己的项目文件。本次整理没有重新运行这些案例，也不新增验证结论。

## Case 1

- 已验证案例：/Users/heting/Documents/readGripData/analysis_outputs/results/stage_reports/paired_summary_table/render_table.py；其内容与布局参数分别在table_content.json和layout.json。

## Case 2

- Markdown 表格同步案例：`/Users/heting/Downloads/素材/范式表格PNG/render_experiment_tables.py` 从 README 按标题提取表格，配合 `table_sources.json` 保存输出名与列宽权重；用 `sync_if_readme_changed.py` 仅在来源比 PNG 新时重绘。macOS 中文字体可使用 `/System/Library/Fonts/Hiragino Sans GB.ttc`，生成后以原尺寸检查文字截断。
