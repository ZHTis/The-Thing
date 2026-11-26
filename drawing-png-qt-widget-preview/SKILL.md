---
name: drawing-png-qt-widget-preview
description: 使用真实 PyQt6 QWidget 绘图代码生成 PNG，检查实时曲线窗口的布局；不编辑照片。
---
# Qt 曲线窗口 PNG 预览

- 工具：PyQt6 QApplication、QPainter、QWidget.grab；运行环境须已有 Qt。
- 在单独预览进程中设置 `QT_QPA_PLATFORM=offscreen`，创建真实窗口，注入注明为模拟的数据，`resize → show → processEvents → grab().save(...)`。
- PNG 尺寸取实际生成结果；窗口逻辑尺寸不能直接当作 Retina 像素尺寸。检查中文、轴标签边界、未标定空态、缺失数据断线及超过 100% 的曲线。
- 已验证纠错：若主进程为 SVG 栅格化设置了 offscreen，真实监视子进程启动前需移除该继承变量，否则窗口不可见。实时采集的观察缓存须独立，显示队列有界且非阻塞；这不是提高采样率的方法。
- 可复现代码：[预览脚本](/Users/heting/Documents/grip_psychopy/tools/preview_uno_monitor.py)、[真实绘制与数据逻辑](/Users/heting/Documents/grip_psychopy/gripflight/uno_monitor.py)。本例以模拟信号完成 PNG 目视检查与单屏双窗口联调；不能据此声称双屏时序已实测。
- 曲线叠加日志表格时，预览调用真实 apply_payload 更新子控件后再 grab；验证紧凑尺寸、滚动区边界以及表格获焦后的 Esc（窗口级 QShortcut）。日志与曲线使用同一主机时钟，明确区分事件请求时间和硬件确认／TTL 实测；模拟 ACK/DONE 必须标注无硬件输出。
