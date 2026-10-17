# Devin 简体中文

为 **Devin Desktop**（VS Code fork）提供完整简体中文界面。

## 下载

**[⬇ 下载最新版 devin-zh-hans.vsix](https://github.com/klarkxy/devin-zh-hans/releases/latest/download/devin-zh-hans.vsix)**
　·　[全部版本](https://github.com/klarkxy/devin-zh-hans/releases)　·　[更新日志](CHANGELOG.md)

安装：

```powershell
# 关闭 Devin
Get-Process Devin -ErrorAction SilentlyContinue | Stop-Process -Force

# 安装（文件名固定，链接永远指向最新版）
& "$env:LOCALAPPDATA\Programs\Devin\bin\devin-desktop.cmd" --install-extension .\devin-zh-hans.vsix

# 启动（不要带 ELECTRON_RUN_AS_NODE）
Remove-Item Env:\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue
Start-Process "$env:LOCALAPPDATA\Programs\Devin\Devin.exe"
```

> 首次安装后**重启一次** Devin 才会完全生效 —— 语言包与窗口脚本在启动早期被读取，
> 而扩展激活在启动后期。此后每次启动都是中文。

覆盖范围：

| 层级 | 覆盖内容 | 机制 |
|---|---|---|
| 编辑器外壳 | 菜单栏、命令面板、设置界面、侧边栏、状态栏、右键菜单、对话框 | VS Code 官方语言包机制 |
| 内置扩展 | `windsurf` 扩展的 64 个命令标题、设置项标题与说明（176 个字段） | `contributes.localizations` 的 `windsurf` bundle |
| Agent UI | Agent 侧边栏与会话窗口（新建会话 / 会话 / 评审 / 自动化 / 值班 / 安全 / 知识库 / 云设置 / 空间 / 自定义 …） | 窗口级 DOM 翻译器 |

## 安装

```powershell
# 关闭 Devin
Get-Process Devin -ErrorAction SilentlyContinue | Stop-Process -Force

# 安装
& "$env:LOCALAPPDATA\Programs\Devin\bin\devin-desktop.cmd" --install-extension .\devin-zh-hans-1.0.2.vsix

# 启动（注意：不要带 ELECTRON_RUN_AS_NODE 环境变量）
Remove-Item Env:\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue
Start-Process "$env:LOCALAPPDATA\Programs\Devin\Devin.exe"
```

**首次安装后需要重启一次 Devin。** 扩展要到第一次启动时才会落地注入，而语言包与窗口脚本都在启动更早的阶段被读取 ——
所以「装完 → 启动 → 再启动一次」是完全生效的最短路径。此后每次启动都是中文。

若界面语言仍是英文，执行命令面板（`Ctrl+Shift+P`）里的 **`Devin 中文: 查看汉化状态`** 检查，或运行 **`Devin 中文: 重新应用汉化`**。

## 自动化行为

扩展每次启动都会静默自检并修复，全程幂等：

| 检查项 | 行为 |
|---|---|
| 合并版语言包被 Devin 更新覆盖 | 自动重写 |
| `windsurf` bundle 未注册 | 写进语言包清单，并补进 `languagepacks.json` |
| 窗口脚本或 `<script>` 标签被覆盖 | 自动重写并重新注入 |
| `product.json.checksums` 与文件不符 | 自动同步为自洽 |

因此 **Devin 自动更新后无需手动处理**，下次启动会自己恢复。

## 命令

| 命令 | 作用 |
|---|---|
| `Devin 中文: 查看汉化状态` | 显示语言包条数、DOM 注入状态、完整性校验自洽情况 |
| `Devin 中文: 重新应用汉化` | 重新落地所有汉化（幂等，Devin 更新后用它恢复） |
| `Devin 中文: 卸载汉化并回滚` | 从备份还原到安装前状态 |

## 原理

这个扩展不是纯语言包，而是**语言包 + 落地器**两段式：

**1. 语言包层**

扩展自带合并版 `translations/main.i18n.json`（官方 21,336 条 + 本插件补充的 667 条 Devin/Windsurf 专有文案 = **22,003 条**）。

之所以要"落地"而不是只靠 `contributes.localizations`：VS Code 在同一 locale 下按扩展顺序合并 `translations`，官方语言包 `ms-ceintl.*` 排序在后时会把我们的 `vscode` bundle 盖掉。所以激活时会把合并版直接写进已安装的官方语言包，无论谁先谁后都是完整版。

**2. DOM 层**

Agent 侧边栏的文案既**不在 i18next 资源表**里（实测 `useTranslation(` 调用数为 **0**，资源表是死数据），也**不在 JS 字面量**里 —— 只有少数硬编码项可本地替换。因此只能由 `dist/devin-zh-dom.js` 在窗口里做 DOM 级替换：

- 往 `workbench.html` / `sessions.html` 各注入一行 `<script src="./devin-zh-dom.js">`
  （CSP 是 `script-src 'self'`，同目录外链脚本合法；Trusted Types 只约束 `innerHTML`，翻译器只改 `nodeValue`，不触发）
- TreeWalker + MutationObserver，词典 19,565 条 + 4 条正则
- 只改文本节点，不动 React 状态与事件

**3. 完整性校验**

`workbench.html` / `sessions.html` 在 `product.json.checksums` 的 11 个受保护文件里，所以注入后会**同步更新这两个条目的哈希**。实测 11 项全部自洽 → **不会出现「Devin 安装似乎损坏」**。

## 刻意不翻译的区域

代码编辑器、终端（`.monaco-editor` / `.xterm` / `.cm-editor`）、
**Agent 消息正文**（`[data-transcript-row-key]` / `[data-testid*="message-content"]` / `.prose` / `[data-streamdown]`）、
输入框、`[contenteditable]`、`[translate="no"]`。

保证不碰代码，也不碰你和 Agent 的对话内容。

## Devin 更新后

自动更新会覆盖 `resources/app`。扩展下次激活时会检测到并**自动重新注入**；
如果没自动恢复，运行 **`Devin 中文: 重新应用汉化`** 即可。

## 关于「Devin 安装似乎损坏」提示

`product.json.checksums` 保护 11 个文件，其中两个正是我们注入的窗口 HTML（`workbench.html`、`sessions.html`）。
一旦这两个文件与清单中的哈希不一致，Devin 启动时会弹该提示。

- 正常使用**不会**出现：扩展注入后立即同步哈希（实测 11 项全部自洽）。
- 唯一例外是**注入时机**：注入发生在扩展激活时（启动后期），而完整性检查在启动早期。
  所以如果你在 Devin 运行期间手动改过这两个 HTML，**当次**启动会弹一次，下次启动即恢复。
- 想确认是否健康：运行 `Devin 中文: 查看汉化状态`，看到 `完整性校验自洽 11 / 11 ✓` 即可。

## 已知边界

- 少数文案仍是英文：`2 MCP servers`（React 把文本拆成多个节点，整串匹配不到）、配额提示条（模板被拆分且日期由表达式拼接）、输入框区域的 `Local` / `Devin Local`。
  补法：往 `assets/ui-strings-zh.json` 加词条后重新打包。
- Monaco 编辑器内部渲染文本不翻译（canvas 双渲染，也不应翻译）。
- 跨域 iframe（内嵌的 `app.devin.ai`）不在注入范围内。
- macOS 未验证：本插件按 Windows 安装树（`%LOCALAPPDATA%\Programs\Devin`）编写。

## 回滚

```powershell
& "$env:LOCALAPPDATA\Programs\Devin\bin\devin-desktop.cmd" --uninstall-extension devin-zh.devin-zh-hans
```

或使用命令面板里的 `Devin 中文: 卸载汉化并回滚`（会从 `~/.devin/devin-zh-backups/vsix-*` 还原）。

## 许可

MIT。语言包内含 Microsoft 官方 zh-hans 译文（MIT 许可）。
