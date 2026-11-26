# 本机历史案例与来源

以下为整理前已记录的案例及代码位置，原样保留以便追溯。它们不是随技能安装的依赖；其他机器需定位自己的项目文件。本次整理没有重新运行这些案例，也不新增验证结论。

## Case 1

- 案例脚本：/Users/heting/Documents/ChatGPT/范式是假设的验证/animations/build_right_hand_raise.py；本机PsychoPy解释器含Pillow，默认python3不一定包含。

## Case 2

- 白底蓝色网格手势可先画掌面，再把每根手指画为三段相连的圆角路径；蓝色外轮廓及关节圆端须先画，白色内层后画，避免关节出现一串独立圆环。沿每段切向／法向加纵横网格，逐指设置屈曲量；用四关键帧总览检查张开、过渡、闭合、返回。已验证 600×600、2.4 秒循环 GIF：`/Users/heting/Documents/paradigm/assets/gesture_animations/blue_grid_hand/build_gesture_animations.py`（2026-11-14）；仅为无角度标定的示意运动。
