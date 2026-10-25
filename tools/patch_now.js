/**
 * patch_now.js — 直接在当前安装上执行第 3 层注入（供调试用，正式路径仍是 extension.js）
 *
 * 用法:
 *   node tools/patch_now.js            # 对真实安装执行
 *   node tools/patch_now.js --dry      # 只报告会做什么
 *   node tools/patch_now.js --restore  # 从备份恢复
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DRY = process.argv.includes('--dry');
const RESTORE = process.argv.includes('--restore');

const APP = (() => {
  const c = [process.env.DEVIN_INSTALL,
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Devin'), 'C:\\Program Files\\Devin'];
  for (const p of c) if (p && fs.existsSync(path.join(p, 'Devin.exe'))) return p;
  return null;
})();
if (!APP) { console.error('✗ 未找到 Devin 安装'); process.exit(1); }

const DIR = path.join(APP, 'resources', 'app', 'out', 'vs', 'workbench', 'devin-webapp-host', 'assets');
const MARK = '/*devin-zh*/';
const END = '/*/devin-zh*/';
const ANCHOR = 'Mt.isInitialized||Eu()';

const chunk = path.join(DIR, 'entry-host-editor-mode-menu-DUnUGWLA.js');
if (!fs.existsSync(chunk)) { console.error('✗ chunk 不存在'); process.exit(1); }

const BACKUP = path.join(ROOT, '.backup', path.basename(chunk));
fs.mkdirSync(path.dirname(BACKUP), { recursive: true });

if (RESTORE) {
  if (!fs.existsSync(BACKUP)) { console.error('✗ 无备份'); process.exit(1); }
  fs.copyFileSync(BACKUP, chunk);
  console.log('✓ 已从备份恢复', path.basename(chunk));
  process.exit(0);
}

// 首次运行时留存干净副本
if (!fs.existsSync(BACKUP)) {
  fs.copyFileSync(chunk, BACKUP);
  console.log('已备份原始 chunk ->', path.relative(ROOT, BACKUP));
}

const zh = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets', 'webapp-i18n.json'), 'utf8'));
const payload = MARK + 'Object.assign(mu||{},' + JSON.stringify(zh) + ')' + END;

let s = fs.readFileSync(chunk, 'utf8');
const sizeBefore = s.length;

// 1) 去掉旧载荷（含旧式把锚点吞进去的那种）
const a0 = s.indexOf(MARK);
const b0 = s.indexOf(END);
if (a0 >= 0 && b0 > a0) {
  s = s.slice(0, a0) + s.slice(b0 + END.length);
  console.log('已移除旧载荷');
}

// 2) 若锚点被旧载荷一起吃掉，从备份里补回来
if (!s.includes(ANCHOR)) {
  const orig = fs.readFileSync(BACKUP, 'utf8');
  if (orig.includes(ANCHOR) && s.includes('cL=s(),')) {
    s = s.replace('cL=s(),', 'cL=s(),' + ANCHOR + ',');
    console.log('已从备份恢复锚点');
  } else {
    // 退一步：直接在 webapp 初始化闭包末尾补锚点调用
    s = s.replace(/(cL=s\(\),)\s*/, '$1' + ANCHOR + ',');
    console.log('已补回锚点');
  }
}

// 3) 在锚点之前插入载荷
const at = s.indexOf(ANCHOR);
if (at < 0) { console.error('✗ 仍找不到锚点，放弃'); process.exit(1); }
s = s.slice(0, at) + payload + ',' + s.slice(at);

if (!DRY) fs.writeFileSync(chunk, s, 'utf8');
console.log('%s %s  %d -> %d 字节  命名空间 %d 条',
  DRY ? '(dry)' : '✓ 已写入', path.basename(chunk), sizeBefore, s.length, Object.keys(zh).length);
console.log('注入点:', JSON.stringify(s.slice(Math.max(0, s.indexOf(MARK) - 70), s.indexOf(MARK) + 40)));
