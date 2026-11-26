# 共享技能维护

本目录是完整共享技能仓库和本机唯一维护来源。保持每个技能原有目录及相对引用；绘图建模与文档汇报技能保持独立。

修改技能前读取 skill-creator 和 writing-for-agents 的 SKILL.md。保留第三方来源与许可；当前内容包含第三方技能及本地修改，不统一重新授权。

用户选择手动上传。技能修改、检查完成后报告修改文件和验证结果，由用户决定何时提交或上传。未经新的明确指令，不自动 commit、push，不创建上传定时任务或文件监听。

工具目录链接同一份内容。新增工具前核对其技能发现路径；已有目录或同名技能先比较，保留原内容，避免覆盖。

## Agent Skills 标准维护

所有 SKILL.md 使用规范字段，metadata 仅使用字符串值；工具扩展放在 agents 中。分类更新同时维护 taxonomy.json 与 FUNCTIONAL-INDEX.md，drawing-* 统一归类但保留按格式和用途拆分，文档汇报单列。入口保持少于 500 行；本机案例路径放在 references/local-cases.md 并保留来源与验证边界。新增工具依赖写 compatibility，不能用格式通过代替执行验证。

修改后运行 scripts/validate_skills.py（使用 requirements-validation.txt 的独立环境）；需要迁移原始工具字段时保留调用策略和来源。系统技能可能被应用升级覆盖，升级后重跑检查。提交上传继续由用户明确指示。
