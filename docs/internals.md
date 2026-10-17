# Devin Desktop 内部机制与实证记录

这份文档记录逆向/实测得到的事实，以及几条**导致错误结论的坑**。所有结论都标注了证据来源。

## 1. Devin Desktop 的身份

**它是 Windsurf（Exafunction / Codeium）改名而来的 VS Code fork。**

证据来自本机 Devin 1.126.0 的 `resources/app/product.json`：

```
nameShort        : "Devin"
applicationName  : "devin-desktop"
oldNameShort     : "Windsurf"          ← 改名痕迹
oldDataFolderName: ".windsurf"
oldUrlProtocol   : "windsurf"
licenseName      : "MIT"
codeiumVersion   : "1.48.2"
windsurfVersion  : "3.10.67"
author           : Exafunction, Inc.
extensionsGallery: marketplace.windsurf.com
```

因此它同时具备两套扩展机制：标准 VS Code 扩展（VSIX）+ 自己的 Agent UI。

## 2. 相关目录

| 路径 | 内容 |
|---|---|
| `%LOCALAPPDATA%\Programs\Devin\` | 安装树（**未打包成 asar**，`resources/app` 是明文目录） |
| `…\resources\app\out\` | 编译产物（workbench / sessions / extensions） |
| `…\resources\app\node_modules\@exa\chat-client\index.js` | **真正被加载的 Agent chat-client（25 MB）** |
| `…\bin\devin-desktop.cmd` | CLI，等价于 VS Code 的 `code` —— `--install-extension` 可用 |
| `%USERPROFILE%\.devin\argv.json` | 启动参数（`locale` 在这里） |
| `%USERPROFILE%\.devin\extensions\` | 用户扩展与语言包 |
| `%APPDATA%\devin\languagepacks.json` | 语言包缓存索引（**不要伪造它的 hash**，见坑 2） |
| `%APPDATA%\devin\logs\<时间戳>\` | 日志（`main.log` / `exthost.log` / `renderer.log`） |

## 3. NLS（界面字符串）机制

`out/nls.keys.json` 的结构是 `[[源文件, [key...]], ...]`（1,797 个源文件），
`out/nls.messages.json` 是与之**顺序一一对应**的展平英文数组（21,220 条）。
两者的长度一致，可用来精确还原每个 key 的默认英文。

**关键**：`workbench.desktop.main.js` 里对 `nls.messages.json` 的引用次数是 **0**
—— 英文默认值是**内联**在 bundle 里的，运行时并不读那个 json。
所以"改 `nls.messages.json` 让界面变中文"这条路**不通**，只能走语言包。

覆盖率实测见 [coverage.md](coverage.md)：21,171 条中官方语言包覆盖 20,504 条（96.8%），缺 667 条。

## 4. 完整性校验的确切范围

`out/vs/workbench/workbench.desktop.main.js` 里的实现（反混淆后）：

```js
async _isPure(){
  let i = this.productService.checksums || {};        // ← 只取 product.json 的 checksums
  await this.lifecycleService.when(4);
  let e = await Promise.all(Object.keys(i).map(o => this._resolve(o, i[o])));
  //                ^^^^^^^^^^^^^^ 只遍历这 11 个键
  ...
}
async _resolve(i, e){ ... this.checksumService.checksum(uri) ... }
_createChecksumPair(i, e, t){ return { uri:i, actual:e, expected:t, isPure: e===t } }
_showNotification(){ ... }        // ← 失败只弹通知，不阻止启动
```

结论：

- 校验范围**就是** `product.json.checksums` 那 11 个文件，**不含** `extensions/`，也不含用户目录；
- 哈希算法是 `base64(sha256(file))` 去掉 `=` 填充；
- 校验失败**只弹通知**，不阻止启动。

受保护的 11 个文件：

```
vs/base/parts/sandbox/electron-browser/preload.js
vs/workbench/workbench.desktop.main.js
vs/workbench/windsurf-chat-client/index.js
vs/workbench/workbench.desktop.main.css
vs/workbench/api/node/extensionHostProcess.js
vs/code/electron-browser/workbench/workbench.html        ← 我们注入 DOM 脚本
vs/code/electron-browser/workbench/workbench.js
vs/sessions/sessions.desktop.main.js
vs/sessions/sessions.desktop.main.css
vs/sessions/electron-browser/sessions.html               ← 我们注入 DOM 脚本
vs/sessions/electron-browser/sessions.js
```

`node_modules/@exa/chat-client/index.js` **不在**清单里，改它无需同步哈希。

## 5. Agent UI 的 i18n 真相

这是本项目最反直觉的一段。Agent 侧边栏（新建会话 / 会话 / 评审 / …）实测**改不动**，排查链路：

| 检查 | 结果 | 推论 |
|---|---|---|
| `sessions.desktop.main.js` / `chat-client/index.js` 里的 i18next 资源表 | 确实存在 `"nav":{"newSession":"New session",...}` | 看起来该走 i18n |
| 深合并入口 `englishOverrides:JSON.parse('...')` | 存在且**全局唯一**，注入后文件确认变大 | 界面**无任何变化** |
| `useTranslation(` 在 bundle 里的调用数 | **0 次** | React 组件**根本没用 i18next**，资源表是死数据 |
| `nav.` 作为 i18n key 的出现次数 | **0 次** | 同上 |
| `"Cloud settings"` 全 `resources/app` 树出现次数 | **仅 1 处**（在死资源表里） | 界面显示它却改不动 → 文案来自**运行时数据** |
| `Spaces` 的形态 | `label:"Spaces"`（硬编码 JSX prop） | 这类**能**改，实测生效 |

顺带确认：这两个 bundle 里确实带西班牙语、日语资源（`nav.agent:"エージェント"`），
说明 i18n 机制本身是通的，只是**没有中文**且 `lng` 硬编码 `"en"` —— 但即使把中文塞进资源表也无效，
因为根本没有组件去读它。

**结论**：Agent 侧边栏文案只能在 DOM 层拦截。

## 6. 三个坑

### 坑 1：`ELECTRON_RUN_AS_NODE` 会让 Devin 变成 Node，然后静默退出

`bin/devin-desktop.cmd` 用 `set ELECTRON_RUN_AS_NODE=1` + `Devin.exe out/cli.js` 实现 CLI。
用这个变量跑完脚本后如果没清掉，再 `Start-Process Devin.exe` 启动的其实是 **Node 进程**：

- 进程列表里没有 Devin（或一闪而过）
- 日志目录不新建
- **exit code 0**（正常退出，不报错）

表现和"补丁破坏了完整性校验导致软件拒绝启动"一模一样。判定：

```powershell
& "$env:LOCALAPPDATA\Programs\Devin\Devin.exe" --version
# v24.x.x  → 中了这个坑（Node 版本）
# v3x.x.x  → 正常（应用版本）
```

### 坑 2：不要伪造 `languagepacks.json` 的 hash

VS Code 用 `clp/<hash>.<locale>` 作为语言包缓存目录名。
把 hash 改成自定义值（本意是"强制重建"）会让它在启动时 `scandir` 一个不存在的目录：

```
ENOENT: no such file or directory, scandir
  '…\AppData\Roaming\Devin\clp\devin-zh-1792211331252.zh-cn'
```

正确做法：**只补 `translations` 条目，不动 hash**。
因为 hash 只由「语言包扩展 id + 版本」决定、不含 bundle 列表，补条目不会让它失配。

### 坑 3：不要用"启动一次看进程在不在"判断补丁安全性

排查过程中一度据此得出"改 `extensions/windsurf/package.json` 会触发字节级哈希校验"的结论，
并写进了文档 —— **是错的**。后来做基线测试才推翻：**完全未打补丁的原始状态同样启动不起来**，
原因是坑 1 的环境变量残留。

教训：启动本身受单实例锁、更新检查、环境变量等多因素影响，**单点采样会得出错误结论**。
要么读代码（如第 4 节那样），要么固定全部变量做多次采样。

另一个相关的误判：一次"读入 JSON → 原样写回"（值一个都没改，只有格式变化）也被当成了校验证据，
实际上那次运行同样受环境变量干扰。

## 7. Devin 的自动更新

安装树由 Inno Setup 维护（`unins000.exe`），自动更新会覆盖 `resources/app`。
被覆盖的是第 2/3/4 层（扩展贡献点、bundle 字符串、窗口注入），
第 1 层的语言包在用户目录、通常保留。

因此插件的 `extension.js` 每次启动都做幂等自检，四项全部自动修复。
