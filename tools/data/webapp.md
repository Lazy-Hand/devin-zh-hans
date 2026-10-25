# webapp-host（新版 Agent UI）i18n 资源与词典覆盖

- i18n chunk: `entry-host-editor-mode-menu-DUnUGWLA.js`
- 命名空间: **317**
- 叶子 key: **19,269**
- 去重后英文原文: **15,361**
- 词典已覆盖: **8,358** (54.4%)
- 仍缺中文: **7,003**（其中可整串替换 6,864）

## 最大的命名空间

| 条数 | 命名空间 |
|---:|---|
| 3938 | `settings` |
| 1288 | `automations` |
| 706 | `transcript` |
| 617 | `worklog` |
| 592 | `analyticsRevamp` |
| 535 | `billing` |
| 368 | `sidebar` |
| 358 | `oncall` |
| 343 | `readiness` |
| 339 | `boards` |
| 307 | `bots` |
| 277 | `admin` |
| 269 | `onboarding` |
| 252 | `apps` |
| 248 | `scopedTriggers` |

## 缺口样例（前 60）

| 命名空间 | key | 英文 |
|---|---|---|
| `defaultPrimaryBillingOrg` | `description` | Applies when a user has no primary billing organization. Existing assignments and organization acces |
| `adminBudgetBackfill` | `account` | Account: {{accountId}} |
| `adminBudgetBackfill` | `description` | Sync eligible orgs to budgets with the current feature flags. This can create budgets and replace or |
| `adminBudgetBackfill` | `success` | Budget backfill complete in {{duration}} seconds. |
| `adminBudgetBackfill` | `failure` | Budget backfill request failed. If the connection was lost, the changes may have committed. {{error} |
| `adminBudgetBackfill` | `confirmDescription` | Sync eligible orgs for {{accountId}} to budgets. This can create budgets and replace org-linked budg |
| `adminGovernance` | `rollout.description` | Run the grants rollout backfills for this account as background jobs, in order, with the account's U |
| `adminGovernance` | `rollout.runStep` | Run {{step}} |
| `adminGovernance` | `rollout.succeeded` | Succeeded {{time}} |
| `adminGovernance` | `rollout.failed` | Failed {{time}} |
| `adminGovernance` | `rollout.confirmTitle` | Run {{step}}? |
| `adminGovernance` | `rollout.confirmDescription` | Runs {{step}} for {{accountId}} in a background job. Committed batches stay if it fails. |
| `adminGovernance` | `rollout.confirmDescriptionAll` | Runs all {{count}} backfills for {{accountId}} in order, one job each. The chain stops at the first  |
| `adminGovernance` | `rollout.confirmDescriptionBitmaps` | Runs {{step}} for {{accountId}} in a background job, as one transaction. Grant changes for this acco |
| `adminGovernance` | `rollout.abortStep` | Abort {{step}} |
| `adminGovernance` | `rollout.abortConfirmTitle` | Abort {{step}}? |
| `adminGovernance` | `rollout.abortConfirmDescription` | Stops {{step}} for {{accountId}} within a few seconds. Committed batches stay and the step fails, so |
| `adminJobs` | `actionsNamed` | Actions for {{name}} |
| `adminJobs` | `batch.help` | Each entry has args matching the task's schema and an optional dedupe_key. Up to 100,000 entries / 6 |
| `adminJobs` | `batch.ready_one` | {{count}} entry ready |
| `adminJobs` | `batch.ready_other` | {{count}} entries ready |
| `adminJobs` | `batch.confirmTitle_one` | Enqueue {{count}} entry? |
| `adminJobs` | `batch.confirmTitle_other` | Enqueue {{count}} entries? |
| `adminJobs` | `batch.confirmDescription` | Run {{task}} for every valid entry. Each job uses the account from its arguments, or the system acco |
| `adminJobs` | `batch.progress` | {{processed}} / {{total}} entries processed: {{enqueued}} enqueued, {{skipped}} deduplicated, {{fail |
| `adminJobs` | `batch.stopped` | Upload stopped. Some jobs in the last request may have committed without a confirmed response. Later |
| `adminJobs` | `batch.entryError` | Entry {{index}}: {{detail}} |
| `adminJobs` | `breakGlass.queues` | Paused queues: {{names, list}} |
| `adminJobs` | `breakGlass.tasks` | Paused tasks and crons: {{names, list}} |
| `adminJobs` | `breakGlass.reason` | Reason: {{reason}} |
| `adminJobs` | `breakGlass.source` | Set in {{location}}, not on this page. It applies on top of the holds below. Delete the file to lift |
| `adminJobs` | `breakGlass.unreadable` | The break-glass file {{location}} can't be used: {{error}}. Dispatchers and workers keep the last ve |
| `adminJobs` | `breakGlass.checkFailed` | Couldn't check the break-glass pause: {{error}}. A pause may be on. |
| `adminJobs` | `control.pauseOrCapNamed` | Pause / cap {{name}} |
| `adminJobs` | `control.title` | Pause or cap {{name}} |
| `adminJobs` | `control.saved` | Hold on {{name}} saved |
| `adminJobs` | `control.lifted` | Hold on {{name}} lifted |
| `adminJobs` | `control.paused` | paused |
| `adminJobs` | `control.capped` | max {{count}} in flight |
| `adminJobs` | `control.scopeQueue` | queue |
| `adminJobs` | `control.scopeTask` | task |
| `adminJobs` | `control.editNamed` | Edit {{name}} |
| `adminJobs` | `control.liftNamed` | Lift hold on {{name}} |
| `adminJobs` | `taskRequeueTitle` | Requeue failed jobs for {{task}} on {{queue}} |
| `adminJobs` | `taskRequeued_one` | Requeued {{count}} failed job for {{task}} on {{queue}} |
| `adminJobs` | `taskRequeued_other` | Requeued {{count}} failed jobs for {{task}} on {{queue}} |
| `adminJobs` | `taskRemaining` | {{done}}; {{remaining}} still failed (run again to continue) |
| `adminJobs` | `enqueue.descriptionSingle` | Same path as app.jobs.enqueue() in code. The audit log records task, queue and account, not the argu |
| `adminJobs` | `enqueue.maxAttempts_one` | max {{count}} attempt |
| `adminJobs` | `enqueue.maxAttempts_other` | max {{count}} attempts |
| `adminJobs` | `enqueue.timeout` | timeout {{seconds}}s |
| `adminJobs` | `enqueue.invalidJson` | Invalid JSON: {{detail}} |
| `adminJobs` | `enqueue.confirmTitle` | Enqueue {{task}} |
| `adminJobs` | `enqueue.deduplicated` | Not enqueued: a pending {{task}} job with this dedupe key already exists |
| `adminJobs` | `enqueue.enqueued` | Enqueued job {{jobId}} on {{queue}} |
| `adminJobs` | `info.openNamed` | Details for {{name}} |
| `adminJobs` | `info.holdSetBy` | Set by {{by}} at {{at}} |
| `accountTerms` | `description` | Before using Devin, an admin needs to accept the terms for this account. One acceptance covers every |
| `accountTerms` | `account` | Account: {{accountName}} |
| `mcpConfiguration` | `oauth` | OAuth |
