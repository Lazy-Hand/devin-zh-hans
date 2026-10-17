# Changelog

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