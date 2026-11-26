---
name: drawing-png-task-icon
description: 为本地 PsychoPy 任务制作可直接载入的默认图标。
---

# PsychoPy 默认 PNG 图标

用途：为刺激任务提供一个浏览器可预览、PsychoPy `ImageStim` 可加载的本地图标。

做法：用内嵌 SVG 描述几何图标，再用 macOS `sips -s format png source.svg --out target.png` 转成 PNG；配置使用 PNG 相对路径。

当图标需要更强的瞬时可辨识度时，可用内置图像生成工具直接生成透明背景 PNG；提示中明确列出图形语义、完整构图、禁止文字和小尺寸可辨识性。替换前目视检查红色禁令圈、斜杠和被禁止物都没有被裁切。

检查：浏览器预览和 `ImageStim` 都指向同一 PNG。不要让运行配置直接引用 SVG，因为 PsychoPy 的加载器通过 Pillow 打开文件，不能读取 SVG。案例：`experiments/type2_visual_stimulus/ui/assets/no-smoking.png`。
