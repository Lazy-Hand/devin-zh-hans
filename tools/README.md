# tools

仓库级工具。所有脚本通过 [`_paths.py`](_paths.py) 解析路径，**不写死任何用户目录**。

本仓库只维护一个插件，**仓库根目录就是插件根目录**，所以脚本里没有「插件选择」这类参数。

## 路径解析

| 环境变量 | 用途 | 默认 |
|---|---|---|
| `DEVIN_INSTALL` | Devin 安装根目录（含 `Devin.exe`） | 依次探测 `%LOCALAPPDATA%\Programs\Devin`、`C:\Program Files\Devin` |
| `DEVIN_HOME` | Devin 用户目录 | `~/.devin` |
| `DEVIN_PLUGIN_REPO` | 发布目标仓库 | `klarkxy/devin-zh-hans` |

关键目录：

| 位置 | 说明 |
|---|---|
| `./`（仓库根） | 插件本体：`package.json` / `extension.js` / `assets/` / `dist/` / `translations/` |
| `tools/data/` | 中间数据（分析结果、译文、构建日志），会提交 |
| `tools/dict/` | 人工维护的词表，会提交 |
| `build/` | VSIX 打包输出，**被 git 忽略** |

## 脚本

### `build_vsix.py` — 打包

```powershell
python tools/build_vsix.py              # 输出到 build/
python tools/build_vsix.py --dry-run    # 只列出会打包哪些文件
```

把仓库根下**属于插件的那部分**塞进 VSIX 的 `extension/`，仓库级目录（`tools/`、`docs/`、`.github/`、`build/` 等）一律排除。
`dist/` 是插件自带的运行时文件（DOM 翻译器），**必须提交**，不要和打包产物 `build/` 混淆。

### `release.py` — 发布

```powershell
python tools/release.py             # 按 package.json 的 version 发布
python tools/release.py --dry-run
python tools/release.py --status    # 看当前发布状态与下载入口
```

发布时创建 tag `v<version>`，并上传**两个** asset：

| asset | 用途 |
|---|---|
| `devin-zh-hans-1.0.2.vsix` | 带版本号，用于归档与「我要指定版本」 |
| `devin-zh-hans.vsix` | **固定名**，每次发版覆盖 |

固定名是为了这条 URL 永久有效：

```
https://github.com/klarkxy/devin-zh-hans/releases/latest/download/devin-zh-hans.vsix
```

GitHub 的 `releases/latest/download/<asset>` 会解析到「最新正式 release 的那个 asset」，
所以只要 asset 名不变，链接就永远指向最新版 —— README 里放的就是它。

### `analyze_nls.py` — 分析本地化缺口

扫描当前这台机器上 Devin 的 `out/nls.keys.json` 与语言包，输出：

- `data/coverage.md` — 覆盖率报告（按源文件聚合、Devin 专有模块清单、样例）
- `data/missing.json` — 完整缺口清单 `{file, key, en}`
- `data/todo.json` — 按源文件分组的待译清单

用于判断一次 Devin 更新引入了多少新字符串。输出到 `data/coverage.md`（原名 `report.md`）。

### `build_patch.py` — 由词表生成产物

读 `data/todo.json` + `data/zh/g*.json`（译文），产物直接写进仓库根：

```
translations/main.i18n.json              合并版语言包（官方 + 补充）→ 22,003 条
translations/extensions/windsurf.i18n.json
assets/ui-dict.json                      DOM 翻译器词典
assets/windsurf.en2key.json              值替换表
assets/windsurf.package.nls.json         windsurf 扩展英文默认值
```

**前提**：本机已安装官方简体中文语言包（合并版的底子来自它）。

**注意一个坑**：本脚本从「当前安装目录」的 `windsurf/package.json` 提取字段，但插件装过之后那个文件
已经被换成 `%key%` 了，提取结果会从 176 个字段降到 112 个。所以脚本会**与已有产物合并**并打印提示，
不会把仓库里的完整产物写坏。若要得到与仓库完全一致的产物，请在未打补丁的 Devin 上运行。

### `verify_integrity.py` — 完整性自检

检查三件事，是「不会触发告警」这一声明的证据来源：

1. `product.json.checksums` 的 11 个文件实际哈希是否自洽
2. `%key%` 占位符是否都能在 `package.nls.json` 解析、且都有中文
3. 语言包 bundle 注册状态与译文可查性

输出 `data/verify-report.md`。

### `devin-ui-tool.js` — Agent UI 的 CDP 工具（可选）

DOM 层已由 `dist/devin-zh-dom.js` 覆盖，这个工具用于**扩充词典**：

```powershell
# 带调试端口启动 Devin（需先完全退出）
& "$env:LOCALAPPDATA\Programs\Devin\Devin.exe" --remote-debugging-port=9222
node tools/devin-ui-tool.js --extract --out new-strings.json
```

把新词条译好后并入 `tools/dict/ui-strings-zh.json`，重跑 `build_patch.py`。

> 本机 Devin 3.10.67 实测**不接受** `--remote-debugging-port`（端口不监听），
> 该工具只在接受此参数的版本上可用。

## 数据目录 `data/`

| 文件 | 说明 |
|---|---|
| `todo.json` / `missing.json` | 分析结果（可重新生成） |
| `zh/g1..g4.json` | NLS 缺口的译文，格式 `{"English": "中文"}` |
| `zh/g5.json` | windsurf 扩展贡献点的译文，格式 `{"<id>": "中文"}` |
| `coverage.md` / `verify-report.md` | 报告产物 |
| `meta.json` / `build.log` | 构建元信息与日志 |

## 发版流程

```powershell
# 1. 改版本号（同时更新 CHANGELOG.md）
#    package.json 的 version

# 2. 本地验证
python tools/build_vsix.py
python tools/release.py --dry-run

# 3. 提交并打 tag
git add -A; git commit -m "release: v1.0.3"
git tag v1.0.3; git push; git push --tags

# 4. CI 会自动构建并发布（.github/workflows/build.yml）
#    也可以本地手动发：
python tools/release.py
```

CI 会校验 **tag 与 `package.json` 的版本一致**，不一致直接失败。
