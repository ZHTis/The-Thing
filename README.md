# The Thing

个人完整技能库，按 [Agent Skills Specification](https://agentskills.io/specification) 整理。每个技能独立目录，分类见 [功能索引](FUNCTIONAL-INDEX.md)，逐项整理记录见 [清单](reports/standardization-inventory.json)。分类本身不是标准要求。

## 本机共享

唯一维护目录为 `~/.codex/skills`，Codex 直接使用；`~/.claude/skills` 是指向它的链接。其他机器克隆完整仓库后，根据目标工具实际的技能发现规则配置目录链接。共享文件不会同步聊天、工具权限、Python 环境或插件。

所有绘图技能统一分类，方法和输出格式仍独立，方便准确触发。文档与汇报单列。`.system` 是当前随附系统技能快照；插件缓存中的文档、表格等技能未复制进来。

## 校验

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-validation.txt
.venv/bin/python scripts/lint_skills.py
.venv/bin/python -m unittest discover -s tests -v
# 单项官方校验示例
.venv/bin/skills-ref validate case-based-planning
```

skills-ref 是官方的示范参考工具，不是执行质量认证；详细边界见 [兼容性说明](PORTABILITY.md)。

## 手动提交上传

公开仓库：https://github.com/ZHTis/The-Thing 。未启用 implement 时由用户决定是否提交；实际启用 implement 完成验证后自动提交该任务相关文件。Push 仍须单独明确授权，本任务仅修改规则，不自动推送。

```sh
cd ~/.codex/skills
git status --short
git add .
git commit -m "更新技能"
git push
```

保留第三方来源和许可，见 [来源](third-party/SOURCES.md)。本仓库不提供统一再授权。历史案例包含本机项目路径，仅用于追溯，不随仓库提供对应项目数据或执行环境。

## Lint 规则

全部技能统一运行 [Lint 规则](LINT.md)，错误包含规则编号和修复提示。GitHub Actions 配置在上传后的 push/PR 上运行相同检查，本地没有自动提交或上传。

## 草稿、发布与宠物流程

仅出方案不会自动进入规格、任务、代码和发布整套流程；外部发布遵循用户授权。ChatGPT Work宠物使用官方work-pets插件；共享库的 [work-pets-support](work-pets-support/SKILL.md) 补充回归/审查，并在用户明确选择Codex本地目标时提供独立兼容分支。两种格式和安装结果分开验证，旧hatch-pet入口已归档。
