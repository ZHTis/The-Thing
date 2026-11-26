---
name: drawing-step-cadquery
description: 用 Python 和 CadQuery 从尺寸图或官方 PCB 文件生成 STEP 实体参考模型，适合外壳设计、安装孔定位及 Fusion 导入。
---
# STEP：尺寸图生成实体

工具：Python、CadQuery（本次验证版本 2.8.0）；Eagle XML 可用 ElementTree 读取。

1. 优先取官方 CAD/尺寸数据，明确单位、原点和坐标方向；将标注尺寸与估算外形分开。
2. 用 Workplane、lineTo、threePointArc 建轮廓，extrude 拉伸；box、circle 建元件，cut 切孔，translate/rotate 定位。
3. 用 Assembly.add 分件命名与着色，再 Assembly.export('model.step')；需要时另导出单独安装板。
4. 用 importers.importStep 重新导入；检查每个实体 isValid()、包围盒、安装孔尺寸和坐标，并查看渲染图。
5. 随模型给出数据来源、简化内容、估算高度和适用版本。参考模型不自动具备加工精度；STEP 也不保留原始参数化建模历史。

注意：PCB 封装主要提供平面数据，不能据此声称元件高度精确；插头空间和焊点间隙需额外考虑。截图未标注的尺寸不能当实测值。

已验证案例：/Users/heting/Documents/ChatGPT/未来不知何去何从的猴子/output/uno_r3_step/build_uno.py

补充验证：多零件机械开关可用 `Assembly.add` 分别加入主体、安装螺纹套、垫圈/螺母、摇柄和端子，导出后用 `importers.importStep` 检查多个有效实体与总包围盒；未标注的端子块尺寸、安装耳和螺纹牙形应在 README 中标为估算或简化。案例代码：[9016 开关](/Users/heting/Documents/ChatGPT/手搓但是会点火/output/cad/9016-toggle-switch/build_model.py)。
