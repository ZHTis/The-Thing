# 来源与已验证边界

来源：用户指定的Windows工作站SSH案例（2026-11-26）。公开技能不包含原始工作站日志、私钥、token、原始IP或个人项目数据。

本次直接读取的本机案例脚本：`~/Documents/Codex/query_workstation_folders.py`。对应追加日志由来源chat记录为 `~/Documents/Codex/workstation-ssh.log`；本次没有读取日志正文，也没有重新连接工作站或重复确认远端仓库。

来源chat提供的实际观察：默认SSH密钥失败，指定已授权的密钥成功；多层shell/eval使PowerShell的 `$_` 受损，报错仍可能返回SSH 0；UTF-16LE编码传输保留脚本，Console UTF-8设置解决查询输出的中文乱码；查询逐行打印并追加日志。自动打开Terminal曾因macOS权限被拒，不能声称已开成日志窗。

来源chat还报告：目标项目clone、递归子模块和干净工作树核验成功；网页授权成功后也出现过远端token换取超时。因此通用流程分别核验commit/子模块/工作树与远端凭据可用性，不能把网页成功当成CLI成功。曾有凭据转发动作被审批拒绝，这不授权在通用脚本中绕过。

本次新增runner是配置化实现，不是把原实例脚本原样公开。其传输、退出与验收、部分失败、超时、追加日志和常见凭据脱敏由本技能tests中的离线模拟验证；这不替代在实际Windows PowerShell上的首次只读实测。实例已验证事实、来源chat报告和本次测试保持区分。
