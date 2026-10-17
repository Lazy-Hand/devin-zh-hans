# Devin 桌面版汉化可行性实证报告

- Devin 安装目录: `C:\Users\27837\AppData\Local\Programs\Devin\resources\app`
- 应用版本: Devin 1.126.0 / windsurfVersion 3.10.67 / codeiumVersion 1.48.2 (Exafunction, Inc.)
- 语言包: `C:\Users\27837\.devin\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.126.0-universal`

## 1. NLS 结构

| 文件 | 结构 | 规模 |
|---|---|---:|
| `out/nls.keys.json` | `[[源文件, [key,...]], ...]` | 1,797 个源文件 |
| `out/nls.messages.json` | 展平的默认英文数组 | 21,220 条 |
| `main.i18n.json` → `contents` | `{源文件: {key: 译文}}` | 1,806 个源文件 |

展平后 key 总数 = **21,220**  ·  与 messages 数组长度一致 ✅

## 2. 覆盖率 (按 (源文件, key) 二元组)

- 全部 NLS 字符串 : **21,171**
- 官方语言包已译  : **20,504** (96.8%)
- 缺中文          : **667** (3.2%)
- 语言包译文总条数 : 21,336  (其中 832 条本构建已不存在)

## 3. 缺失字符串按源文件聚合 TOP 45

| 缺失 | 该文件总数 | 源文件 |
|---:|---:|---|
| 52 | 52 | `vs/workbench/contrib/lifeguard/browser/lifeguardPane` |
| 18 | 265 | `vs/workbench/browser/workbench.contribution` |
| 18 | 18 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` |
| 17 | 41 | `vs/workbench/contrib/update/browser/update` |
| 16 | 16 | `vs/workbench/contrib/lifeguard/browser/lifeguardService` |
| 16 | 16 | `vs/workbench/browser/parts/auxiliaryactivitybar/auxiliaryactivitybarPart` |
| 15 | 15 | `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` |
| 14 | 14 | `vs/workbench/contrib/windsurfPullRequest/browser/pullRequest.contribution` |
| 13 | 13 | `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` |
| 13 | 13 | `vs/platform/theme/common/colors/windsurfCustomColors` |
| 12 | 12 | `vs/workbench/contrib/windsurfMigration/electron-browser/windsurfMigration.contribution` |
| 12 | 12 | `vs/workbench/contrib/deepwiki/browser/deepwiki.contribution` |
| 12 | 96 | `vs/workbench/common/contextkeys` |
| 12 | 12 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewMainService` |
| 11 | 11 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` |
| 11 | 11 | `vs/workbench/contrib/windsurfChatClient/electron-browser/chatClientModuleSelection.contribution` |
| 11 | 11 | `vs/workbench/contrib/lifeguard/browser/lifeguardBugCard` |
| 11 | 11 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` |
| 11 | 11 | `vs/workbench/contrib/windsurfMcpService/browser/windsurfMcp.contribution` |
| 10 | 10 | `vs/workbench/services/devinCloudFiles/browser/devinCloudEditorError` |
| 10 | 142 | `vs/workbench/contrib/welcomeGettingStarted/common/gettingStartedContent` |
| 9 | 58 | `vs/workbench/contrib/extensions/browser/extensionsViewlet` |
| 9 | 9 | `vs/workbench/contrib/windsurfAgentWindow/browser/newSessionTabButton` |
| 9 | 11 | `vs/workbench/browser/parts/titlebar/titlebarPart` |
| 9 | 9 | `vs/workbench/browser/parts/titlebar/agentEditorSwitch` |
| 8 | 8 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/windsurfStatusBarSettingsPanel` |
| 8 | 8 | `vs/workbench/contrib/windsurfFeedback/browser/windsurfFeedback.contribution` |
| 7 | 7 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` |
| 7 | 12 | `vs/workbench/electron-browser/actions/installActions` |
| 7 | 19 | `vs/platform/windows/electron-main/windowImpl` |
| 6 | 142 | `vs/workbench/browser/parts/editor/editor.contribution` |
| 6 | 6 | `vs/workbench/contrib/lifeguard/browser/lifeguard.contribution` |
| 6 | 6 | `vs/workbench/contrib/windsurfAcpService/browser/acpSessionsQuickAccess` |
| 6 | 6 | `vs/platform/windsurfSvg/browser/windsurfCodicons` |
| 6 | 6 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFilesStatusView` |
| 6 | 19 | `vs/platform/native/electron-main/nativeHostMainService` |
| 6 | 6 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` |
| 5 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/dissolveAllSpacesDev.contribution` |
| 5 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/loadCloudSessionByIdDev.contribution` |
| 5 | 65 | `vs/workbench/browser/parts/editor/editorStatus` |
| 5 | 5 | `vs/workbench/contrib/deepwiki/browser/deepwikiHoverParticipant` |
| 5 | 5 | `vs/workbench/contrib/terminalContrib/terminalCommandPopup/browser/terminal.terminalCommandPopupHint.contribution` |
| 5 | 24 | `vs/workbench/contrib/scm/browser/scmViewPane` |
| 5 | 5 | `vs/workbench/contrib/windsurfAcpService/browser/cascadeMigrationWizard.contribution` |
| 4 | 4 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShell.contribution` |

## 4. Devin/Windsurf 专有源文件

| 缺失 | 总数 | 源文件 |
|---:|---:|---|
| 18 | 18 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` |
| 15 | 15 | `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` |
| 14 | 14 | `vs/workbench/contrib/windsurfPullRequest/browser/pullRequest.contribution` |
| 13 | 13 | `vs/platform/theme/common/colors/windsurfCustomColors` |
| 13 | 13 | `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` |
| 12 | 12 | `vs/workbench/contrib/windsurfMigration/electron-browser/windsurfMigration.contribution` |
| 12 | 12 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewMainService` |
| 11 | 11 | `vs/workbench/contrib/windsurfChatClient/electron-browser/chatClientModuleSelection.contribution` |
| 11 | 11 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` |
| 11 | 11 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` |
| 11 | 11 | `vs/workbench/contrib/windsurfMcpService/browser/windsurfMcp.contribution` |
| 10 | 10 | `vs/workbench/services/devinCloudFiles/browser/devinCloudEditorError` |
| 9 | 9 | `vs/workbench/contrib/windsurfAgentWindow/browser/newSessionTabButton` |
| 8 | 8 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/windsurfStatusBarSettingsPanel` |
| 8 | 8 | `vs/workbench/contrib/windsurfFeedback/browser/windsurfFeedback.contribution` |
| 7 | 7 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` |
| 6 | 6 | `vs/platform/windsurfSvg/browser/windsurfCodicons` |
| 6 | 6 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` |
| 6 | 6 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFilesStatusView` |
| 6 | 6 | `vs/workbench/contrib/windsurfAcpService/browser/acpSessionsQuickAccess` |
| 5 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/loadCloudSessionByIdDev.contribution` |
| 5 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/dissolveAllSpacesDev.contribution` |
| 5 | 5 | `vs/workbench/contrib/windsurfAcpService/browser/cascadeMigrationWizard.contribution` |
| 4 | 4 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShell.contribution` |
| 4 | 4 | `vs/platform/windsurfChatClient/common/chatClientPreview` |
| 4 | 4 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcp.contribution` |
| 4 | 4 | `vs/platform/theme/common/colors/windsurfDiffColors` |
| 4 | 4 | `vs/workbench/contrib/windsurfAgentWindow/browser/agentSpaceNavHistory` |
| 4 | 4 | `vs/workbench/contrib/windsurfDatadogRum/browser/datadogRum.contribution` |
| 4 | 4 | `vs/workbench/contrib/windsurfDesktopBridge/browser/desktopNav.contribution` |
| 3 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiff.contribution` |
| 3 | 3 | `vs/workbench/contrib/windsurfOnboarding/browser/windsurfOnboarding.contribution` |
| 3 | 3 | `vs/workbench/browser/parts/editor/editorGroupWindsurfWelcome` |
| 3 | 3 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascade.contribution` |
| 3 | 3 | `vs/workbench/contrib/windsurfDesignTokenEditor/browser/designTokenEditor.contribution` |
| 3 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiffEditorPane` |
| 3 | 3 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFiles.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapExportAction` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopViewer/browser/desktopViewer.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/windsurfAgentWindowActions` |
| 2 | 2 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/customizationsEditor.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfAgentWindow/browser/devinCloudTerminal` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopBridge/browser/openCloudSession` |
| 2 | 2 | `vs/workbench/contrib/windsurfSettingsPage/browser/react/windsurfReactSettingsPageInput` |
| 2 | 2 | `vs/platform/windsurfAuth/common/windsurfAuth` |
| 2 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWindowReveal` |
| 2 | 2 | `vs/workbench/contrib/windsurfShellViewer/browser/shellViewer.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfCustomAppIcon/browser/windsurfAppIconCustomization.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowFont` |
| 2 | 2 | `vs/workbench/contrib/windsurfPlanEditor/browser/planEditor.contribution` |
| 1 | 1 | `vs/workbench/contrib/terminalContrib/cascadeManagedFooter/browser/terminal.cascadeManagedFooter.contribution` |
| 1 | 1 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/customizationsEditorInput` |
| 1 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapBookmarkDecorationService` |
| 1 | 1 | `vs/workbench/contrib/windsurfPlanViewer/browser/planViewer.contribution` |
| 1 | 1 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/tabs/keybindingTab` |
| 1 | 1 | `vs/workbench/contrib/windsurfTestRecordingViewer/browser/testRecordingViewer.contribution` |
| 1 | 1 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascadeMainThreadCommands` |
| 1 | 1 | `vs/workbench/contrib/windsurfSettingsPage/browser/react/windsurfReactSettingsPage.contribution` |
| 1 | 1 | `vs/workbench/contrib/windsurfAgentSidebar/browser/windsurfAgentSidebar.contribution` |
| 1 | 1 | `vs/workbench/browser/windsurfSaveFile` |
| 1 | 1 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcpService` |
| 1 | 1 | `vs/workbench/contrib/windsurfAcpService/browser/cascadeMigrationWizardEditor` |
| 1 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/snippetEditorPane` |
| 1 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapHomeEditorInput` |
| 1 | 1 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPageConstants` |
| 1 | 1 | `vs/workbench/contrib/windsurfAcpDev/browser/acpDev.contribution` |
| 1 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/readOnlyDiffContentProvider` |
| 1 | 1 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWorkspacePrewarm` |
| 1 | 1 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/devinLocalPluginEditorInput` |

专有文件合计: 69 个文件, 全部 key 316, 其中缺中文 316

## 5. 缺中文的 Devin/Windsurf 字符串样例 (前 60)

| 源文件 | 英文原文 |
|---|---|
| `codeMapViewer.contribution` | Add Codemap to Cascade |
| `codeMapViewer.contribution` | Home |
| `codeMapViewer.contribution` | Codemap Editor |
| `codeMapViewer.contribution` | Codemaps |
| `codeMapViewer.contribution` | Codemaps |
| `codeMapViewer.contribution` | Generate Codemap |
| `codeMapViewer.contribution` | Generate Codemap from Cascade |
| `codeMapViewer.contribution` | Generate Codemap from Navigation History |
| `codeMapViewer.contribution` | {0} codemap generating |
| `codeMapViewer.contribution` | {0} codemaps generating |
| `codeMapViewer.contribution` | Check if Codemaps is Enabled |
| `codeMapViewer.contribution` | Load Codemap |
| `codeMapViewer.contribution` | &&Codemaps |
| `codeMapViewer.contribution` | Open Codemap by ID |
| `codeMapViewer.contribution` | Open Codemap Chat |
| `codeMapViewer.contribution` | Open Codemaps |
| `codeMapViewer.contribution` | Open Trajectory Dashboard |
| `codeMapViewer.contribution` | Devin |
| `acpRemoteHostActions` | Add New SSH Host... |
| `acpRemoteHostActions` | Add New SSH Host for Remote Agents... |
| `acpRemoteHostActions` | Configure SSH Hosts... |
| `acpRemoteHostActions` | Configure SSH Hosts for Remote Agents... |
| `acpRemoteHostActions` | Open SSH configuration file |
| `acpRemoteHostActions` | Connect to Remote Agent Host... |
| `acpRemoteHostActions` | Select a configured SSH host or enter user@host |
| `acpRemoteHostActions` | Connect to remote agent host |
| `acpRemoteHostActions` | Disconnect Remote Agent Host |
| `acpRemoteHostActions` | Enter an SSH host alias or user@host. |
| `acpRemoteHostActions` | saved |
| `acpRemoteHostActions` | Remove Remote Agent Host |
| `acpRemoteHostActions` | Failed to create the SSH config file: {0} |
| `acpRemoteHostActions` | Failed to list SSH config files: {0} |
| `acpRemoteHostActions` | Devin |
| `pullRequest.contribution` | Open Pull Request |
| `pullRequest.contribution` | Find Next in Devin Review |
| `pullRequest.contribution` | Find Previous in Devin Review |
| `pullRequest.contribution` | Stop Find in Devin Review |
| `pullRequest.contribution` | Refresh Devin Review |
| `pullRequest.contribution` | Find in Devin Review |
| `pullRequest.contribution` | Toggle Developer Tools (Devin Review) |
| `pullRequest.contribution` | Open in Devin Review |
| `pullRequest.contribution` | Open in GitHub |
| `pullRequest.contribution` | Devin Review |
| `pullRequest.contribution` | Render Devin Review in an embedded webview iframe instead of a native browser view. Intended for local development; in production  |
| `pullRequest.contribution` | Pull Request |
| `pullRequest.contribution` | Devin |
| `pullRequest.contribution` | Enter the pull request URL |
| `windsurfCustomColors` | A subtler version of list.hoverBackground, a theme-aware hover color that often has a bit more color than a neutral translucent gr |
| `windsurfCustomColors` | The background color used in stark buttons. |
| `windsurfCustomColors` | The foreground color used in stark buttons. |
| `windsurfCustomColors` | The background color used in stark buttons when hovered. |
| `windsurfCustomColors` | Devin black color used for custom UI elements. |
| `windsurfCustomColors` | Devin sea color used for custom UI elements. |
| `windsurfCustomColors` | Devin sea shade color used for custom UI elements. |
| `windsurfCustomColors` | Devin sea tint color used for custom UI elements. |
| `windsurfCustomColors` | Blue session status color. |
| `windsurfCustomColors` | Green session status color. |
| `windsurfCustomColors` | Orange session status color. |
| `windsurfCustomColors` | Purple session status color. |
| `windsurfCustomColors` | Red session status color. |

## 6. 完全缺中文的源文件 (语言包零覆盖)

共 54 个文件。前 30：

- `vs/workbench/contrib/lifeguard/browser/lifeguardPane` (52 条)
- `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` (18 条)
- `vs/workbench/browser/parts/auxiliaryactivitybar/auxiliaryactivitybarPart` (16 条)
- `vs/workbench/contrib/lifeguard/browser/lifeguardService` (16 条)
- `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` (15 条)
- `vs/workbench/contrib/windsurfPullRequest/browser/pullRequest.contribution` (14 条)
- `vs/platform/theme/common/colors/windsurfCustomColors` (13 条)
- `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` (13 条)
- `vs/workbench/contrib/windsurfMigration/electron-browser/windsurfMigration.contribution` (12 条)
- `vs/workbench/contrib/deepwiki/browser/deepwiki.contribution` (12 条)
- `vs/platform/windsurfChatClient/electron-main/chatClientPreviewMainService` (12 条)
- `vs/workbench/contrib/windsurfChatClient/electron-browser/chatClientModuleSelection.contribution` (11 条)
- `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` (11 条)
- `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` (11 条)
- `vs/workbench/contrib/windsurfMcpService/browser/windsurfMcp.contribution` (11 条)
- `vs/workbench/contrib/lifeguard/browser/lifeguardBugCard` (11 条)
- `vs/workbench/services/devinCloudFiles/browser/devinCloudEditorError` (10 条)
- `vs/workbench/browser/parts/titlebar/agentEditorSwitch` (9 条)
- `vs/workbench/contrib/windsurfAgentWindow/browser/newSessionTabButton` (9 条)
- `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/windsurfStatusBarSettingsPanel` (8 条)
- `vs/workbench/contrib/windsurfFeedback/browser/windsurfFeedback.contribution` (8 条)
- `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` (7 条)
- `vs/platform/windsurfSvg/browser/windsurfCodicons` (6 条)
- `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` (6 条)
- `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFilesStatusView` (6 条)
- `vs/workbench/contrib/lifeguard/browser/lifeguard.contribution` (6 条)
- `vs/workbench/contrib/windsurfAcpService/browser/acpSessionsQuickAccess` (6 条)
- `vs/workbench/contrib/terminalContrib/terminalCommandPopup/browser/terminal.terminalCommandPopupHint.contribution` (5 条)
- `vs/workbench/contrib/deepwiki/browser/deepwikiHoverParticipant` (5 条)
- `vs/workbench/contrib/windsurfCascadeView/browser/loadCloudSessionByIdDev.contribution` (5 条)

## 7. `extensions/windsurf` 扩展本身

- package.json 命令数: 64
- title 为**硬编码英文**(无 `%key%` 占位符): **64 / 64**
- 目录内 `package.nls*.json` 文件: **无** → 该扩展完全没有本地化入口**
- 编译产物: `dist/extension.js` 9,760,537 bytes (未 minify 成 asar，可直接改)

结论: 该扩展的 64 个命令标题、菜单、配置项描述全部硬编码英文，**官方语言包机制无法覆盖**，
必须在 `resources/app/extensions/windsurf/package.json` 里补 `package.nls.zh-cn.json` 并改成 `%key%`。
