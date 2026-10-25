/**
 * probe_order.py 的替代：直接确认「中文是被谁覆盖掉的」
 *
 * Eu() 里：
 *     let n={en:{translation: t?JSON.parse(JSON.stringify(mu)):mu, review:hu}};
 *     Mt.use(Mn).init({resources:n, lng:"en", ns:["translation","review"], defaultNS:"translation"})
 *     t && Mt.addResourceBundle("en","translation",t,!0,!0)
 *     return Mt
 *
 * 我们的注入：
 *     Mt.isInitialized||Eu(), Mt.addResourceBundle("en","translation",{…},!0,!0)
 *
 * 看起来没问题：init 之后 addResourceBundle。但如果 lL() 在组件挂载前被调用多次，
 * 或者 i18next 的 addResourceBundle 在 init 完成前（initAsync 默认 true）就发了，
 * bundle 会被 init 时的 resources 覆盖掉 —— 这正是「载荷存在但界面没生效」。
 *
 * 正确做法：把中文合并到 **resources 对象本身**，也就是在 Eu() 调用前改写 mu。
 * 本脚本验证：mu 是不是一个可以直接 Object.assign 的普通对象。
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
const DIR = path.join(APP, 'resources', 'app', 'out', 'vs', 'workbench', 'devin-webapp-host', 'assets');
const CH = path.join(DIR, 'entry-host-editor-mode-menu-DUnUGWLA.js');
const s = fs.readFileSync(CH, 'utf8');

const i = s.indexOf('function Eu({pseudoLocale');
console.log('Eu() 原文:');
console.log(s.slice(i, i + 560));
console.log('\n--- 关键判断 ---');
console.log('initAsync 是否被显式关闭:', /initAsync\s*:/.test(s.slice(i, i + 800)));
console.log('addResourceBundle 在 init 同一表达式内:', /init\(\{[\s\S]{0,700}addResourceBundle/.test(s.slice(i, i + 900)));
