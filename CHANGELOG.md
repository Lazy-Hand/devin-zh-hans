# Changelog

## 1.2.1

修掉一个比 1.2.0 更致命的时序 bug：**webapp 的中文资源从来没真正进入 i18next**。
界面因此出现两种症状：单词恰好被 DOM 层翻成的（安全 / 评审 / 知识库）是中文，
其余位置直接暴露**原始 i18n key**（`sidebar.automations`、`sidebar.recent`），
输入框提示行 `Tip: Hide or show the sidebar` 也保持英文。

- **根因：`addResourceBundle` 的调用时机被 init 覆盖。**
  1.2.0 注入的是 `Mt.isInitialized||Eu(), Mt.addResourceBundle("en","translation",{…})`。
  i18next 的 `initAsync` 默认 `true`，`init()` 完成时会用 `resources` 覆盖已有 bundle，
  于是后加的中文被吃掉 —— 文件里载荷完整、验证脚本全绿，界面却是原始 key。
- **改为合并进 `resources` 对象本身。** `mu` 就是英文资源（`mu=yl`），
  在 `Mt.isInitialized||Eu()` **之前**插 `Object.assign(mu||{}, 中文)`，
  中文直接成为 `init({resources})` 的一部分，与英文同源同寿命，不依赖任何时序。
- **修掉尾逗号导致的语法错误。** 锚点后原本有逗号，插在锚点前再拼接会留下
  `…,Mt.isInitialized||Eu(),}`，整个 chunk 语法错误、Devin 起不来。已收敛并加断言。
- **验证从「文件里有载荷」升级到「i18next 真的能查到」。**
  新增 `tools/test_runtime_merge.js`：真实执行注入语句、模拟 `t()` 查找，
  9 条断言覆盖截图里出问题的每一处；已接入 `verify_integrity.py`。
  `verify_layers.js` 增加三条硬断言：
  `载荷位于初始化锚点之前`、`不是 addResourceBundle 形态`、`锚点后无残留尾逗号`。
- **DOM 层加兜底巡检。** 会话列表的相对时间由 `Intl.RelativeTimeFormat` 生成、
  且会被 React 复用节点重新水合，`MutationObserver` 偶尔收不到。
  启动后 60 秒内每 2 秒补扫一次（已是中文的节点被 CJK 短路，开销接近零）。
- `.backup`（2.2 MB 原始 chunk）不再打进 VSIX。

## 1.2.0

修掉三个让汉化「装了却几乎看不见效果」的实质性 bug。菜单栏与侧边栏在 1.1.x 已生效，
但设置页、输入框提示、会话时间这些要么整片英文，要么译错。

- **修复：webapp i18next 载荷用了扁平 key，一条都匹配不到。**
  Devin 的 en 资源是**嵌套命名空间**结构（`yl={composerTips:ma, nav:$a, …}`），
  i18next 查的是 `composerTips.newSession`。1.1.x 用正则 `key: 值` 扫出 4,575 个扁平 key
  并注入成 `{"newSession": …}`，命中率为 0。改为结构化解析建出真实的树：
  **317 个命名空间 / 19,269 个 key**。`tools/extract_webapp_i18n.js`。
- **修复：漏掉了 `JSON.parse(\`…\`)` 内联资源。**
  设置页那一大片文案（`settings` 命名空间 **3,938 个 key**）是内联 JSON 字符串，
  不是对象字面量，整个没被扫到 —— 这就是截图里「外观 / 语言 / 通知」整页英文的原因。
  解析器现在同时处理两种写法，并修正模板字符串 → JSON 的转义层级（`\"` 与 `\u`）。
- **修复：DOM 词典用 NLS key 建表而不是英文原文。**
  `desktopShell.goBack` 这种 key 永远不会出现在界面文本里。改为从
  `nls.keys.json`（顺序）+ `nls.messages.json`（值）反查英文原文，配
  `tools/dict/ui-common-zh.json` 人工校订层处理一词多义
  （`Forward` 前进 vs 转发、`Review` 评审 vs 审阅、`View` 视图 vs 查看）。
- **修复：官方语言包把 Devin 译成了别的品牌。**
  官方 zh-hans 是给 VS Code 做的：`Devin Console` → "VS Code 控制台"、
  `Restart Devin` → "重新启动 VS Code"、`mcp.discovery.source.windsurf` → "Windsurf"。
  新增 `tools/data/zh/g8-brand.json`，只回正「英文原文里没有 VS Code/Windsurf、
  译文里却有」的 **59** 条 —— 无歧义才改。
- **修复：相对时间不经过 i18n。** `yesterday` / `3 days ago` 由
  `Intl.RelativeTimeFormat(locale)` 生成，查不到 key。DOM 层新增 36 条正则规则
  覆盖秒/分/时/天/周/月/年与 `in N x`、`yesterday/today/tomorrow/just now`。
- **验证加强：断言载荷 key 真能查到。** 之前只检查「载荷存在」，所以上面那些 bug 全漏了。
  现在 `verify_layers.js` 会解析载荷、逐 key 比对 en 资源树，并抽查实际条目：
  `载荷 key 命中率 100.0%（11413/11413）`。
- 数据：webapp 覆盖从 6,576 → **11,413** 条（309 个命名空间）；
  DOM 词典 16,518 → **20,220** 条；新增设置页译文 2,444 条。

## 1.1.0

适配 **Devin 3.11.216**（`windsurfVersion` 3.10.67 → 3.11.216）。这次更新换了 Agent UI 的实现，
所以不是「补几条词」而是新增一层。

- **新增第 3 层：Agent UI 的 i18next 覆盖。**
  Devin 3.11 起 Agent 侧边栏由 `out/vs/workbench/devin-webapp-host/`（约 91 MB、1,800+ chunk）
  承担，由 `workbench.desktop.main.js` 用 `import("@devin/webapp-host")` 挂进 workbench 渲染进程。
  它自带 i18next 与 en/ja/pt/es 四份资源，**没有中文**。本插件沿用 Devin 自己的实例，
  在 `Mt.isInitialized||Eu()` 后追加 `addResourceBundle("en","translation",{…})`。
  不新增 locale、不改 `lng`、不动组件代码。
- **重做第 2 层：内置扩展从 1 个扩到 5 个。**
  新增 `windsurf-dev-containers` / `windsurf-remote-devin` / `windsurf-remote-openssh` /
  `windsurf-remote-wsl`，字段数 176 → **254**。改为写 `package.nls.json` +
  `package.nls.zh-cn.json` 走 VS Code 自己的 `getLocalizedMessages` 路径。
- **语言包补齐新版缺口。** 新增 162 条译文（`tools/data/zh/g6.json`），
  主要是新的桌面壳菜单栏（55 条 `&&` 加速键）、Devin Cloud 保存通知（24 条）、
  webapp 命令与 ACP 远程主机（17 + 6 条）、SSH 会话窗口等。
  同时用当前构建的 `nls.keys.json` **剔除 1,004 条死条目**，合并版 22,003 → **21,161** 条。
- **完整性校验从 11 项变 12 项**（新版多了 `vs/workbench/devin-webapp-host/index.js`）。
  同步逻辑改为遍历全部条目，不再写死。
- **提升可验证性。** 新增 `tools/verify_layers.js`：给 `extension.js` 喂假 `vscode` 模块，
  在 `resources/app` 的沙盒副本上跑真实落地逻辑并断言，验证幂等（第二次零写入）。

## 1.0.2

- 修复：不再删除 `languagepacks.json`（那会让 VS Code 到下一次启动才重建，用户得多重启一次），
  改为直接把 `windsurf` bundle 条目补进清单。
- 修复：不再伪造 `languagepacks.json` 的 hash —— VS Code 用它作 `clp/<hash>.<locale>`
  缓存目录名，伪造值会导致启动时 `scandir` 一个不存在的目录并抛 ENOENT。
- 安装提示更明确：告知需要重启一次才能完全生效。

## 1.0.1

- 修复 `languagepacks.json` hash 被伪造导致的 clp 目录 ENOENT。

## 1.0.0

- 首个版本：语言包（22,003 条）+ `windsurf` 扩展贡献点（176 条）+ 窗口级 DOM 翻译器（19,565 条词典）。
- 覆盖编辑器外壳、命令面板、设置项，以及 Agent 侧边栏与会话窗口。
