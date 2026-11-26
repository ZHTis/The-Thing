---
name: drawing-gif-gesture
description: 用Pillow绘制原创示意动作并导出循环GIF。
compatibility: Python with Pillow; frame and duration inspection.
metadata:
  the-thing.category: drawing-modeling
---
# 示意动作GIF

- Pillow在2倍画布绘制肢体，局部坐标用sin/cos围绕关节旋转，smoothstep控制抬起/保持/回落，缩小抗锯齿后save_all导出。
- 正面人物解剖右侧在画面左侧，显式标注视角；示意图不声称精确运动学。
- 检查关键帧及画布边界。GIF编码会合并静止重复帧，不断言帧数等于输入帧数；核验尺寸、有效帧和累计duration。
- 案例脚本：[本机案例 1](references/local-cases.md#case-1)；本机PsychoPy解释器含Pillow，默认python3不一定包含。

- 单指提示先按视角核对拇指—食指相邻关系，不能按画面横坐标顺序直接套食/中/环/小标签；用关键帧总览逐项核对。腕屈伸用侧视，尺桡偏用掌/背视，避免二维投影混淆；动作范围未标定须明确。案例：同对话animations/PMC5621048/build_actions.py，原论文Figure1定义对应A1–A11。

- 白底蓝色网格手势可先画掌面，再把每根手指画为三段相连的圆角路径；蓝色外轮廓及关节圆端须先画，白色内层后画，避免关节出现一串独立圆环。沿每段切向／法向加纵横网格，逐指设置屈曲量；用四关键帧总览检查张开、过渡、闭合、返回。已验证 600×600、2.4 秒循环 GIF：[本机案例 2](references/local-cases.md#case-2)（2026-11-14）；仅为无角度标定的示意运动。

- 侧向抓握明确建立五条digit路径（拇、食、中、环、小），先掌/前臂后手指，深色细轮廓区分重叠；拇食指与杯柄接触，其余三指独立屈曲。代码数量断言与关键帧目视并用，路径条数不能单独证明解剖准确。案例PMC5621048的A3修订。

- 前臂旋前/旋后固定肩肘腕中心，沿前臂长轴旋转掌/指横截面，正交投影y*cos(theta)-z*sin(theta)，以掌纹/手背指甲区分掌向；不能绕腕平面旋转代替。关键帧确认上臂不动、肘角不变、腕中立。案例assets/gesture_animations/forearm_rotation/build_forearm_rotation.py，近似示意而非解剖标定。

- 抓握图不能调用已含五指的通用palm()后再加抓握手指；拆成掌/腕底形和恰好五条digit路径，逐帧复用，避免双重指尖。A2圆柱抓握已按此修复并目视核对关键帧。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
