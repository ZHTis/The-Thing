---
name: drawing-png-psychopy-preview
description: 从实际 PsychoPy 刺激绘制代码导出 PNG，检查实验提示和实时反馈布局，不生成虚构实验结果。
---
# PsychoPy 刺激 PNG 检查

- 工具：项目 PsychoPy 运行环境、visual.Window、原生刺激类。
- 用明确标记为模拟的数据创建 windowed 预览；调用真实 draw 后，在 flip 前执行 `win.getMovieFrame(buffer='back')`，保存 `win.movieFrames[-1]` 为 PNG；最后关闭窗口。
- 检查中文、不同阶段、低／高输入及完成页；窗口使用 height 单位并按实际宽高比限制布局。逻辑窗口尺寸不等于 Retina 截图像素尺寸，不把截图当成真实采集数据。
- 本例固定三次反馈尺度、只让真实输入改变圆球；时间进度与力度反馈分别处理。缺数据不虚构互动响应。
- 已验证代码：[预览脚本](/Users/heting/Documents/grip_psychopy/tools/preview_uno_calibration.py)、[刺激绘制](/Users/heting/Documents/grip_psychopy/gripflight/uno_feedback.py)。已在本机窗口模式导出并目视检查；不代表外接屏时序测量。
- 有动画状态时，预览应连续推进同一渲染器的可控时间并逐帧 draw/flip，再截取目标帧；不要刚切换输入就截图，以免误把过渡起点当作稳定状态。本例预览脚本用模拟时钟推进 61 帧；缩回时限另以 30/60/144 Hz 单元测试核验，静态 PNG 本身不能证明实际屏幕时序。
- 实时字号变化用有限档位量化，并只在值改变时设置 height/wrapWidth，避免不变布局每帧重建；用真实渲染器分别检查高输入与静止休息页。原生闪退需另查系统日志与资源生命周期，PNG 通过不等于长期运行稳定。

## TextBox2 中文缺字回归

- 用实际 TextBox2 的 `glFont.face.get_char_index(ord(char))` 检查全部配置标签，0表示缺字；记录 `glFont.filename`，不要只看请求的字体名。macOS 系统字体存在不保证 PsychoPy 可识别，也不保证默认 regular 字重存在；本机 `Heiti TC`＋`bold="light"` 已真实渲染验证，PingFang SC 在该字体管理器中未识别。
- 从运行器实际构造及缺字保护路径生成各阶段 PNG，保留原位布局；缺字断言与目视检查同时通过。案例：`/Users/heting/Documents/paradigm/experiments/tests/test_t05_cjk_render.py`；M05/M06 的真实字体为 STHeiti Light.ttc。

- 项目使用共享 `text_style.chinese_font` 时，原生预览须导入同一字体选择器并携带真实 mode 上下文，不硬编码旧字体。T05 新标签与失效提示已用 Hiragino Sans GB 检查通过；PNG仅证明布局/字形，不证明闭环时序。

- 圆周速度反馈的预览可在实际任务Window.flip前抓取back buffer，测试恒定模拟输入0/停转阈值/反向/无效样本；同时检查日志累计角度与固定半径，单张PNG不能证明转动方向。案例：paradigm 的 `experiments/tests/test_t05_native_smoke.py`，外部输出禁用，已验证并目视检查。

- TextStim需显示汉字间距时，可仅在显示字符串相邻CJK字符间插入U+2005（四分之一em），保留原始日志文本；字号宽度预算计入空白，检查角落文字缓存比较使用同一显示转换。案例：paradigm/experiments/center_out_ball/eightpoint/runtime.py。原生预览能验证字形间隔，Retina窗口裁切须另查坐标范围，不能据此声称全屏布局通过。

- 本机ImageStim RGB浮点数组原生验证应使用[0,1]；[-1,1]会出现肤色变橙及深色裁切。Pillow帧转np.float32/255并flipud适配纹理行原点；用实际back-buffer像素与源色对照，不能只做范围断言。案例T03 animated_cue.py和M03F纯手GIF预览。
