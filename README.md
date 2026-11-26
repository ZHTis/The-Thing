# The Thing

个人完整技能库，按 [Agent Skills Specification](https://agentskills.io/specification) 整理。每个技能独立目录，分类见 [功能索引](FUNCTIONAL-INDEX.md)，逐项整理记录见 [清单](reports/standardization-inventory.json)。分类本身不是标准要求。

## 本机共享

唯一维护目录为 `~/.codex/skills`，Codex 直接使用；`~/.claude/skills` 是指向它的链接。其他机器克隆完整仓库后，根据目标工具实际的技能发现规则配置目录链接。共享文件不会同步聊天、工具权限、Python 环境或插件。

所有绘图技能统一分类，方法和输出格式仍独立，方便准确触发。文档与汇报单列。`.system` 是当前随附系统技能快照；插件缓存中的文档、表格等技能未复制进来。

## 校验

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-validation.txt
.venv/bin/python scripts/validate_skills.py
# 单项官方校验示例
.venv/bin/skills-ref validate case-based-planning
```

skills-ref 是官方的示范参考工具，不是执行质量认证；详细边界见 [兼容性说明](PORTABILITY.md)。

## 手动提交上传

公开仓库：https://github.com/ZHTis/The-Thing 。修改后检查并由用户决定何时提交上传，本任务整理阶段不自动推送。

```sh
cd ~/.codex/skills
git status --short
git add .
git commit -m "更新技能"
git push
```

保留第三方来源和许可，见 [来源](third-party/SOURCES.md)。本仓库不提供统一再授权。历史案例包含本机项目路径，仅用于追溯，不随仓库提供对应项目数据或执行环境。
