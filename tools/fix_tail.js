/**
 * fix_tail.js — 修复载荷尾部的多余逗号
 *
 * patch_now.js 把载荷插到了 `Mt.isInitialized||Eu(),` 这个位置（锚点后面本来就有逗号），
 * 写回时变成 `…}),Mt.isInitialized||Eu(),}` —— 锚点后遗留的逗号成了尾逗号，语法错误。
 *
 * 修复：把 `,Mt.isInitialized||Eu(),}` 收敛成 `,Mt.isInitialized||Eu()}`。
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
const chunk = path.join(APP, 'resources', 'app', 'out', 'vs', 'workbench',
  'devin-webapp-host', 'assets', 'entry-host-editor-mode-menu-DUnUGWLA.js');

let s = fs.readFileSync(chunk, 'utf8');
const before = s.length;

// 锚点后紧跟 `,}` 就是尾逗号
const bad = /(Mt\.isInitialized\|\|Eu\(\)),(\s*\})/g;
let n = 0;
s = s.replace(bad, (m, a, b) => { n++; return a + b; });

// 顺带兜底：载荷末尾 `),` 紧接 `}` 的情况
const bad2 = /(\/\*\/devin-zh\*\/),(\s*\})/g;
s = s.replace(bad2, (m, a, b) => { n++; return a + b; });

if (n === 0) {
  console.log('没有发现尾逗号，未改动');
} else {
  fs.writeFileSync(chunk, s, 'utf8');
  console.log('✓ 修复 %d 处尾逗号  %d -> %d 字节', n, before, s.length);
}
