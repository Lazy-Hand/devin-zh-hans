# Changelog

## 1.1.0

适配 **Devin 3.11.216**（`windsurfVersion` 3.10.67 → 3.11.216）。这次更新换了 Agent UI 的实现，
所以不是「补几条词」而是新增一层。

- **新增第 3 层：Agent UI 的 i18next 覆盖。**
  Devin 3.11 起 Agent 侧边栏由 `out/vs/workbench/devin-webapp-host/`（约 91 MB、1,800+ chunk）
  承担，由 `workbench.desktop.main.js` 用 `import("@devin/webapp-host")` 挂进 workbench 渲染进程。
  它自带 i18next 与 en/ja/pt/es 四份资源，**没有中文**。本插件沿用 Devin 自己的实例，
  在 `Mt.isInitialized||Eu()` 后追加 `addResourceBundle("en","translation",{…})`，
  按英文 key 把 **4,575** 条中文深合并进 `en`。不新增 locale、不改 `lng`、不动组件代码。
- **重做第 2 层：内置扩展从 1 个扩到 5 个。**
  新增 `windsurf-dev-containers` / `windsurf-remote-devin` / `windsurf-remote-openssh` /
  `windsurf-remote-wsl`，字段数 176 → **254**。改为写 `package.nls.json` +
  `package.nls.zh-cn.json` 走 VS Code 自己的 `getLocalizedMessages` 路径，
  不再依赖注册语言包 bundle。
- **语言包补齐新版缺口。** 新增 162 条译文（`tools/data/zh/g6.json`），
  主要是新的桌面壳菜单栏（55 条 `&&` 加速键）、Devin Cloud 保存通知（24 条）、
  webapp 命令与 ACP 远程主机（17 + 6 条）、SSH 会话窗口等。
  同时用当前构建的 `nls.keys.json` **剔除 1,004 条死条目**（官方语言包自带的、
  本构建已不存在的 key），合并版从 22,003 → **21,161** 条，全部可查。
- **DOM 词典扩容。** 19,565 → **25,999** 条（新增 webapp 专有文案 7,056 条），
  正则规则 4 → 22 条（相对时间、计数短语、`Tip:` 等模板）。
  跳过规则更新到新版 DOM 结构：新增 `[data-slate-node]`、`[data-devin-input-box]`、
  `.markdown-body`、`.cm-content`，并加 CJK 短路（已含中文的节点不再处理）。
- **完整性校验从 11 项变 12 项**（新版 `product.json.checksums` 多了
  `vs/workbench/devin-webapp-host/index.js`）。同步逻辑改为遍历全部条目，不再写死。
- **提升可验证性。** 新增 `tools/verify_layers.js`：给 `extension.js` 喂假 `vscode` 模块，
  在 `resources/app` 的沙盒副本上跑真实落地逻辑并断言四层状态，验证幂等（第二次零写入）。
  沙盒通过 `DEVIN_INSTALL` / `DEVIN_HOME` 环境变量指向，不写系统目录。
- 删除被取代的 `tools/patch_dom_inject.py`、`patch_agent_ui.py`、`patch_ui_strings.py`
  与 `assets/windsurf.en2key.json`、`assets/windsurf.package.nls.json`（新路线不再需要值替换表）。

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
