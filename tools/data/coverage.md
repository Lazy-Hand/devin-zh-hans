# Devin 桌面版汉化可行性实证报告

- Devin 安装目录: `C:\Users\27837\AppData\Local\Programs\Devin\resources\app`
- 应用版本: Devin 1.126.0 / windsurfVersion 3.10.67 / codeiumVersion 1.48.2 (Exafunction, Inc.)
- 语言包: `C:\Users\27837\.devin\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.126.0-universal`

## 1. NLS 结构

| 文件 | 结构 | 规模 |
|---|---|---:|
| `out/nls.keys.json` | `[[源文件, [key,...]], ...]` | 1,797 个源文件 |
| `out/nls.messages.json` | 展平的默认英文数组 | 21,220 条 |
| `main.i18n.json` → `contents` | `{源文件: {key: 译文}}` | 1,898 个源文件 |

展平后 key 总数 = **21,220**  ·  与 messages 数组长度一致 ✅

## 2. 覆盖率 (按 (源文件, key) 二元组)

- 全部 NLS 字符串 : **21,171**
- 官方语言包已译  : **21,171** (100.0%)
- 缺中文          : **0** (0.0%)
- 语言包译文总条数 : 22,003  (其中 832 条本构建已不存在)

## 3. 缺失字符串按源文件聚合 TOP 45

| 缺失 | 该文件总数 | 源文件 |
|---:|---:|---|

## 4. Devin/Windsurf 专有源文件

| 缺失 | 总数 | 源文件 |
|---:|---:|---|
| 0 | 13 | `vs/platform/theme/common/colors/windsurfCustomColors` |
| 0 | 14 | `vs/workbench/contrib/windsurfPullRequest/browser/pullRequest.contribution` |
| 0 | 12 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewMainService` |
| 0 | 1 | `vs/workbench/contrib/terminalContrib/cascadeManagedFooter/browser/terminal.cascadeManagedFooter.contribution` |
| 0 | 6 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFilesStatusView` |
| 0 | 2 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/customizationsEditor.contribution` |
| 0 | 3 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFiles.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/tabs/keybindingTab` |
| 0 | 4 | `vs/platform/windsurfChatClient/common/chatClientPreview` |
| 0 | 4 | `vs/workbench/contrib/windsurfDatadogRum/browser/datadogRum.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfAcpDev/browser/acpDev.contribution` |
| 0 | 15 | `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` |
| 0 | 8 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/windsurfStatusBarSettingsPanel` |
| 0 | 11 | `vs/workbench/contrib/windsurfMcpService/browser/windsurfMcp.contribution` |
| 0 | 9 | `vs/workbench/contrib/windsurfAgentWindow/browser/newSessionTabButton` |
| 0 | 18 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` |
| 0 | 4 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShell.contribution` |
| 0 | 13 | `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWindowReveal` |
| 0 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/loadCloudSessionByIdDev.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascadeMainThreadCommands` |
| 0 | 11 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` |
| 0 | 6 | `vs/platform/windsurfSvg/browser/windsurfCodicons` |
| 0 | 4 | `vs/workbench/contrib/windsurfDesktopBridge/browser/desktopNav.contribution` |
| 0 | 1 | `vs/workbench/browser/windsurfSaveFile` |
| 0 | 4 | `vs/workbench/contrib/windsurfAgentWindow/browser/agentSpaceNavHistory` |
| 0 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/dissolveAllSpacesDev.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfAgentSidebar/browser/windsurfAgentSidebar.contribution` |
| 0 | 6 | `vs/workbench/contrib/windsurfAcpService/browser/acpSessionsQuickAccess` |
| 0 | 5 | `vs/workbench/contrib/windsurfAcpService/browser/cascadeMigrationWizard.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPageConstants` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowFont` |
| 0 | 11 | `vs/workbench/contrib/windsurfChatClient/electron-browser/chatClientModuleSelection.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapExportAction` |
| 0 | 12 | `vs/workbench/contrib/windsurfMigration/electron-browser/windsurfMigration.contribution` |
| 0 | 8 | `vs/workbench/contrib/windsurfFeedback/browser/windsurfFeedback.contribution` |
| 0 | 11 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` |
| 0 | 6 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` |
| 0 | 4 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcp.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfPlanViewer/browser/planViewer.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfPlanEditor/browser/planEditor.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/windsurfAgentWindowActions` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/snippetEditorPane` |
| 0 | 2 | `vs/platform/windsurfAuth/common/windsurfAuth` |
| 0 | 7 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` |
| 0 | 3 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascade.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfDesktopViewer/browser/desktopViewer.contribution` |
| 0 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiffEditorPane` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/readOnlyDiffContentProvider` |
| 0 | 1 | `vs/workbench/contrib/windsurfTestRecordingViewer/browser/testRecordingViewer.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfSettingsPage/browser/react/windsurfReactSettingsPageInput` |
| 0 | 4 | `vs/platform/theme/common/colors/windsurfDiffColors` |
| 0 | 3 | `vs/workbench/contrib/windsurfDesignTokenEditor/browser/designTokenEditor.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfDesktopBridge/browser/openCloudSession` |
| 0 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiff.contribution` |
| 0 | 3 | `vs/workbench/contrib/windsurfOnboarding/browser/windsurfOnboarding.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/customizationsEditorInput` |
| 0 | 10 | `vs/workbench/services/devinCloudFiles/browser/devinCloudEditorError` |
| 0 | 1 | `vs/workbench/contrib/windsurfAcpService/browser/cascadeMigrationWizardEditor` |
| 0 | 3 | `vs/workbench/browser/parts/editor/editorGroupWindsurfWelcome` |
| 0 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapBookmarkDecorationService` |
| 0 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapHomeEditorInput` |
| 0 | 1 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcpService` |
| 0 | 2 | `vs/workbench/contrib/windsurfShellViewer/browser/shellViewer.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWorkspacePrewarm` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/browser/devinCloudTerminal` |
| 0 | 2 | `vs/workbench/contrib/windsurfCustomAppIcon/browser/windsurfAppIconCustomization.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfSettingsPage/browser/react/windsurfReactSettingsPage.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfCustomizationsEditor/browser/devinLocalPluginEditorInput` |

专有文件合计: 69 个文件, 全部 key 316, 其中缺中文 0

## 5. 缺中文的 Devin/Windsurf 字符串样例 (前 60)

| 源文件 | 英文原文 |
|---|---|

## 6. 完全缺中文的源文件 (语言包零覆盖)

共 0 个文件。前 30：


## 7. `extensions/windsurf` 扩展本身

- package.json 命令数: 64
- title 为**硬编码英文**(无 `%key%` 占位符): **0 / 64**
- 目录内 `package.nls*.json` 文件: ['package.nls.json']
- 编译产物: `dist/extension.js` 9,760,537 bytes (未 minify 成 asar，可直接改)

结论: 该扩展的 64 个命令标题、菜单、配置项描述全部硬编码英文，**官方语言包机制无法覆盖**，
必须在 `resources/app/extensions/windsurf/package.json` 里补 `package.nls.zh-cn.json` 并改成 `%key%`。
