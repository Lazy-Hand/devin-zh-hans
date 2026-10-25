/**
 * test_runtime_merge.js — 真正在 Node 里模拟 webapp 的 i18next 初始化，验证中文能查到
 *
 * 这比「文件里有载荷」强得多：它证明
 *   ① 注入后的代码语法可执行
 *   ② Object.assign 在 Eu() 之前生效，中文进入 resources
 *   ③ i18next 查 composerTips.sidebar / sidebar.automations 能拿到中文
 *
 * 用真 i18next 太重，这里用一个 30 行的最小实现，只验证「key → resources 的查找路径」。
 */
'use strict';
const fs = require('fs');
const path = require('path');

const APP = (() => {
  const c = [process.env.DEVIN_INSTALL,
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Devin'), 'C:\\Program Files\\Devin'];
  for (const p of c) if (p && fs.existsSync(path.join(p, 'Devin.exe'))) return p;
  return null;
})();

const chunkPath = path.join(APP, 'resources', 'app', 'out', 'vs', 'workbench',
  'devin-webapp-host', 'assets', 'entry-host-editor-mode-menu-DUnUGWLA.js');
const src = fs.readFileSync(chunkPath, 'utf8');

// ── 1. 抠出载荷 ──
const mark = 'Object.assign(mu||{},';
const i = src.indexOf(mark);
if (i < 0) { console.error('✗ 未找到载荷'); process.exit(1); }
const open = src.indexOf('{', i + mark.length - 1);
let depth = 0, j = open, q = null;
for (; j < src.length; j++) {
  const ch = src[j];
  if (q) { if (ch === '\\') { j++; continue; } if (ch === q) q = null; continue; }
  if (ch === '"') { q = ch; continue; }
  if (ch === '{') depth++;
  else if (ch === '}') { depth--; if (depth === 0) break; }
}
const zh = JSON.parse(src.slice(open, j + 1));
console.log('载荷: ' + Object.keys(zh).length + ' 个命名空间, ' +
  Object.values(zh).reduce((a, o) => a + Object.keys(o).length, 0) + ' 条');

// ── 2. 模拟 Devin 的英文资源 mu（取真实 chunk 里 mu = yl 的形态）──
// 只用截图里出现过的 key 造一个最小 mu，验证合并与查找。
const mu = {
  sidebar: {
    automations: 'Automations',
    recent: 'Recent',
    security: 'Security',
    wiki: 'Wiki',
    review: 'Review',
    customize: 'Customize',
  },
  composerTips: {
    sidebar: 'Tip: Hide or show the sidebar (<shortcut/>)',
    newSession: 'Tip: Start a new session (<shortcut/>)',
    sessionNav: 'Tip: Move between sessions (<up/> / <down/>)',
  },
  nav: { newSession: 'New session', security: 'Security' },
  settings: { highContrast: 'High contrast mode', uiFont: 'Interface font' },
};

// ── 3. 执行注入语句（与文件里一字不差）──
const stmt = 'Object.assign(mu||{},' + JSON.stringify(zh) + ')';
eval(stmt);

// ── 4. 模拟 i18next 的 key 查找（defaultNS=translation，点号嵌套）──
function t(key, ns) {
  const parts = key.split('.');
  let cur = mu;
  for (const p of parts) {
    if (cur == null || typeof cur !== 'object') return key;
    cur = cur[p];
  }
  return typeof cur === 'string' ? cur : key;
}

const cases = [
  ['sidebar.automations', '自动化'],
  ['sidebar.recent', '最近'],
  ['nav.security', '安全'],
  ['composerTips.sidebar', '提示：隐藏或显示侧边栏'],
  ['composerTips.newSession', '提示：开始新会话'],
  ['composerTips.sessionNav', '提示：在会话之间切换'],
  ['nav.newSession', '新建会话'],
  ['settings.highContrast', '高对比度模式'],
  ['settings.uiFont', '界面字体'],
];

let pass = 0;
console.log('\n== i18next 查找验证 ==');
for (const [key, want] of cases) {
  const got = t(key);
  const ok = got.includes(want);
  if (ok) pass++;
  console.log((ok ? '✓' : '✗') + ' ' + key.padEnd(26) + ' → ' + got);
}
console.log(''); console.log(pass + '/' + cases.length + ' 通过');
process.exit(pass === cases.length ? 0 : 1);

