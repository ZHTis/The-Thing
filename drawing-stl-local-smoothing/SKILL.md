---
name: drawing-stl-local-smoothing
description: 对现有 STL 局部平滑，保留原件、单位和网格连接，导出并检查候选几何。
---
# STL：受约束局部平滑

工具：NumPy 读取二进制 STL，SciPy 稀疏邻接平均，Blender mathutils.bvhtree 检查交叉。

1. 精确合并重复坐标，查连通分量、开口/非流形边、零面积面；STL 无单位，不擅自换算毫米。
2. 用实际几何选择渐变权重；迭代邻域平滑时限制相对原位移、面面积与法线方向，阻止坏面涉及顶点移动。保留选择权重与输入 SHA256。
3. 导出 float32 前后都检查；重新读 STL 查顶点/边/面积，确认选择区外位移为零。
4. 用同一 BVH 比较原件与候选非相邻三角面交叉对，排除共享顶点面；保护新增交叉涉及区域后重算。零新增不等于消除原有自交，数值接触和邻接面交叉也不在该检查保证内。
5. 原件不覆盖，保存候选、脚本与 JSON。普通高迭代 Laplacian 对细长三角面可能造成翻折；不要仅凭闭合边数宣称可打印。

已验证案例：/Users/heting/Documents/建模/base001_局部圆滑_20261104/process_mesh.py 与 check_intersections.py。参数/选择仅适用对应模型；预览技巧另见 drawing-png-cad-preview。
