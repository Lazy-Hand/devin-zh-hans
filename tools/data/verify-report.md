> 本报告读的是**本机真实安装目录的当前状态**，回答「现在是否已落地」。
> 想验证插件*能不能*落地（尤其在新版 Devin 上），跑 `node tools/verify_layers.js --apply`：
> 它在 `resources/app` 的沙盒副本上执行真实落地逻辑，并断言四层结果与幂等性。

## 1. product.json 完整性校验（补丁后重新计算）

| 结果 | 受保护文件 |
|---|---|
| ✅ 一致 | `vs/base/parts/sandbox/electron-browser/preload.js` |
| ✅ 一致 | `vs/workbench/workbench.desktop.main.js` |
| ✅ 一致 | `vs/workbench/windsurf-chat-client/index.js` |
| ✅ 一致 | `vs/workbench/devin-webapp-host/index.js` |
| ✅ 一致 | `vs/workbench/workbench.desktop.main.css` |
| ✅ 一致 | `vs/workbench/api/node/extensionHostProcess.js` |
| ✅ 一致 | `vs/code/electron-browser/workbench/workbench.html` |
| ✅ 一致 | `vs/code/electron-browser/workbench/workbench.js` |
| ✅ 一致 | `vs/sessions/sessions.desktop.main.js` |
| ✅ 一致 | `vs/sessions/sessions.desktop.main.css` |
| ✅ 一致 | `vs/sessions/electron-browser/sessions.html` |
| ✅ 一致 | `vs/sessions/electron-browser/sessions.js` |

**结论：12 个受保护文件全部自洽 → 不会触发“Devin 安装似乎损坏”告警**

## 2. 内置扩展的 %key% 占位符可解析性

| 扩展 | 占位符 | 无法解析 | 缺中文 |
|---|---:|---:|---:|
| `windsurf` | 0 | 0 | 0 |
| `windsurf-dev-containers` | 0 | 0 | 0 |
| `windsurf-remote-devin` | 0 | 0 | 0 |
| `windsurf-remote-openssh` | 0 | 0 | 0 |
| `windsurf-remote-wsl` | 0 | 0 | 0 |

⚠ 安装目录里的 package.json 仍是硬编码英文（尚未落地）。
本插件会在下次激活时写入 **254** 个 `%key%` 占位符与两个 nls 文件；node tools/verify_layers.js --apply 已在沙盒副本上验证该过程（未解析 0、缺中文 0）。


## 3. 语言包 bundle 注册与译文可查性

- 语言包版本 : 1.126.0 (engines.vscode = ^1.126.0)
- 已注册 bundle 数 : **95**
- 含 `windsurf` : ✅
- vscode bundle 译文总量 : **22,003** 条
- 本插件补充的 162 条 : 当前语言包中可查 **0/162**
  （说明汉化尚未落地到这台机器，或 Devin 更新后覆盖了语言包；下次启动 Devin 或执行 `Devin 中文: 重新应用汉化` 即可恢复）

## 4. Agent UI（webapp-host）与 DOM 层

- webapp i18next 载荷 : ❌ 未注入
- webapp 覆盖词条 : **4,575** 条
- DOM 词典 : 16,914 条（通用 9,776 + 界面 7,138）
- 注入 `workbench.html` : ✅（运行时 ✅）
- 注入 `sessions.html` : ✅（运行时 ✅）
