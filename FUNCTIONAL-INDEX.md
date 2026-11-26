# 个人技能功能索引

功能索引不改变技能安装目录。每个技能仍保持独立目录，便于现有工具发现；链接按本文件位置解析。

| 功能 | 主入口 | 按需独立能力 |
|---|---|---|
| 调研与方案 | [case-based-planning](case-based-planning/SKILL.md) | research 深入调研；grilling 推敲方案；prototype 原型验证；wayfinder 大型探索 |
| 计划与进展 | [plan-progress-sync](plan-progress-sync/SKILL.md) | to-spec 形成规格；to-tickets 拆解任务；triage 分诊需求 |
| 神经数据分析 | 按问题选择 | neural-data-model-adapters 数据集与模型适配；neural-data-splits-batches 样本、划分与组批；两者保持独立 |
| 编程与审查 | implement 单项实现；implement-spec 多任务实现 | diagnosing-bugs 诊断；tdd 测试驱动；code-review 审查；codebase-design 与 improve-codebase-architecture 架构 |
| 工程配置 | 按问题选择 | setup-pre-commit、git-guardrails-claude-code、scaffold-exercises、migrate-to-shoehorn、wizard |
| 交接与复盘 | 按问题选择 | handoff、claude-handoff、retro；ask-matt 保留上游工作流索引 |

## 保持原样的类别

绘图与建模（drawing-*）与文档汇报、写作技能保持独立，本次没有合并或修改；插件管理的文档与汇报技能也未改动。

## 兼容与来源

- grill-me 与 grill-with-docs 保留旧名字，统一进入 grilling，后者选择记录模式。
- research、to-spec、to-tickets 保留独立调用，方案主入口按需衔接；不强制每次走全流程。
- mattpocock 来源技能存在本地定制；未来升级应比较差异后合并，避免覆盖。备份位置见本次操作输出。
