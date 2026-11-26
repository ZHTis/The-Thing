# 共享技能维护

本目录是完整共享技能仓库和本机唯一维护来源。保持每个技能原有目录及相对引用；绘图建模与文档汇报技能保持独立。

修改技能前读取 skill-creator 和 writing-for-agents 的 SKILL.md。保留第三方来源与许可；当前内容包含第三方技能及本地修改，不统一重新授权。

用户选择手动上传。未实际启用 implement 工作流时，修改和检查完成后报告文件与结果，由用户决定是否 commit；实际启用 implement 时，检查通过后自动 commit 该任务相关文件，保留无关修改。仅讨论技能名称不算启用 implement，implement-spec 不自动继承该例外。Push 仍需单独明确授权，不创建上传定时任务或文件监听。

工具目录链接同一份内容。新增工具前核对其技能发现路径；已有目录或同名技能先比较，保留原内容，避免覆盖。

## Agent Skills 标准维护

所有 SKILL.md 使用规范字段，metadata 仅使用字符串值；工具扩展放在 agents 中。分类更新同时维护 taxonomy.json 与 FUNCTIONAL-INDEX.md，drawing-* 统一归类但保留按格式和用途拆分，文档汇报单列。入口保持少于 500 行；本机案例路径放在 references/local-cases.md 并保留来源与验证边界。新增工具依赖写 compatibility，不能用格式通过代替执行验证。

修改后运行 scripts/validate_skills.py（使用 requirements-validation.txt 的独立环境）；需要迁移原始工具字段时保留调用策略和来源。系统技能可能被应用升级覆盖，升级后重跑检查。提交遵循上述 implement 例外；上传仍由用户明确指示。

## Lint 默认规则

每次新增或修改技能运行 `scripts/lint_skills.py`，使用 requirements-validation.txt 的独立环境。规则详见 LINT.md，覆盖全部技能；新增检查应以反例验证。客观可判定、反复出现的问题优先通过接口约束、类型、lint或测试解决；需要判断的内容留在技能说明中，不把单次修正无限扩大。

执行具体技能任务时优先复用目标项目现有 lint 和确定性检查，报告检查范围、结果及未验证项。检查通过不代表科学有效性、视觉质量或设备时序已验证。Lint 不执行提交或上传；GitHub检查配置在用户上传后才在线运行。

## 方案阶段与发布边界

仅要求出方案时止于方案；规格、任务拆分和实现各自按实际请求进入。to-spec/to-tickets默认生成可审阅草稿，草稿确认不自动变成外部发布授权。发布issue、创建/推送PR、推进tracker状态及上线等动作按用户已明确授权的范围执行；已有授权无需重复确认。

## 宠物能力入口

ChatGPT Work宠物制作与管理使用官方work-pets插件；需要额外审查模板、修复记录或回归验证时读取 work-pets-support/SKILL.md。用户明确选择Codex本地宠物时使用该补充包的独立兼容分支，分别使用对应格式、脚本、验收与安装方式。目标不明确先澄清。原hatch-pet不再作为独立技能入口；兼容能力和原件均保留，不把Work创建成功当作Codex本地安装成功。
