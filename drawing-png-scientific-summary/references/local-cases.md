# 本机历史案例与来源

以下为整理前已记录的案例及代码位置，原样保留以便追溯。它们不是随技能安装的依赖；其他机器需定位自己的项目文件。本次整理没有重新运行这些案例，也不新增验证结论。

## Case 1

- 已验证案例：`/Users/heting/Documents/readGripData/analysis_tools/render_candidate_overview.py`，输出 `candidate_overview.png` 与同名 CSV。

## Case 2

- 已验证代码：/Users/heting/Documents/grip_psychopy/tools/plot_candidate_maps.py；10 图前段分面和全图/局部双视图均已目视检查。

## Case 3

- 已验证代码：`/Users/heting/Documents/grip_psychopy/tools/analyze_grip_quality.py`；实际五段记录图已目视检查，缺号、回绕、重置及真实序号端点交叉核验通过。

## Case 4

- 已验证代码：`/Users/heting/Documents/paradigm/assets/word_library/render_semantic_balance.py`；PNG 为3840×3600、240 DPI，已目视检查。

## Case 5

- 已验证代码：`/Users/heting/Documents/ChatGPT/范式是假设的验证/ttl_lsl_check/check.py` 和 `plot.py`；PNG 已目视检查。

## Case 6

- 同步检查可拆成首事件归零的累计漂移、残差直方图（±绝对残差P95带）、阶段×trial残差热图及标签覆盖图；热图色标以0居中并固定范围。独立图注用 figure text 的 va="top" 并预留底部空间，避免多行文字从基线向上侵入横轴标签。已验证：`/Users/heting/Documents/ChatGPT/范式是假设的验证/ttl_lsl_check/alternatives.py`。

## Case 7

- 已验证代码与官方读取来源：`/Users/heting/Documents/1120实验记录C57派特塞/1120频谱分析/analyze_spectra.py`；同目录 `importrhdutilities.py` 来自 https://github.com/Intan-Technologies/load-rhd-notebook-python 。分组及通道热图已目视检查。

## Case 8

- 先验证中文字体与外侧标签无裁切，再导出 PNG/SVG。已验证代码：`/Users/heting/Documents/summaries/1127 素材/build.py`。
