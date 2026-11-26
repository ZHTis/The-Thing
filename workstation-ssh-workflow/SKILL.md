---
name: workstation-ssh-workflow
description: 将本机或当前chat的方案交接到Windows工作站，通过SSH执行已授权任务并实时返回可审计日志；用于同步仓库、核验环境和数据就绪状态、运行工作站命令及跨chat交接，区分命令退出与任务验收。
compatibility: Python 3.10+ and OpenSSH on the caller; Windows OpenSSH Server and PowerShell 5.1+ or pwsh on the target; destination-owned credentials and an already trusted host key. Durable long tasks require a separately authorized scheduler.
metadata:
  the-thing.category: engineering-setup
---
# 方案交接、工作站执行与诚实 SSH 日志

## 入口与边界

先读取当前任务和已有项目约定。本技能承接已明确的方案；只有用户要求出方案时才开展方案调研。跨 chat 使用任务文件、提交和日志交接，不假定共享完整聊天上下文。用户允许独立 SSH 时可以独立连接，但明确说这是新建连接；不得声称在其已有终端里输入。

本技能管理交接与执行证据，不规定训练配方、冻结权重或数据分析方法。创建技能不等于获准连接、安装环境、复制凭据、启动训练或覆盖仓库。每一步沿用会话中实际授权；批准过的同范围操作无需反复确认。审批拒绝后停止被拒操作，说明原因，不能编码或换工具绕过。

## 最少工作流

1. **交接**：按[任务契约](references/task-contract.md)记录任务ID、当前目标/验收、目标主机、仓库完整提交与子模块、环境和数据路径、命令、产物、风险与授权范围；未知项写明待核验。方案、代码就绪、数据就绪、环境就绪、已提交任务、运行完成分别记录。
2. **预检**：只读确认 SSH 身份、实际 hostname、仓库 HEAD/子模块/工作树，以及本次需要的环境和数据状态。连接用本机配置的密钥路径，不读出或传送私钥；认证优先在目标机独立完成。网页显示授权成功后，还要以远端工具返回和实际仓库访问确认认证落地。
3. **同步**：将确定的提交、任务清单和必要的小配置同步到工作站，核对版本及路径。已有目录先检查，保留未提交修改；不能自动 reset、clean 或覆盖数据。不把“clone成功”写成“环境已配置”或“训练已开始”。
4. **展开并执行**：向用户展示实际目标和展开后的可读命令。通过[审计运行器](scripts/ssh_task.py)或能提供同等证据的已验证工具逐步执行；原始示例见[配置模板](assets/task-example.json)。默认只预览，`--execute` 仅用于已授权且已审阅的本地清单。PowerShell正文用 UTF-16LE/Base64 编码传输，SSH由argv启动，避免eval和多层shell拼接。
5. **日志与验收**：命令、合并stdout/stderr、UTC时间、任务ID/run ID、实际主机、退出码和输出验收逐条同步到用户并追加到同一日志。前台失败、超时或不完整时停止后续步骤，保留已完成与未开始项；详见[执行与故障处理](references/execution.md)。退出码0不足以证明成功，必须同时核对任务要求的实际输出或目标状态。
6. **返回**：按[结果模板](references/task-contract.md#结果摘要)报告主机、时间范围、任务/提交、执行内容、SSH退出和验收、日志/产物位置、未完成项与下一步。只把实际查证的项标为完成；模拟测试、本机测试、远端实测分开。

## 使用运行器

路径相对于本技能根目录。把样例复制到公开技能目录之外，填写自己的主机、密钥路径和日志位置；任务文件只保存非秘密配置。

```sh
python3 scripts/ssh_task.py /path/to/local-task.json
python3 scripts/ssh_task.py /path/to/local-task.json --execute
python3 -m unittest discover -s tests -v
```

运行器对每一步新建SSH连接；不会保持用户终端的cwd、虚拟环境或PowerShell变量，所以每步明确所需路径和环境。JSONL日志按每份最多20 MB（20,000,000字节）、含当前文件共保留最近10份轮转，删除最旧份；需长期留存的记录先另行归档。它用于可读审计，不是防篡改存储；日志窗可用 `tail -n 100 -F /path/to/task.jsonl` 跟随轮转，它只展示内容。打开日志窗失败时如实报告并给手动命令，不声称窗口已经打开。

只有具备明确授权的持久任务机制，才可承接长训练/计算：记录远端任务ID、PID、状态/退出文件和远端日志，断开后重新连接核验。运行器只支持前台任务；SSH断开或工具超时后，远端实际状态可能未知，不能推断训练完成或已停止。

## 复用前的验证范围

本技能源于一个实际Windows工作站查询案例，保留[来源与纠错](references/provenance.md)。本次提供的通用运行器通过离线模拟传输测试，不因此声称在每台Windows上实测。日志会对常见凭据形态脱敏，但并非完备识别；执行前选择不会输出秘密的命令，完整日志保留本地，发布摘要只摘取必要的脱敏证据。
