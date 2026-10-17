# tools

仓库级工具。所有脚本通过 [`_paths.py`](_paths.py) 解析路径，**不写死任何用户目录**。

## 路径解析

| 环境变量 | 用途 | 默认 |
|---|---|---|
| `DEVIN_INSTALL` | Devin 安装根目录（含 `Devin.exe`） | 依次探测 `%LOCALAPPDATA%\Programs\Devin`、`C:\Program Files\Devin` |
| `DEVIN_HOME` | Devin 用户目录 | `~/.devin` |
| `DEVIN_PLUGIN` | 操作哪个插件 | `zh-hans` |

`DEVIN_INSTALL` 探测失败时，依赖安装目录的脚本会明确报错而不是静默失败。

## 脚本

### `build_vsix.py` — 打包

```powershell
python tools/build_vsix.py                  # 打包 plugins/zh-hans
python tools/build_vsix.py --plugin <name>
python tools/build_vsix.py --all            # 打包全部插件
python tools/build_vsix.py --out dist       # 指定产物目录
```

`plugins/<name>/` 的内容**原样**成为 VSIX 里的 `extension/`，不做任何重排。
打包时排除 `CHANGELOG.md`、`node_modules/`、`__pycache__/`。

### `analyze_nls.py` — 分析本地化缺口

扫描当前这台机器上 Devin 的 `out/nls.keys.json` 与语言包，输出：

- `data/coverage.md` — 覆盖率报告（按源文件聚合、Devin 专有模块清单、样例）
- `data/missing.json` — 完整缺口清单（`{file, key, en}`）
- `data/todo.json` — 按源文件分组的待译清单

用于判断一次 Devin 更新引入了多少新字符串。

### `build_patch.py` — 由词表生成产物

读 `data/todo.json` + `data/zh/g*.json`（译文），产物直接写进插件：

```
plugins/<name>/translations/main.i18n.json              合并版语言包（官方 + 补充）
plugins/<name>/translations/extensions/windsurf.i18n.json
plugins/<name>/assets/ui-dict.json                      DOM 翻译器词典
plugins/<name>/assets/windsurf.*.json                   windsurf 扩展本地化映射
```

**前提**：本机已安装官方简体中文语言包（合并版的底子来自它）。
版本不匹配时脚本会提示，此时应先跑 `analyze_nls.py` 重新对齐。

### `verify_integrity.py` — 完整性自检

检查三件事，是"不会触发告警"这一声明的证据来源：

1. `product.json.checksums` 的 11 个文件实际哈希是否自洽
2. `%key%` 占位符是否都能在 `package.nls.json` 解析、且都有中文
3. 语言包 bundle 注册状态与译文可查性

输出 `data/verify-report.md`。

### `devin-ui-tool.js` — Agent UI 的 CDP 工具（可选）

DOM 层已由插件的 `devin-zh-dom.js` 覆盖，这个工具用于**扩充词典**：

```powershell
# 带调试端口启动 Devin（需先完全退出）
& "$env:LOCALAPPDATA\Programs\Devin\Devin.exe" --remote-debugging-port=9222
# 抓取当前界面上词典还没覆盖的英文
node tools/devin-ui-tool.js --extract --out new-strings.json
```

把新词条译好后并入 `shared/dict/ui-strings-zh.json`，重跑 `build_patch.py`。

> 注意：本机 Devin 3.10.67 实测**不接受** `--remote-debugging-port`（端口不监听），
> 此工具在能接受该参数的版本上才可用。词典也可以直接用 `--extract` 之外的途径手工补充。

## 数据目录 `data/`

| 文件 | 说明 |
|---|---|
| `todo.json` / `missing.json` | 分析结果（可重新生成） |
| `zh/g1..g4.json` | NLS 缺口的译文，格式 `{"English": "中文"}` |
| `zh/g5.json` | windsurf 扩展贡献点的译文，格式 `{"<id>": "中文"}` |
| `coverage.md` / `verify-report.md` | 报告产物 |
| `meta.json` / `build.log` | 构建元信息与日志 |

这些是**生成物的输入**，因此提交进仓库以保证可复现；`dist/` 才是被忽略的产物目录。
