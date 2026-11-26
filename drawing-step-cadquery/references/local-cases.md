# 本机历史案例与来源

以下为整理前已记录的案例及代码位置，原样保留以便追溯。它们不是随技能安装的依赖；其他机器需定位自己的项目文件。本次整理没有重新运行这些案例，也不新增验证结论。

## Case 1

已验证案例：/Users/heting/Documents/ChatGPT/未来不知何去何从的猴子/output/uno_r3_step/build_uno.py

## Case 2

补充验证：多零件机械开关可用 `Assembly.add` 分别加入主体、安装螺纹套、垫圈/螺母、摇柄和端子，导出后用 `importers.importStep` 检查多个有效实体与总包围盒；未标注的端子块尺寸、安装耳和螺纹牙形应在 README 中标为估算或简化。案例代码：[9016 开关](/Users/heting/Documents/ChatGPT/手搓但是会点火/output/cad/9016-toggle-switch/build_model.py)。
