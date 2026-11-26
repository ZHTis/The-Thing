# 任务契约

## 方案交接

每项任务集中记录下列信息。复用现有计划、配置和提交；链接到它们而非复制整段聊天。

| 项目 | 要记录的内容 |
|---|---|
| 身份 | task_id、源chat或任务引用、计划版本、目标SSH别名/user@host和预期hostname |
| 目标 | 要完成的具体行为、验收输出/目标状态、允许的修改范围 |
| 仓库 | 工作站路径、URL（无凭据）、完整commit、分支、递归子模块状态、已有工作树修改 |
| 环境 | 操作系统、可执行文件完整路径、环境名称/版本、需要的GPU或库、各项证据/未知状态 |
| 数据 | 原始与派生数据路径、可用性及本次需要的校验信息，不默认上传数据 |
| 操作 | 每一步可读PowerShell、目的、前置条件、验收、预期产物位置 |
| 权限 | 用户实际授权、风险/影响、明确未授权项；任务文件本身不构成授权 |
| 执行 | 当前阶段、task/run ID、日志路径、持久任务机制（如使用）、结果文件与未完成项 |

## 运行器清单

JSON字段见入口链接的 assets/task-example.json。

- `target.ssh_target`、`identity_file`、`expected_hostname` 来自本机实例配置。密钥字段只填文件路径，绝不填私钥、token、密码或带凭据URL。
- `context.repository/environment/data` 分别记就绪状态和证据。运行器只记录这些声明，不会自动证明它们；实际核查写入steps并检查输出。无需某一项时记录not_applicable和原因。
- `authorization.scope`概括已获授权的操作；`execution_mode`仅支持foreground。`timeout_seconds`是整个前台任务预算，不是脱离SSH继续运行的保证。
- `steps[].script`是实际PowerShell正文；`expect`是每步非空的多行正则验收列表。只检查宽泛的“成功”字样会误判；要求具体commit、文件存在性、数量、状态或结构化字段。验证命令自身亦应在失败时返回非零。
- 每步独立连接，显式设置 `Set-Location -LiteralPath ...`、Python可执行文件或环境初始化。原生程序每次调用使用wrapper提供的 `Invoke-CheckedNative -File 'git' -Arguments @('-C', $repo, 'rev-parse', 'HEAD')`，避免中间native失败被后续成功覆盖。
- `log_file`是技能目录外的本地追加日志；优先放在私有运行目录，避免被提交。当前runner在日志中写入最终 `task_result`，没有隐含单独的summary文件；如另存摘要，应从该run ID的日志提取。

同步Git时先检查 `rev-parse HEAD`、`status --porcelain` 和 `submodule status --recursive`，核对完整提交、子模块是否未检出/偏离/冲突。可在已有授权下fetch和切换已核验版本，保留工作树内容；不能以reset清理差异。子模块检出、依赖安装和训练启动是不同的验收阶段。

## 结果摘要

```text
任务ID / run ID：
目标SSH / 实际hostname：
UTC起止时间（如转北京时间，明确时区）：
计划版本 / 工作站仓库完整commit / 子模块状态：
本次实际执行：
每步SSH退出码 / 完成标记 / 输出验收 / 目标状态核验：
代码、环境、数据、任务运行各自状态：
日志位置及定位run ID：
产物位置及可访问性：
未完成 / 失败 / 未核验：
下一步：
```

SSH返回码属于传输/远程进程结果；runner的accepted仅指该次步骤同时满足主机、退出、完成标记和配置的输出条件。它不自动证明科学结果正确、模型有效或所有隐含需求完成。
