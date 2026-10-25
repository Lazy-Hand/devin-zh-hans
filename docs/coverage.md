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

---

## webapp-host（新版 Agent UI）i18n 资源与词典覆盖

- 目录: `C:\Users\27837\AppData\Local\Programs\Devin\resources\app\out\vs\workbench\devin-webapp-host`
- chunk 数: **1877**（另有语言包 chunk 6 个）
  - `es-DoaNSjW8.js` → 1092 个 key
  - `es-lslvHws0.js` → 4846 个 key
  - `ja-Cd26s5QO.js` → 5030 个 key
  - `ja-yCsZX4qV.js` → 997 个 key
  - `pt-BXE2Mn0r.js` → 1054 个 key
  - `pt-C9gxajH_.js` → 1229 个 key
- 语言包 key 并集: **7140**
- en 资源里能对上语言包 key 的: **6454**
- 去重后英文原文: **6118**
- 词典已覆盖: **4188** (68.5%)
- 仍缺中文: **1930**（其中可直接做整串替换的 304）

## 英文资源最集中的 chunk

| 条数 | chunk |
|---:|---|
| 5829 | `entry-host-editor-mode-menu-DUnUGWLA.js` |
| 58 | `app-initial-iBdDCKn9.js` |
| 55 | `AutomationScopeRow-P5pwWySJ.js` |
| 40 | `analytics-CJCVA0_o.js` |
| 17 | `app-initial-BSaQs-19.js` |
| 15 | `_id-BbuwVwEK.js` |
| 15 | `app-initial-BLk5Klv2.js` |
| 14 | `app-initial-BaGlYeyX.js` |
| 13 | `SessionPanes-CRE6Kml9.js` |
| 13 | `app-initial-DBgi9uS8.js` |
| 13 | `app-initial-BDS1xbku.js` |
| 12 | `CollectionDialog-BPXGjGhG.js` |
| 11 | `app-initial-ByKIbGC8.js` |
| 11 | `ScopedTriggerSummary-BQFAxFP3.js` |
| 11 | `PRDigestUnauthedHomePage-oadWXHfk.js` |

## 缺口样例（前 80）

| key | 英文 |
|---|---|
| `accessDeniedDescription` | You don't have permission to view this page. Contact your organization admin to request access. |
| `acknowledgeStatement` | By proceeding, I acknowledge that I have read, understood, and will comply with the rules above. |
| `actorEmailHelp` | Notes and incident updates Devin writes to PagerDuty are attributed to this user. Use a service user for clari |
| `addPluginMcpDescription` | Point Devin at an MCP server you run yourself. It is saved to your plugin and connected. |
| `addReviewMd` | Add a REVIEW.md to your repository with repository-specific instructions for code review. |
| `adminDescription` | Enterprise admins can select or clear the default under Membership. The selected default applies regardless of |
| `advancedEditorHint` | Want to add more resources, like scripts or templates? Use the <link>advanced editor</link>. |
| `aiWarning` | ⚠️ This is a Generative AI based tool — it can make mistakes. Confirm accuracy of output before any uses. |
| `allocationSubtitle` | Each bar is the LOB's assigned ACUs for the selected period, filled by what it consumed |
| `appRegistrationRemoveDescription` | Members will have to link their PagerDuty accounts again once a new app registration is added. |
| `appRegistrationScopeHelp` | Space-separated scopes; must match the scopes enabled on the PagerDuty app. Leave empty to use the app's own p |
| `archiveConfirmDescription` | Archived budgets stay in the list under the All filter. New child budgets can't be added under them. |
| `argsHelpFromArgs` | Pre-filled from the task's args model with every field named; enqueue validates against it. The job's account  |
| `argsHelpSystem` | Pre-filled from the task's args model with every field named; enqueue validates against it. Account-less task: |
| `askDevinDesc` | Integrates with Devin's agentic reasoning harness to answer any question about the PR or larger codebase. |
| `authenticateViaCliWarning` | Authenticate via GitHub CLI on Devin’s machine. Some features, including Devin Review, will not be available. |
| `authority` | By accepting, you confirm you’re authorized to accept these terms on behalf of your account. |
| `awaitingResponseDetails` | Devin is awaiting your response. Type 'SLEEP' to put Devin to sleep. Devin will auto-sleep after a period of i |
| `bannerBody` | Automations supports schedules and more, including event-driven triggers. Migrate this organization's schedule |
| `binaryFile` | The file is not displayed in the text editor because it is either binary or uses an unsupported text encoding. |
| `blockedDescription` | Plugins marked as blocked by policy, including dependencies from the latest index. |
| `bodyAndroid` | This account isn't on the Android beta yet. Ask your Devin contact to enable it for you. |
| `bodyMcpOfficial` | Devin will be allowed to run this plugin's rules, hooks, and skills, including access to external data through |
| `bodyOfficial` | Devin will be allowed to run this plugin's rules, hooks, and skills. Only proceed if you trust this plugin. |
| `bugDetectionDesc` | Identifies potential bugs and flags parts of the code worth reviewing more carefully. |
| `bulkPii` | Bulk PII — more than 5,000 individual user records, as defined <definitionLink>here</definitionLink>. |
| `bulkPlaceholder` | API_KEY=your-api-key-here # Use this API Key for GitHub
DATABASE_URL=postgresql://user:pass@localhost:5432/db  |
| `button` | text-text-primary [@media(any-hover:hover)]:group-hover/menu-item:text-text-primary group-has-[[data-popup-ope |
| `bypassRulesDialogDescription` | This pull request does not meet the repository's merge requirements. Your GitHub account is allowed to bypass  |
| `canConfigureDescription` | Can view, disable and delete this automation, and edit it if they can also run it |
| `canConfigureDescriptionRunsAsCreator` | Can view, disable and delete this automation. Only its creator can edit it, because it runs as them |
| `canonicalEditorDescription` | The canonical blueprint for this repository. Environments that follow it run this setup. |
| `capabilityCardChatGPTSubError` | Your ChatGPT plan can't be used right now. <manageLink>Check your connection</manageLink>. |
| `capabilityCardChatGPTSubReconnectRequired` | Your ChatGPT connection has expired. <manageLink>Reconnect</manageLink> to use your plan. |
| `capabilityCardGptSubscription` | You're currently using your ChatGPT subscription. <manageLink>Manage</manageLink> |
| `changes` | _clock |
| `chatgptIdentityMismatch` | This Devin account is linked to a different ChatGPT account. Sign in with the linked ChatGPT account or use an |
| `chatgptLinkRequired` | A Devin account already uses this email. Sign in with your existing method, then link ChatGPT on the Connectio |
| `chatgptSsoRequired` | This account requires SSO and can’t be linked to ChatGPT. Sign in using your organization’s SSO. |
| `claimedBody` | A worker in your outpost accepted this session and is connecting. Devin is ready and will start as soon as you |
| `cloudDescription` | Applies to Devin sessions and Devin Review only. Devin Desktop and Terminal CLI usage is not counted toward th |
| `coachEmpty` | Devin coaches your team as they prompt and work. Suggestion outcomes will appear here. |
| `collectionActionsNote` | Move and Delete only apply to resources, so they're hidden while a collection is selected. |
| `collectionSelectedNote` | A selected collection covers everything inside it, including resources added later. |
| `combinedDescription` | Applies to usage across all products: Devin sessions, Devin Review, Devin Desktop, and Terminal CLI. |
| `combinedFieldDescription` | Counts usage across Devin sessions, Devin Review, Devin Desktop, and Terminal CLI |
| `commitPerFile` | This git provider commits one file at a time, so each file becomes its own commit with this message. |
| `commitUnsupported` | Committing changes isn't supported for this git provider yet. Apply the proposed changes manually. |
| `companyGraphDescription` | What Devin knows about your organization: repositories, tools and where things are discussed. Updated nightly, |
| `complianceApprovedPurposes` | This System is authorized for approved business purposes only; any other use is prohibited. |
| `complianceDisciplinary` | Unauthorized use of this System or non-compliance with these rules may result in disciplinary action. |
| `complianceMonitored` | Activities on this System will be monitored and recorded to the extent permitted by local law. |
| `complianceNoProduction` | Use of this System or its outputs for any Citi production-related activity is not authorized. |
| `confidentialUpdate` | ⚠️ Update: Devin supports Confidential data. Standard handling, need-to-know, and entitlement requirements con |
| `configureOnce` | Configure it once — sessions in the organizations you target get it automatically. |
| `confirmDisableDescription` | Devin stops syncing this connection with GitLab. Grants already created by sync are left as they are until syn |
| `confirmNotRequired` | Acceptance will not be required for this account. Existing evidence will be retained. |
| `confirmPrivateSyncDescription` | This session is private. Everyone in that Slack channel can see its new messages. |
| `confirmRequired` | Accounts without acceptance of this terms URL and link label will be gated. Changing either requires a new acc |
| `conflictWarning` | There is a conflict with another change to the knowledge. The update must be made manually. |
| `connectReposOrUpgrade` | Connect your repositories to try Devin for free or <upgradeButton>upgrade your plan</upgradeButton> |
| `connectionsDescription` | The git hosts this enterprise connects to, and the route git-manager takes to reach each one. |
| `content` | Paste cookie JSON directly, or a pre-encoded base64 string of semicolon-delimited JSON objects |
| `copyMoveDesc` | Automatically detects when code is moved or copied, and shows you where it came from. |
| `coreUpgradeTeams` | Any usage you already paid for remains available. For additional paid Devin usage, you'll need to upgrade to < |
| `createAutomationPrompt` | Help me create an automation. Ask me what routine work I want handled and when it should run, then set it up. |
| `createDescription` | Devin can build and deploy apps behind a stable URL for everyone in your organization. |
| `createWithDevinPrompt` | Devin, please help me create billing tags based on the following sources

[upload attachments and include link |
| `createdWithoutToken` | Service user created. Static keys are disabled for this account, so no token was issued. |
| `customHeadersHint` | Optional headers sent with every request to this server. Values are write-only: editing headers replaces the w |
| `customSubtitle` | Point Devin at an MCP server you run yourself. Configure it once — sessions in the organizations you target ge |
| `customerChannelUrlHelper` | e.g. the shared Slack channel the customer can also use. Shown with its label, including while live support is |
| `dedupeKeyHelp` | At most one pending job per task, account and key; a duplicate is skipped, not queued. |
| `defaultBranch` | The main branch of the repository (e.g., 'main' or 'master'). Devin will default to working off this branch. |
| `defaultSuffix` | (default) |
| `deleteDescription` | This will delete the blueprint for this repository. This action cannot be undone. |
| `deletePluginDescription` | This plugin was uploaded here, so it has no other copy. Its files are permanently deleted. This cannot be undo |
| `deleteProjectConfirm` | Are you sure you want to delete this project? This will remove all associated commands and configurations. |
| `descriptionQueue` | Holds back dispatch of every job on this queue. Takes effect within about a second, with no deploy. Held jobs  |
| `descriptionTask` | Holds back dispatch of this task's jobs. Takes effect within about a second, with no deploy. Held jobs stay qu |

