---
name: drawing-png-scientific-summary
description: Render fixed-scale scientific candidate-summary PNGs from precomputed tables.
---

# PNG 科学候选总览

- 用途：将重复条件下的候选以分面点图汇总；不重新计算统计量或候选标签。
- 实现：Matplotlib；固定发散色标，负值绿色、0 浅色、正值紫色（`PRGn_r`）；点位置/颜色表示有符号效应，横线为 session IQR，点面积为实际覆盖量。
- 检查：保存前用支持中文的系统字体（如 `PingFang SC`），并在同一图中固定 `vmin/vmax`；视觉检查中文标签、误差线和无候选分面均可读。
- 双语导出：表中保留原始标签；仅在绘图层用显式映射生成英文标签，并另存 `_en` 文件，避免修改原始结果或覆盖原语言图。
- 结果汇总：可将既有、版本化的结果 PNG 编排为一张大图；只加展示层分面标题与读图说明，不重新计算统计量。若源图标题含不宜展示的来源标识，可裁去标题区，并在汇总图补写中性说明。
- 分类标记：源图颜色已编码效应量时，把左右手等类别放在分面标题颜色与显式图例中，并声明该颜色不编码效应方向，避免和原图色标混淆。
- 矩阵单元：若通道×特征热图需要比较单元面积，直接从已保存表重画同一数值与顺序，使用 `imshow(..., aspect='equal', interpolation='nearest')`；不要横向拉伸原始 PNG。
- 已验证案例：`/Users/heting/Documents/readGripData/analysis_tools/render_candidate_overview.py`，输出 `candidate_overview.png` 与同名 CSV。

## 空间障碍候选图

- 从中心坐标与宽高用 Matplotlib Rectangle 绘制真实矩形边界；不同候选固定同一 X/Y 范围。全程很长时同时提供全图和实际任务时间覆盖段的放大图，明确横轴压缩且单位为游戏坐标。
- 比较形状分布时保留随机种子与原数据来源；长度和数量相同不代表动力学难度等效。静态图须注明编辑坐标后不会自动重画。
- 已验证代码：/Users/heting/Documents/grip_psychopy/tools/plot_candidate_maps.py；10 图前段分面和全图/局部双视图均已目视检查。


## 串口采集质量时间序列

- 只读 SQLite 事务取同一快照（含已提交 WAL），保留时间、记录 ID 边界和会话状态；活动会话仅代表已落盘区间。
- 将原始信号／阶段色带、每整秒主机帧数、设备与主机间隔、累计序号缺失分面。序号按 uint32 回绕检查，重复／重置与缺号分开，退出半行不计作内部丢点，首尾之外不外推。设备时间采样率和主机接收率分别标注。
- 中文字体须验证真实路径；本机 Matplotlib 使用 `/System/Library/Fonts/STHeiti Light.ttc`，不要假定 PingFang 的固定文件路径存在。先目视检查图例不遮数值；短会话不足窗口时用缺值，不伪造 0 Hz。
- 已验证代码：`/Users/heting/Documents/grip_psychopy/tools/analyze_grip_quality.py`；实际五段记录图已目视检查，缺号、回绕、重置及真实序号端点交叉核验通过。

## 材料配平报告

- 已保存词表的逐词散点/箱线图与报告的两两绝对 SMD 热图并列；色标固定0–1，全表与评分子集用分隔线及真实 n 区分。评分误差线注明均值±SD，不能写作CI；按位置画声调边际时注明不代表联合组合匹配。
- 保存原词表和报告 SHA-256、显示抖动种子与 DPI；只在绘图层读数据，不改材料选择。检查中文、图例和说明无重叠，并校验输出像素及来源哈希。
- 已验证代码：`/Users/heting/Documents/paradigm/assets/word_library/render_semantic_balance.py`；PNG 为3840×3600、240 DPI，已目视检查。


## TTL 与 LSL 时差检查

- 同时画去固定时钟偏移的时间差、去线性漂移残差及相邻事件间隔差；报告漂移 ppm 和残差 P95，不能把拟合后的残差称为绝对硬件延迟。
- 先检查跨 RHD 文件采样时间连续性、TTL 边沿数量与 XDF 真实标签数量；排除额外边沿须保留时间和理由，顺序匹配需由相邻间隔一致性支持。原始 sender LSL 时间与接收端时钟校正分开说明。
- 已验证代码：`/Users/heting/Documents/ChatGPT/范式是假设的验证/ttl_lsl_check/check.py` 和 `plot.py`；PNG 已目视检查。

- 同步检查可拆成首事件归零的累计漂移、残差直方图（±绝对残差P95带）、阶段×trial残差热图及标签覆盖图；热图色标以0居中并固定范围。独立图注用 figure text 的 va="top" 并预留底部空间，避免多行文字从基线向上侵入横轴标签。已验证：`/Users/heting/Documents/ChatGPT/范式是假设的验证/ttl_lsl_check/alternatives.py`。

## 多组电生理频谱 PNG

- 使用统一 Welch 窗长与重叠率，逐文件累加窗功率后按窗数加权；保存逐通道线性 PSD，展示通道中位数与 IQR（不是置信区间）。组图固定纵轴，热图固定色标，配低频放大与全频段。
- 核对 RHD 头与 settings.xml 的陷波及参考设置；不同设置不直接作条件因果比较。末尾不足完整块时记录排除字节数，不静默解码。
- 已验证代码与官方读取来源：`/Users/heting/Documents/1120实验记录C57派特塞/1120频谱分析/analyze_spectra.py`；同目录 `importrhdutilities.py` 来自 https://github.com/Intan-Technologies/load-rhd-notebook-python 。分组及通道热图已目视检查。


## 多词表交集与六圆示意

- 用原始刺激字符串构建集合，保存逐项归属与互斥交集；校验并集大小、各集合大小及覆盖人数加权总和。
- 六个等面积圆可用圆交面积公式反解两两距离，再多起点拟合圆心；六圆不能精确表达任意高阶交集，须明确为示意、报告两两面积最大误差，并配精确交集矩阵与覆盖人数分布。不可把中心面积解释为真实六组交集。
- 先验证中文字体与外侧标签无裁切，再导出 PNG/SVG。已验证代码：`/Users/heting/Documents/summaries/1127 素材/build.py`。
