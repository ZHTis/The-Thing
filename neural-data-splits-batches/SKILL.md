---
name: neural-data-splits-batches
description: 设计或审计脑电及语言神经解码数据管线时，管理逐样本元数据、训练验证测试划分和batch组批策略；用于滑窗、跨run或跨被试评估及模型对比。
compatibility: Access to dataset metadata and split/sampler configuration; data runtime required only for executed
  checks.
metadata:
  the-thing.category: neural-data
---
# 样本来源、数据划分与组批

## 样本来源

为每条送入模型的样本保留稳定sample_id，以及dataset_id、subject_id、session_id、run_id、block_id、trial_id、窗口起止时间、标签和source_file。缺失字段明确记录unknown或not_applicable，不能推断或伪造。

时间字段注明单位、相对原点和所属时钟；窗口同时记录原始采样索引、原始采样率及重采样映射。多层标签用具名字段保存，并记录标签来源。通道表保留通道ID、顺序、参考、选择和融合映射；元数据通过sample_id与张量、预测结果一一对应，避免数据打乱后失联。

明确张量每个轴的含义。batch轴只代表一起计算的样本数量，不编码被试或run；同一batch是否跨被试、跨run由采样策略决定。通道融合通常在每条样本内部执行，不能把batch轴解释为融合后的通道。

## 先定义泛化目标，再划分

明确评估的是同被试新trial、新block、新run、新session，还是新被试，并选择对应的分组隔离单位。组合键包含dataset和subject等上层ID，避免不同被试的run编号重复。

先分配原始trial或更高层组到train/validation/test，再生成窗口；同一trial及其重叠窗口、增强副本保留在同一集合。连续记录的窗口在集合边界保持时间隔离，检查原始时间区间重叠与滤波跨界影响。

保存可复用的split manifest：sample或trial ID、group ID、集合、fold、划分种子和版本。区分“比例相同”“分组规则相同”“具体样本索引相同”，仅在核验后声称一致。已有官方划分先保留用于复现；如另做严格分组评估，分别报告。

标准化统计、PCA、数据驱动通道选择、特征选择等在当前训练fold拟合，验证与测试仅应用。超参数在训练内部的分组验证中选择，锁定方案后评估测试集。记录预训练是否接触下游测试记录；无标签接触也需披露，区分归纳式与传导式设置。

## 划分后组batch

在每个集合内独立配置DataLoader或sampler，记录batch size、shuffle、采样种子、drop_last、类别平衡、被试/run混合策略；使用梯度累积或多设备时记录有效batch size。

按sample_id检查实际batch成员，不能只凭张量形状或随机种子断言跨被试、同run或批次一致。验证和测试保留全部样本，报告明确需要排除的例外。

模型对比默认复用划分清单。相同batch size不等于相同样本、顺序或增强。只有研究要求控制组批时，才进一步共享batch成员清单；不同模型的必要输入适配单独记录。

## 完成标准

交付或审计时报告：张量轴定义、元数据字段与缺失项、泛化目标、划分清单、组批策略，以及集合间组ID/原始窗口重叠检查结果。记录拟合型预处理的数据范围、预训练接触范围与未核验项。未运行检查时明确标记为设计或待核验，不能宣称无泄漏。
