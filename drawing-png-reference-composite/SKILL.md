---
name: drawing-png-reference-composite
description: 用 image_gen 将实物照片中的设备合成到框架截图，并按手绘路径生成管路效果图。
compatibility: Image-generation/editing capability and user-provided equipment/reference images.
metadata:
  the-thing.category: drawing-modeling
---
将基底图、实物参考图分别指定角色；提示中逐条描述手绘粗线与细线代表的实体、两端连接对象和悬垂走向，要求移除原标记。用内置 image_gen 编辑；不以手绘尺寸作为准确工程尺寸。
HEIC 无法直接查看时，可用 sips -s format png 输入 --out 输出转换，再 view_image 核对；转换失败需检查执行权限。
检查泵头身份、端口与软管连续性、框架遮挡和水瓶是否落在层板上；保存原图来源及提示。效果图不能证明支撑结构或尺寸可制造。
已验证案例：[本机案例 1](references/local-cases.md#case-1) 与同名 PNG。

纠错：指定旋转时同时写出局部特征的新方向（右侧安装耳→上方、开关→左侧、端口→下方），并说明挂接哪根横梁与螺钉接触位置；只说旋转90度容易遗漏悬挂关系。验证案例：pump-frame-hanging-v3.png（上述案例目录）；生成图仍可能改变面板比例，不当作精确CAD旋转。

管路纠错经验：同时要求“支架”和管路时，生成器可能复制金属管或留下无连接软管。将支架明确限定为平板、指定单根硬管和两根软管的起终点，逐条追踪连续性；重绘后仍遮挡的部分应注明未验证，不能只凭局部正确宣布完成。案例：pump-frame-supported-v4.txt。

空间换面时，用可见立柱定义前右角与后右角，指定两柱间的侧横梁和设备面平行关系，比仅写“右侧”更明确。案例：pump-frame-right-side-v5.png；已验证侧面位置变化，软管连续性仍不可靠。

## 案例来源的使用范围

本机案例与代码位置见 [local-cases](references/local-cases.md)。案例文件未随技能打包，先查可用性；复用通用方法时使用当前项目输入，不能把旧案例验证等同于本次验证。
