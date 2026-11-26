# The Thing

完整本地技能仓库，位置为 `~/.codex/skills`。Codex 直接使用此目录，Claude Code 的 `~/.claude/skills` 链接到此目录，因此修改一份即可共享。未配置的工具需确认支持方式后另行链接。

技能分类见 [FUNCTIONAL-INDEX.md](FUNCTIONAL-INDEX.md)。每个技能的规则在其 `SKILL.md` 中。`.system` 是本机随附系统技能快照，可能随 Codex 升级变化；插件缓存中的文档、表格等技能不在此目录，未复制到仓库。

## 手动上传

远程仓库：`https://github.com/ZHTis/The-Thing`（公开）。本次按用户明确指令提交上传，后续仍由用户决定何时提交上传。

后续更新时在终端执行：

```sh
cd ~/.codex/skills
git status --short
git add .
git commit -m "更新技能"
git push
```

Git 首次提交若提示缺少身份，在本仓库内配置自己的 `user.name` 和 `user.email`。后续更新手动执行 `git add`、`git commit`、`git push`；没有后台自动上传。

## 使用范围

共享文件不等于共享聊天历史、插件权限或运行环境。技能中仍可能有本机路径或工具专属能力，跨电脑使用需按实际环境核对。保留现有第三方许可、署名及来源，不为整个仓库新增统一许可证；本仓库包含第三方技能及本地修改，各项保留原有许可与署名；仓库不提供统一再授权。
