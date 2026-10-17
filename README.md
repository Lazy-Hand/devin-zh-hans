# devin-plugin

**Devin Desktop 插件集合。** 每个插件独立成包、独立版本、独立打包成 VSIX。

Devin Desktop 是 Cognition 从 Windsurf 演化来的 VS Code fork，因此它同时接受两套扩展机制：
标准的 VS Code 扩展（VSIX），以及它自己那套 Agent UI。这个仓库里的插件按需组合这两者。

## 插件列表

| 插件 | 说明 | 版本 | 形态 |
|---|---|---|---|
| [**zh-hans**](plugins/zh-hans) | Devin 简体中文界面 —— 编辑器外壳、命令面板、设置项，以及 Agent 侧边栏与会话窗口 | 1.0.2 | VSIX |

## 安装一个插件

```powershell
# 构建
python tools/build_vsix.py --plugin zh-hans

# 装到本机 Devin
Get-Process Devin -ErrorAction SilentlyContinue | Stop-Process -Force
& "$env:LOCALAPPDATA\Programs\Devin\bin\devin-desktop.cmd" --install-extension .\dist\devin-zh-hans-1.0.2.vsix
Remove-Item Env:\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue
Start-Process "$env:LOCALAPPDATA\Programs\Devin\Devin.exe"
```

各插件的具体安装步骤见其自身 README。

## 仓库结构

```
devin-plugin/
├── plugins/                 各插件，一个目录一个插件
│   └── zh-hans/             ← 插件本体（即 VSIX 的内容）
│       ├── package.json     扩展清单（contributes / commands / activationEvents）
│       ├── extension.js     运行时逻辑
│       ├── assets/          运行时资源（词典等）
│       ├── dist/            构建产物（DOM 翻译器）
│       ├── translations/    语言包（VS Code contributes.localizations 读取）
│       ├── README.md
│       └── CHANGELOG.md
├── shared/                  跨插件共享
│   └── dict/                人工维护的词表（Devin 专用术语）
├── tools/                   仓库级构建与分析工具
│   ├── _paths.py            统一的路径解析（Devin 安装位置 / 插件 / 数据）
│   ├── build_vsix.py        打包插件（--plugin / --all）
│   ├── analyze_nls.py       分析某个 Devin 构建的本地化缺口
│   ├── build_patch.py       由词表生成词典与语言包
│   ├── verify_integrity.py  校验 product.json.checksums 自洽性
│   └── data/                中间数据（分析结果、译文、构建日志）
├── docs/                    设计文档与实证报告
└── dist/                    打包产物（git 忽略）
```

**约定**

- `plugins/<name>/` 的内容**就是** VSIX 里 `extension/` 的内容 —— 打包器不做任何重排，所见即所得。
- 插件之间不互相依赖；共享的东西放 `shared/`，由构建期复制或由 `extension.js` 读取。
- 所有脚本通过 `tools/_paths.py` 取路径，**不写死任何用户目录**：
  Devin 安装位置自动探测，可用 `DEVIN_INSTALL` / `DEVIN_HOME` / `DEVIN_PLUGIN` 覆盖。

## 新增一个插件

```powershell
# 1. 建目录
mkdir plugins/<name>

# 2. 最小 package.json（必须字段）
#    name / displayName / description / version / publisher / engines.vscode / main
#    再按需加 contributes

# 3. 打包
python tools/build_vsix.py --plugin <name>
```

要求：

- `package.json` 必须含 `name`、`displayName`、`description`、`version`、`publisher`、`engines.vscode`
- 插件目录内提供 `README.md`（打包进 VSIX 的详情页）与 `LICENSE.txt`
- 若插件会修改 Devin 安装目录，**必须**同步更新 `product.json.checksums`，否则 Devin 会弹「安装似乎损坏」。
  `product.json.checksums` 只覆盖 11 个文件；`extensions/` 与用户目录不在其中。
- 写文件前先备份，并提供回滚路径（参考 `zh-hans/extension.js` 的 `devin-zh-backups`）

## 开发提示

```powershell
# 看某个脚本会做什么（多数脚本支持 --dry-run）
python tools/build_vsix.py --plugin zh-hans
python tools/verify_integrity.py

# 分析当前这台机器上 Devin 的汉化缺口（产出 tools/data/coverage.md）
python tools/analyze_nls.py
```

**关于 `ELECTRON_RUN_AS_NODE`**：Devin 自带的 Electron 可以当 Node 用
（`bin/devin-desktop.cmd` 就是这么跑的）。但如果你手动设置过这个变量，
再用 `Start-Process Devin.exe` 启动，Devin 会以 Node 模式运行 —— **没有窗口、exit 0**，
看起来像"补丁把软件弄坏了"。判定方法：

```powershell
& "$env:LOCALAPPDATA\Programs\Devin\Devin.exe" --version
# v24.x.x  → 中了这个坑（Node 版本）
# v3x.x.x  → 正常（应用版本）
```

## 许可

MIT，见 [LICENSE](LICENSE)。

## 免责

这些插件会修改 Devin 的本地安装文件。所有改动都有备份与回滚路径，但请自行评估风险；
本项目与 Cognition / Windsurf 无关联。
