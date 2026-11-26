---
name: work-pets-support
description: 为官方work-pets补充审查记录和26项回归检查，并在用户明确选择Codex本地宠物时提供独立兼容分支；按目标应用选择格式、脚本和安装方式。
compatibility: Python 3.10+ with Pillow; Work checks require the installed official work-pets create-pet directory. Codex compatibility retains a historical local implementation whose current app support must be verified.
license: Apache-2.0; see LICENSE.txt for retained upstream terms.
metadata:
  the-thing.category: drawing-modeling
  the-thing.source: Local hatch-pet regression fixtures; original author unconfirmed; bundled Apache license retained.
---
# Work Pets 补充与 Codex 兼容

先明确目标应用。ChatGPT Work 宠物以已安装的官方 `work-pets` 插件及 create-pet/update-pet/pets 为主流程，沿用其 Library、Pets MCP 和精灵表契约；需要补充QA时使用本包的Work检查。

用户明确选择Codex本地宠物时，使用下方独立兼容分支。目标不明确先澄清，不能把两个分支的精灵表、验收通过或安装完成互相替代。

## 何时运行

升级插件、排查QA脚本异常或需要确认迁移兼容性时，运行[检查入口](scripts/run_checks.py)。普通宠物请求直接使用官方流程；补充检查不会自动扩大为生成或上传任务，也不替代官方质量检查。

```sh
python3 scripts/run_checks.py --plugin-skill-dir /path/to/work-pets/skills/create-pet
```

路径为当前实际启用版本的 `skills/create-pet` 目录。只有本机缓存中唯一一个版本时可自动定位；存在多个版本则显式指定，避免测错版本。使用具有Pillow的Python环境；缺少依赖时报告未运行，不能声称通过。测试对子进程禁用bytecode写入，临时夹具在结束后删除，不读取实际宠物资料或连接服务。

## 回归检查（24项保留、2项新增）

- 6项：方向行分阶段注册、共享缩放、边缘安全与已通过行的几何保留。
- 10项：色键边缘污染、透明度及颜色保留、跨单元格污染隔离。
- 7项：方向验收的hard/review区分、连续性告警和盲测图结构。
- 1项：盲测严格多数票与平票歧义处理。
- 新增2项：官方73个必需槽位通过、旧版额外中立帧槽位被拒绝，防止迁移时混入不兼容布局。

规则与缺失能力比较见[迁移记录](references/migration.md)。测试报告只证明当前官方脚本通过这些夹具；它不证明宠物视觉语义、动画质量或实际上传成功。官方结构/质量/视觉/MCP门槛仍全部适用，不能用补充测试的成功覆盖官方失败。

## 流程补充

需要隔离盲审任务模板、阶段计时或修复审计时，读取[审查与修复记录](references/review-and-repair.md)，把补充内容接到官方对应阶段，官方所有失败门槛继续有效。

## Codex 本地兼容分支

用户已要求保留此能力，分支入口见[兼容说明](references/codex-compatibility.md)。本分支保存历史Codex工具和本地pet.json打包流程；它不创建ChatGPT Work宠物，不调用Library/Pets上传流程。当前Codex应用是否接受该旧布局仍需实际验证。

```sh
python3 scripts/run_checks.py --target codex
```

此命令只运行24项旧工具离线测试，不安装或激活宠物。真正制作前按实际所需阶段阅读下列历史流程；命令路径均相对于 `compat/codex`，图像生成与访问权限继续遵循当前用户和系统指令。

- [Hatch Pet](compat/codex/references/workflow-01-introduction.md)
- [Overview](compat/codex/references/workflow-02-overview.md)
- [Existing Inputs And Upgrades](compat/codex/references/workflow-03-existing-inputs-and-upgrades.md)
- [Generation Delegation](compat/codex/references/workflow-04-generation-delegation.md)
- [Runtime Dependencies](compat/codex/references/workflow-05-runtime-dependencies.md)
- [Storage Controls](compat/codex/references/workflow-06-storage-controls.md)
- [Brand Discovery](compat/codex/references/workflow-07-brand-discovery.md)
- [Generation Contract](compat/codex/references/workflow-08-generation-contract.md)
- [Pet-Safe Styles](compat/codex/references/workflow-09-pet-safe-styles.md)
- [Transparency And Effects](compat/codex/references/workflow-10-transparency-and-effects.md)
- [Visible Progress Plan](compat/codex/references/workflow-11-visible-progress-plan.md)
- [Time Budget And Convergence](compat/codex/references/workflow-12-time-budget-and-convergence.md)
- [Default Workflow](compat/codex/references/workflow-13-default-workflow.md)
- [Required V2 Look-Direction Stage](compat/codex/references/workflow-14-required-v2-look-direction-stage.md)
- [Lightweight Visual Workers](compat/codex/references/workflow-15-lightweight-visual-workers.md)
- [Subagent Delegation](compat/codex/references/workflow-16-subagent-delegation.md)
- [Repair Workflow](compat/codex/references/workflow-17-repair-workflow.md)
- [Rules](compat/codex/references/workflow-18-rules.md)
- [Acceptance Criteria](compat/codex/references/workflow-19-acceptance-criteria.md)
