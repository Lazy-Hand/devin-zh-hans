# 架构：为什么汉化要分四层

`plugins/zh-hans` 不是普通语言包。原因很简单：Devin Desktop 的界面由**四个互不相通的字符串来源**拼成，
任何单一机制都只能覆盖其中一部分。

## 四层与各自的覆盖面

| 层 | 覆盖 | 机制 | 生效时机 |
|---|---|---|---|
| **1. 语言包** | 菜单栏、命令面板、设置界面、活动栏、状态栏、右键菜单、对话框 | `~/.devin/argv.json` 的 `locale` + `translations/main.i18n.json` | 启动最早期 |
| **2. 扩展贡献点** | 内置 `windsurf` 扩展的 64 个命令标题、50 个设置项标题与说明（共 176 个字段） | `contributes.localizations` 的 `windsurf` bundle + `package.nls.json` | 启动早期 |
| **3. 字符串替换** | Agent UI 里少数硬编码的 JSX prop（如 `label:"Spaces"`） | 直接替换产物 bundle 里的字面量 | 窗口加载 |
| **4. DOM 翻译器** | Agent 侧边栏与会话窗口的其余文案（新建会话 / 会话 / 评审 / 自动化 / 值班 / 安全 / 知识库 / 云设置 / 空间 …） | 窗口 HTML 注入脚本 + TreeWalker + MutationObserver | 窗口加载后持续 |

## 逐层说明

### 第 1 层：语言包，补齐官方缺口

Devin 是 VS Code fork，继承完整 NLS 机制，本机已装官方简体中文语言包。
实测覆盖率：

```
全部 NLS 字符串   21,171
官方语言包已译    20,504   ← 96.8%
缺中文              667   ← 本插件补齐（其中 Devin/Windsurf 专有模块 69 个文件、316 条）
```

关键是**这 667 条无法用 `contributes.localizations` 单独提供**：VS Code 在同一 locale 下按扩展顺序
合并 `translations`，官方包 `ms-ceintl.*` 排序在后会把我们的 `vscode` bundle 盖掉。
所以扩展激活时会**把合并版（官方 21,336 + 667 = 22,003 条）直接写进已安装的官方语言包**，
无论谁先谁后都是完整版。

> 注：NLS 默认英文是**内联**在 `workbench.desktop.main.js` 里的，`out/nls.messages.json` 运行时并不加载 ——
> 所以"改 `nls.messages.json`"这条路上不通，只能走语言包。

### 第 2 层：扩展贡献点，只能改文件

内置 `windsurf` 扩展的 64 个命令 title **100% 硬编码英文**，且目录下**没有** `package.nls*.json`
（`dist/extension.js` 里 `localize` / `l10n.t` 调用数为 **0**）。语言包机制对它完全无效。

做法是把 `package.json` 里的 176 个字符串换成 `%key%`、生成英文默认值 `package.nls.json`，
再把中文放进语言包扩展的 `windsurf` bundle。

**这一层需要写安装目录，但是安全的**：`product.json.checksums` 只覆盖 11 个文件（见 `internals.md`），
`extensions/` 整个目录不在其中。

### 第 3 层：字符串替换

少数文案是 JSX 里写死的 prop，例如侧边栏分组标题 `label:"Spaces"`。这类直接替换产物 bundle 的字面量即可。
由于涉及的两个 bundle 在 `checksums` 里，替换后必须同步哈希。

### 第 4 层：DOM 翻译器，兜住最后一段

这是唯一能覆盖 Agent UI 全部文案的办法。原因见 `internals.md` 的实证部分：
Agent 侧边栏的文字**既不在 i18next 资源表里**（`useTranslation(` 调用数为 0，那张资源表是死数据），
**也不在 JS 字面量里**（`"Cloud settings"` 全树只有 1 处，改掉后界面纹丝不动）—— 它来自运行时数据。

实现：

```
往 workbench.html / sessions.html 各插一行
    <script src="./devin-zh-dom.js"></script>
+ 生成 devin-zh-dom.js（TreeWalker + MutationObserver + 19,565 条词典 + 正则规则）
+ 同步更新这两个 html 的 checksums
```

CSP 是 `script-src 'self'`，同目录外链脚本合法；Trusted Types 只约束 `innerHTML`，
翻译器只改 `nodeValue`，不触发。

**刻意不翻译**：代码编辑器、终端、**Agent 消息正文**、输入框、`[contenteditable]`、`[translate="no"]`
—— 不碰代码，也不碰用户与 Agent 的对话内容。

## 落地顺序与时序约束

```
用户装 VSIX
   ↓
第一次启动   VS Code 读语言包（还未落地）→ 界面基本中文但缺 667 条
             ↓ 启动后期扩展激活 → 落地语言包 / 注册 bundle / 注入 DOM
第二次启动   全部生效
```

语言包与窗口脚本都在启动**早期**被读取，而扩展激活在**后期**（`onStartupFinished`）。
因此首次安装需要重启一次 —— 这也是 VS Code 装语言包的固有节奏。

之后每次启动扩展都会静默自检并修复（幂等），所以 Devin 自动更新覆盖文件后不需要手动处理。

## 完整性校验的处理

`product.json.checksums` 保护 11 个文件，其中两个是我们注入的窗口 HTML。
注入后**立即同步这两个条目的哈希**（`product.json` 自身不在 checksums 内，因此自洽）。

唯一会看到「Devin 安装似乎损坏」的情况：**在 Devin 运行期间手动改过这两个 HTML** ——
此时当次启动的检查早于扩展激活，会弹一次，下次启动即恢复。

## 备份与回滚

所有写文件操作前都会备份到 `~/.devin/devin-zh-backups/<批次>/`：

| 前缀 | 来源 |
|---|---|
| `vsix-*` | 扩展自动落地 |
| `agent-ui-*` / `ui-strings-*` / `dom-inject-*` | `tools/` 下的手动脚本 |

命令面板的 `Devin 中文: 卸载汉化并回滚` 会从最近的 `vsix-*` 批次还原。
