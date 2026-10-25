# Devin 桌面版汉化可行性实证报告

- Devin 安装目录: `C:\Users\27837\AppData\Local\Programs\Devin\resources\app`
- 应用版本: Devin 1.126.0 / windsurfVersion 3.11.216 / codeiumVersion 1.48.2
- 语言包: `C:\Users\27837\.devin\extensions\ms-ceintl.vscode-language-pack-zh-hans-1.126.0-universal`

## 1. NLS 结构

| 文件 | 结构 | 规模 |
|---|---|---:|
| `out/nls.keys.json` | `[[源文件, [key,...]], ...]` | 1,786 个源文件 |
| `out/nls.messages.json` | 展平的默认英文数组 | 21,210 条 |
| `main.i18n.json` → `contents` | `{源文件: {key: 译文}}` | 1,898 个源文件 |

展平后 key 总数 = **21,210**  ·  与 messages 数组长度一致 ✅

## 2. 覆盖率 (按 (源文件, key) 二元组)

- 全部 NLS 字符串 : **21,161**
- 官方语言包已译  : **20,999** (99.2%)
- 缺中文          : **162** (0.8%)
- 语言包译文总条数 : 22,003  (其中 1,004 条本构建已不存在)

## 3. 缺失字符串按源文件聚合 TOP 45

| 缺失 | 该文件总数 | 源文件 |
|---:|---:|---|
| 55 | 55 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellMenubar` |
| 24 | 24 | `vs/workbench/contrib/devinCloudSaveNotices/electron-browser/devinCloudSaveNotices.contribution` |
| 17 | 23 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` |
| 6 | 21 | `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` |
| 6 | 6 | `vs/workbench/contrib/windsurfAgentWindow/browser/devinSessionSshWindow` |
| 5 | 5 | `vs/workbench/contrib/windsurfAgentWindow/browser/cloudSessionEditorWindow` |
| 5 | 5 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellAppControls` |
| 4 | 4 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellSignedOut` |
| 4 | 5 | `vs/workbench/browser/windsurfSaveFile` |
| 4 | 13 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` |
| 4 | 11 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` |
| 3 | 3 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappEditors` |
| 3 | 3 | `vs/workbench/contrib/windsurfCascadeView/browser/cloudSessionWorkspaceEditorInput` |
| 2 | 11 | `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfCodeScanFindings/browser/codeScanFindingsEditorInput` |
| 2 | 2 | `vs/workbench/contrib/windsurfCodeScanFindings/browser/codeScanFindings.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappKeybindingEditing` |
| 2 | 7 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` |
| 2 | 263 | `vs/workbench/browser/workbench.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopShell/browser/createDevinHost` |
| 1 | 5 | `vs/platform/windsurfChatClient/common/chatClientPreview` |
| 1 | 7 | `vs/workbench/contrib/share/browser/share.contribution` |
| 1 | 6 | `vs/workbench/browser/parts/titlebar/agentEditorSwitch` |
| 1 | 18 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` |
| 1 | 51 | `vs/editor/common/editorContextKeys` |
| 1 | 4 | `vs/workbench/contrib/url/browser/url.contribution` |
| 1 | 2 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcpService` |
| 1 | 2 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascadeMainThreadCommands` |

## 4. Devin/Windsurf 专有源文件

| 缺失 | 总数 | 源文件 |
|---:|---:|---|
| 55 | 55 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellMenubar` |
| 24 | 24 | `vs/workbench/contrib/devinCloudSaveNotices/electron-browser/devinCloudSaveNotices.contribution` |
| 17 | 23 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappCommands` |
| 6 | 21 | `vs/workbench/contrib/windsurfAcpService/browser/acpRemoteHostActions` |
| 6 | 6 | `vs/workbench/contrib/windsurfAgentWindow/browser/devinSessionSshWindow` |
| 5 | 5 | `vs/workbench/contrib/windsurfAgentWindow/browser/cloudSessionEditorWindow` |
| 5 | 5 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellAppControls` |
| 4 | 11 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewDownload` |
| 4 | 13 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPage.contribution` |
| 4 | 4 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellSignedOut` |
| 4 | 5 | `vs/workbench/browser/windsurfSaveFile` |
| 3 | 3 | `vs/workbench/contrib/windsurfCascadeView/browser/cloudSessionWorkspaceEditorInput` |
| 3 | 3 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappEditors` |
| 2 | 11 | `vs/workbench/contrib/windsurfCascadeView/browser/cascadeView.contribution` |
| 2 | 7 | `vs/workbench/contrib/windsurfAgentWindow/browser/windsurfAgentWindowActions` |
| 2 | 2 | `vs/workbench/contrib/windsurfCodeScanFindings/browser/codeScanFindingsEditorInput` |
| 2 | 2 | `vs/workbench/contrib/windsurfCodeScanFindings/browser/codeScanFindings.contribution` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopShell/browser/createDevinHost` |
| 2 | 2 | `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappKeybindingEditing` |
| 1 | 18 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapViewer.contribution` |
| 1 | 5 | `vs/platform/windsurfChatClient/common/chatClientPreview` |
| 1 | 2 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcpService` |
| 1 | 2 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascadeMainThreadCommands` |
| 0 | 11 | `vs/workbench/contrib/windsurfChatClient/electron-browser/chatClientModuleSelection.contribution` |
| 0 | 4 | `vs/workbench/contrib/windsurfDatadogRum/browser/datadogRum.contribution` |
| 0 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiffEditorPane` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/snippetEditorPane` |
| 0 | 8 | `vs/workbench/contrib/windsurfFeedback/browser/windsurfFeedback.contribution` |
| 0 | 8 | `vs/workbench/services/devinCloudFiles/browser/devinCloudEditorError` |
| 0 | 14 | `vs/workbench/contrib/windsurfPullRequest/browser/pullRequest.contribution` |
| 0 | 12 | `vs/platform/windsurfChatClient/electron-main/chatClientPreviewMainService` |
| 0 | 12 | `vs/workbench/contrib/windsurfMigration/electron-browser/windsurfMigration.contribution` |
| 0 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/loadCloudSessionByIdDev.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapBookmarkDecorationService` |
| 0 | 6 | `vs/platform/windsurfSvg/browser/windsurfCodicons` |
| 0 | 6 | `vs/workbench/contrib/windsurfAcpService/browser/acpSessionsQuickAccess` |
| 0 | 3 | `vs/workbench/contrib/windsurfOnboarding/browser/windsurfOnboarding.contribution` |
| 0 | 13 | `vs/platform/theme/common/colors/windsurfCustomColors` |
| 0 | 5 | `vs/workbench/contrib/windsurfCascadeView/browser/dissolveAllSpacesDev.contribution` |
| 0 | 8 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/windsurfStatusBarSettingsPanel` |
| 0 | 2 | `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShell.contribution` |
| 0 | 3 | `vs/workbench/contrib/windsurfDiffViewer/browser/spaceDiff.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfDesktopBridge/browser/openCloudSession` |
| 0 | 4 | `vs/workbench/contrib/windsurfAcpService/browser/windsurfAcp.contribution` |
| 0 | 5 | `vs/workbench/contrib/devinCloudFiles/browser/devinCloudFilesStatusView` |
| 0 | 9 | `vs/workbench/contrib/windsurfAgentWindow/browser/newSessionTabButton` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWindowReveal` |
| 0 | 2 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapExportAction` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/windsurfAgentWindowActions` |
| 0 | 2 | `vs/workbench/contrib/windsurfAgentWindow/browser/devinCloudTerminal` |
| 0 | 8 | `vs/workbench/contrib/windsurfMcpService/browser/windsurfMcp.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfStatusBarSettingsService/browser/tabs/keybindingTab` |
| 0 | 2 | `vs/workbench/contrib/windsurfShellViewer/browser/shellViewer.contribution` |
| 0 | 3 | `vs/workbench/contrib/windsurfDesignTokenEditor/browser/designTokenEditor.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfCustomAppIcon/browser/windsurfAppIconCustomization.contribution` |
| 0 | 4 | `vs/platform/theme/common/colors/windsurfDiffColors` |
| 0 | 1 | `vs/workbench/contrib/windsurfPlanViewer/browser/planViewer.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfAgentWindow/electron-browser/agentWorkspacePrewarm` |
| 0 | 2 | `vs/platform/windsurfAuth/common/windsurfAuth` |
| 0 | 1 | `vs/workbench/contrib/windsurfSettingsPage/browser/windsurfSettingsPageConstants` |
| 0 | 1 | `vs/workbench/contrib/windsurfCodeMapViewer/browser/codeMapHomeEditorInput` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascadeView/browser/readOnlyDiffContentProvider` |
| 0 | 1 | `vs/workbench/contrib/windsurfCascade/browser/windsurfCascade.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfTestRecordingViewer/browser/testRecordingViewer.contribution` |
| 0 | 2 | `vs/workbench/contrib/windsurfDesktopViewer/browser/desktopViewer.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfPlanEditor/browser/planEditor.contribution` |
| 0 | 1 | `vs/workbench/contrib/windsurfAcpDev/browser/acpDev.contribution` |
| 0 | 1 | `vs/workbench/contrib/terminalContrib/cascadeManagedFooter/browser/terminal.cascadeManagedFooter.contribution` |

专有文件合计: 68 个文件, 全部 key 418, 其中缺中文 156

## 5. 缺中文的 Devin/Windsurf 字符串样例 (前 60)

| 源文件 | 英文原文 |
|---|---|
| `desktopShellMenubar` | &&Edit |
| `desktopShellMenubar` | &&File |
| `desktopShellMenubar` | &&Go |
| `desktopShellMenubar` | &&Help |
| `desktopShellMenubar` | &&About |
| `desktopShellMenubar` | &&Back |
| `desktopShellMenubar` | Close &&Tab |
| `desktopShellMenubar` | Close Window |
| `desktopShellMenubar` | &&Command Palette |
| `desktopShellMenubar` | &&Copy |
| `desktopShellMenubar` | Cu&&t |
| `desktopShellMenubar` | Devin &&Settings |
| `desktopShellMenubar` | &&Find |
| `desktopShellMenubar` | Find &&Next |
| `desktopShellMenubar` | Find &&Previous |
| `desktopShellMenubar` | &&Forward |
| `desktopShellMenubar` | Go to &&Definition |
| `desktopShellMenubar` | Go to &&File... |
| `desktopShellMenubar` | &&Keyboard Shortcuts |
| `desktopShellMenubar` | New &&Agent Window |
| `desktopShellMenubar` | New &&IDE Window |
| `desktopShellMenubar` | New &&Session |
| `desktopShellMenubar` | &&Next Tab |
| `desktopShellMenubar` | &&Notifications |
| `desktopShellMenubar` | &&Open... |
| `desktopShellMenubar` | &&Open File... |
| `desktopShellMenubar` | Open &&Folder... |
| `desktopShellMenubar` | Open &&Folder... |
| `desktopShellMenubar` | Open &&Recent |
| `desktopShellMenubar` | &&Paste |
| `desktopShellMenubar` | &&Previous Tab |
| `desktopShellMenubar` | Open Process E&&xplorer |
| `desktopShellMenubar` | E&&xit |
| `desktopShellMenubar` | &&Redo |
| `desktopShellMenubar` | &&Reopen Closed Tab |
| `desktopShellMenubar` | &&Replace |
| `desktopShellMenubar` | Re&vert File |
| `desktopShellMenubar` | &&Save |
| `desktopShellMenubar` | Search &&Sessions |
| `desktopShellMenubar` | Search &&Workspace |
| `desktopShellMenubar` | Select &&All |
| `desktopShellMenubar` | Toggle &&Block Comment |
| `desktopShellMenubar` | Toggle Developer &&Tools |
| `desktopShellMenubar` | &&Full Screen |
| `desktopShellMenubar` | &&Toggle Line Comment |
| `desktopShellMenubar` | Toggle &&Sidebar |
| `desktopShellMenubar` | Toggle &&Terminal |
| `desktopShellMenubar` | Toggle &&Theme |
| `desktopShellMenubar` | &&Undo |
| `desktopShellMenubar` | View &&License |
| `desktopShellMenubar` | Zoom &&In |
| `desktopShellMenubar` | Zoom &&Out |
| `desktopShellMenubar` | &&Reset Zoom |
| `desktopShellMenubar` | &&Preferences |
| `desktopShellMenubar` | &&View |
| `devinCloudSaveNotices.contribution` | Devin Cloud: Disable Save Notices |
| `devinCloudSaveNotices.contribution` | Devin is no longer told about the files you save in this Devin Cloud session. |
| `devinCloudSaveNotices.contribution` | Devin Cloud: Enable Save Notices |
| `devinCloudSaveNotices.contribution` | Devin is now told about the files you save in this Devin Cloud session. Devin reviews, commits and pushes them. |
| `devinCloudSaveNotices.contribution` | Save notice failed |

## 6. 完全缺中文的源文件 (语言包零覆盖)

共 8 个文件。前 30：

- `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellMenubar` (55 条)
- `vs/workbench/contrib/devinCloudSaveNotices/electron-browser/devinCloudSaveNotices.contribution` (24 条)
- `vs/workbench/contrib/windsurfAgentWindow/browser/devinSessionSshWindow` (6 条)
- `vs/workbench/contrib/windsurfAgentWindow/browser/cloudSessionEditorWindow` (5 条)
- `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellAppControls` (5 条)
- `vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellSignedOut` (4 条)
- `vs/workbench/contrib/windsurfCascadeView/browser/cloudSessionWorkspaceEditorInput` (3 条)
- `vs/workbench/contrib/windsurfDesktopShell/browser/devinWebappEditors` (3 条)

## 7. 内置扩展的贡献点（Devin 家族）

| 扩展 | 命令数 | 硬编码英文 title | 目录内 package.nls* |
|---|---:|---:|---|
| `windsurf` | 60 | 60 | **无** |
| `windsurf-dev-containers` | 11 | 11 | **无** |
| `windsurf-remote-devin` | 1 | 1 | **无** |
| `windsurf-remote-openssh` | 13 | 13 | **无** |
| `windsurf-remote-wsl` | 14 | 14 | **无** |

结论: 这些扩展的命令标题、菜单、配置项说明全部硬编码英文，**官方语言包机制无法覆盖**；
本插件的做法是写 `package.nls.json` / `package.nls.zh-cn.json` 并把 package.json 里的字符串换成 `%key%`
（见 `tools/build_manifest_plan.py` 与 `extension.js` 的第 2 层）。
