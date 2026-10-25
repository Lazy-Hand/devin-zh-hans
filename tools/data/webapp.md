# webapp-host（新版 Agent UI）i18n 资源与词典覆盖

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
