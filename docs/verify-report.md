## 1. product.json 完整性校验（补丁后重新计算）

| 结果 | 受保护文件 |
|---|---|
| ✅ 一致 | `vs/base/parts/sandbox/electron-browser/preload.js` |
| ✅ 一致 | `vs/workbench/workbench.desktop.main.js` |
| ✅ 一致 | `vs/workbench/windsurf-chat-client/index.js` |
| ✅ 一致 | `vs/workbench/workbench.desktop.main.css` |
| ✅ 一致 | `vs/workbench/api/node/extensionHostProcess.js` |
| ✅ 一致 | `vs/code/electron-browser/workbench/workbench.html` |
| ✅ 一致 | `vs/code/electron-browser/workbench/workbench.js` |
| ✅ 一致 | `vs/sessions/sessions.desktop.main.js` |
| ✅ 一致 | `vs/sessions/sessions.desktop.main.css` |
| ✅ 一致 | `vs/sessions/electron-browser/sessions.html` |
| ✅ 一致 | `vs/sessions/electron-browser/sessions.js` |

**结论：全部 11 个受保护文件哈希与原始值完全一致 → 不会触发“Devin 安装似乎损坏”告警**

## 2. windsurf 扩展 %key% 占位符可解析性

- package.json 中的 %key% 占位符 : **66** 个
- package.nls.json 提供英文默认值 : **176** 条
- 无法解析（会原样显示 %key%）  : **0** ✅
- windsurf.i18n.json 提供中文译文  : **176** 条
- 缺中文（会回落英文）            : **0** ✅

### 抽样对照

| key | 英文默认 | 中文 |
|---|---|---|
| `devin.cmd.devin.cascade.toggleAgentSelector.title` | Switch Agent | 切换智能体 |
| `devin.cmd.devin.copyApiKey.title` | Copy API Key to Clipboard | 复制 API 密钥到剪贴板 |
| `devin.cmd.devin.migrateMcpConfig.title` | Migrate MCP Config (~/.codeium/ → ~/.con | 迁移 MCP 配置（~/.codeium/ → ~/.config/devin/ |
| `devin.cmd.devin.migrateWorkspaceConfig.title` | Migrate Workspace Config (.windsurf/ → . | 迁移工作区配置（.windsurf/ → .devin/） |
| `devin.cmd.windsurf.addCurrentFileToChat.title` | Add current file to conversation | 将当前文件加入对话 |
| `devin.cmd.windsurf.createRule.title` | Create New Rule | 创建新规则 |
| `devin.cmd.windsurf.downloadDiagnostics.title` | Download Devin Diagnostics | 下载 Devin 诊断信息 |
| `devin.cmd.windsurf.generateCommitMessage.title` | Generate Commit Message | 生成提交信息 |

## 3. 语言包 bundle 注册与译文可查性

- 语言包版本 : 1.126.0  (engines.vscode = ^1.126.0)
- 已注册 bundle 数 : **95**
- 含 `windsurf` : ✅
- vscode bundle 译文总量 : **22,003** 条
- 补丁 667 条可查 : **667/667** ✅

### 补丁译文抽样（Devin 专有模块）

| 源文件 | key | 英文 | 中文 |
|---|---|---|---|
| `windsurfCustomColors` | `listHoverBackgroundSubtle` | A subtler version of list.hoverBackground, a | **list.hoverBackground 的更含蓄版本，一种主题感知的悬停颜色，通常比中** |
| `windsurfCustomColors` | `starkButtonBackground` | The background color used in stark buttons. | **用于 stark 按钮的背景颜色。** |
| `windsurfDiffColors` | `diffEditorInsertedCustom` | Background color for text that got inserted. | **用于已插入文本的背景颜色。该颜色不能是不透明的，以免遮挡下方的装饰。** |
| `windsurfDiffColors` | `diffEditorInsertedFallback` | Fallback background color for text that got  | **用于已插入文本的备用背景颜色。该颜色不能是不透明的，以免遮挡下方的装饰。** |
| `windsurfAuth` | `windsurfAccount` | Devin Account | **Devin 账户** |
| `windsurfAuth` | `windsurfUsage` | Devin Usage | **Devin 用量** |
| `chatClientPreview` | `incompatibleChatClientPreview` | This chat client preview requires a differen | **此聊天客户端预览需要不同的 Desktop API。请改用兼容的完整 Desktop 版** |
| `chatClientPreview` | `invalidChatClientPreviewId` | Invalid chat client preview ID. | **聊天客户端预览 ID 无效。** |
| `chatClientPreviewDownload` | `chatClientPreviewBundleHash` | The chat client preview bundle checksum or l | **聊天客户端预览包的校验和或长度不正确。** |
| `chatClientPreviewDownload` | `chatClientPreviewIncomplete` | The chat client preview download is incomple | **聊天客户端预览下载不完整。** |
| `chatClientPreviewMainService` | `cancelChatClientPreview` | Cancel | **取消** |
| `chatClientPreviewMainService` | `chatClientPreviewCacheFull` | At most eight windows can run chat client pr | **最多只能有八个窗口运行聊天客户端预览。请先将另一个窗口恢复正常状态。** |
| `windsurfCodicons` | `acpAgentIcon` | ACP agent icon | **ACP 智能体图标** |
| `windsurfCodicons` | `acpConnectorIcon` | ACP agent icon for {0} | **{0} 的 ACP 智能体图标** |

## 4. 改动清单（只列实际被写入的路径）

备份批次：`20261016-234347`

| 文件 | 原本存在 |
|---|---|
| `C:\Users\27837\.devin\argv.json` | 是（已备份） |
| `C:\Users\27837\.devin\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.126.0-universal\translations\main.i18n.json` | 是（已备份） |
| `C:\Users\27837\.devin\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.126.0-universal\package.json` | 是（已备份） |
| `C:\Users\27837\AppData\Roaming\devin\languagepacks.json` | 是（已备份） |
| `C:\Users\27837\AppData\Local\Programs\Devin\resources\app\extensions\windsurf\package.json` | 是（已备份） |
| `C:\Users\27837\AppData\Local\Programs\Devin\resources\app\extensions\windsurf\package.nls.json` | 否（新增） |

受保护的 11 个文件是否出现在改动清单中：**✅ 一个都没有**
