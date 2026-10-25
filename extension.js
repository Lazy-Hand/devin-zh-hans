/**
 * Devin 简体中文 —— 扩展运行时
 *
 * 四层落地，全程幂等：
 *   1) 语言包层：把合并版 main.i18n.json（官方译文 + 本插件补齐的缺口）写进已安装的
 *      官方 zh-hans 语言包。VS Code 在同一 locale 下按扩展顺序合并 translations，
 *      官方包 ms-ceintl.* 排序在后会把我们的 vscode bundle 盖掉，所以必须硬覆盖。
 *   2) 扩展贡献点层：Devin 内置的 5 个扩展（windsurf / windsurf-dev-containers /
 *      windsurf-remote-*）把命令标题与设置说明硬编码在 package.json 里，且没有
 *      package.nls*.json，语言包机制无效。这里写 package.nls.json + package.nls.zh-cn.json，
 *      并把 package.json 的字符串换成 %key%。
 *   3) webapp i18next 层：Agent UI（out/vs/workbench/devin-webapp-host/）自建 i18next，
 *      只有 en/ja/pt/es 没有 zh。把中文按英文 key 深合并进它的 en 资源。
 *   4) DOM 层：往 workbench.html / sessions.html 注入 devin-zh-dom.js，
 *      覆盖运行时数据拼出来的文案（Agent 侧边栏、会话窗口、菜单）。
 *
 * 第 2/3 层会改到 product.json.checksums 里的文件，所以每次写完都同步哈希，
 * 避免 Devin 启动时报「安装似乎损坏」。
 */
'use strict';
const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const TAG = '[devin-zh]';
const log = (...a) => console.log(TAG, ...a);
const BACKUP_ROOT = path.join(process.env.DEVIN_HOME || path.join(os.homedir(), '.devin'), 'devin-zh-backups');

// 需要注入 DOM 翻译器的窗口
const PAGES = [
  ['out/vs/code/electron-browser/workbench/workbench.html', './workbench.js'],
  ['out/vs/sessions/electron-browser/sessions.html', './sessions.js'],
];

// Devin 内置扩展：package.json 里的贡献点需要 %key% 化
const EXT_FAMILY = [
  'windsurf',
  'windsurf-dev-containers',
  'windsurf-remote-devin',
  'windsurf-remote-openssh',
  'windsurf-remote-wsl',
];

// ───────────────────────── 环境探测 ─────────────────────────
// DEVIN_INSTALL / DEVIN_HOME 供 tools/verify_layers.js 指向沙盒副本；
// 正常使用时留空，走标准探测。
function devinHome() {
  return process.env.DEVIN_HOME || path.join(os.homedir(), '.devin');
}

function findDevinInstall() {
  const cands = [
    process.env.DEVIN_INSTALL,
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Devin'),
    'C:\\Program Files\\Devin',
  ];
  for (const c of cands) {
    if (c && fs.existsSync(path.join(c, 'Devin.exe'))) return c;
  }
  return null;
}

function findLangpack() {
  const root = path.join(devinHome(), 'extensions');
  if (!fs.existsSync(root)) return null;
  for (const d of fs.readdirSync(root)) {
    if (/language-pack-zh-hans/.test(d)) {
      const p = path.join(root, d);
      if (fs.existsSync(path.join(p, 'translations', 'main.i18n.json'))) return p;
    }
  }
  return null;
}

function sha256b64(p) {
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('base64').replace(/=+$/, '');
}

function sameFile(a, b) {
  try {
    if (!fs.existsSync(a) || !fs.existsSync(b)) return false;
    if (fs.statSync(a).size !== fs.statSync(b).size) return false;
    return fs.readFileSync(a).equals(fs.readFileSync(b));
  } catch { return false; }
}

function sameJson(a, b) {
  try {
    return JSON.stringify(a) === JSON.stringify(b);
  } catch { return false; }
}

function backup(p, tag) {
  try {
    if (!fs.existsSync(p)) return;
    const d = path.join(BACKUP_ROOT, 'vsix-' + tag);
    fs.mkdirSync(d, { recursive: true });
    const dst = path.join(d, path.basename(p));
    if (!fs.existsSync(dst)) fs.copyFileSync(p, dst);
  } catch (e) { log('备份失败(忽略):', e.message); }
}

function readJson(p) {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
}

function writeJson(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, '\t'), 'utf8');
}

// ───────────────────────── 第 1 层：语言包落地 ─────────────────────────
function applyLanguagePack(ctx) {
  const lp = findLangpack();
  if (!lp) {
    log('未检测到官方中文语言包 —— VSIX 自带的 localizations 会直接生效。');
    return { langpack: false, changed: false };
  }
  const src = path.join(ctx.extensionPath, 'translations', 'main.i18n.json');
  const dst = path.join(lp, 'translations', 'main.i18n.json');
  let changed = false;

  if (!sameFile(src, dst)) {
    backup(dst, 'langpack');
    fs.copyFileSync(src, dst);
    log('已写入合并版 main.i18n.json');
    changed = true;
  }

  // windsurf 扩展的贡献点 bundle（兼容只认语言包、不认 package.nls 的旧路径）
  const wsSrc = path.join(ctx.extensionPath, 'translations', 'extensions', 'windsurf.i18n.json');
  const wsDst = path.join(lp, 'translations', 'extensions', 'windsurf.i18n.json');
  if (fs.existsSync(wsSrc) && !sameFile(wsSrc, wsDst)) {
    backup(wsDst, 'langpack');
    fs.mkdirSync(path.dirname(wsDst), { recursive: true });
    fs.copyFileSync(wsSrc, wsDst);
    log('已写入 windsurf.i18n.json');
    changed = true;
  }

  // 在语言包清单里注册 windsurf bundle（幂等）
  const pkgPath = path.join(lp, 'package.json');
  try {
    const pkg = readJson(pkgPath);
    const locs = pkg && pkg.contributes && pkg.contributes.localizations;
    if (Array.isArray(locs) && locs[0]) {
      locs[0].translations = locs[0].translations || [];
      if (!locs[0].translations.some((t) => t.id === 'windsurf')) {
        backup(pkgPath, 'langpack');
        locs[0].translations.push({
          id: 'windsurf',
          path: './translations/extensions/windsurf.i18n.json',
        });
        writeJson(pkgPath, pkg);
        log('已在语言包清单注册 windsurf bundle');
        changed = true;
      }
    }
  } catch (e) { log('注册 bundle 失败:', e.message); }

  return { langpack: true, changed };
}

// ───────────────────────── 第 2 层：内置扩展贡献点 ─────────────────────────
function setByPath(obj, parts, value) {
  let cur = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    const k = parts[i];
    if (cur[k] === undefined || cur[k] === null) return false;
    cur = cur[k];
  }
  const last = parts[parts.length - 1];
  if (cur[last] === undefined) return false;
  cur[last] = value;
  return true;
}

function getByPath(obj, parts) {
  let cur = obj;
  for (const k of parts) {
    if (cur === undefined || cur === null) return undefined;
    cur = cur[k];
  }
  return cur;
}

function applyExtensionManifests(ctx) {
  const inst = findDevinInstall();
  if (!inst) return { ext: false, changed: false };

  const planPath = path.join(ctx.extensionPath, 'assets', 'ext-manifest.json');
  const enPath = path.join(ctx.extensionPath, 'assets', 'ext-manifest.en.json');
  const zhPath = path.join(ctx.extensionPath, 'assets', 'ext-manifest.zh.json');
  const plan = readJson(planPath);
  const enMap = readJson(enPath);
  const zhMap = readJson(zhPath);
  if (!plan || !enMap) { log('缺少 ext-manifest 产物，跳过扩展贡献点层'); return { ext: false, changed: false }; }

  const extRoot = path.join(inst, 'resources', 'app', 'extensions');
  let changed = false;

  for (const name of EXT_FAMILY) {
    const entries = plan[name];
    if (!Array.isArray(entries) || !entries.length) continue;
    const dir = path.join(extRoot, name);
    const pkgPath = path.join(dir, 'package.json');
    if (!fs.existsSync(pkgPath)) continue;

    const pkg = readJson(pkgPath);
    if (!pkg) continue;

    // 2a) 两个 nls 文件
    const nlsEn = {};
    const nlsZh = {};
    for (const e of entries) {
      const en = enMap[e.key];
      if (typeof en !== 'string') continue;
      nlsEn[e.key] = en;
      const zh = zhMap[e.key];
      if (typeof zh === 'string') nlsZh[e.key] = zh;
    }
    const pEn = path.join(dir, 'package.nls.json');
    const pZh = path.join(dir, 'package.nls.zh-cn.json');
    if (!sameJson(readJson(pEn), nlsEn)) {
      backup(pEn, 'ext');
      writeJson(pEn, nlsEn);
      changed = true;
    }
    if (!sameJson(readJson(pZh), nlsZh)) {
      backup(pZh, 'ext');
      writeJson(pZh, nlsZh);
      changed = true;
    }

    // 2b) package.json 里的字符串换成 %key%
    let dirty = false;
    for (const e of entries) {
      const cur = getByPath(pkg, e.path);
      if (typeof cur !== 'string') continue;
      if (cur === '%' + e.key + '%') continue;
      if (setByPath(pkg, e.path, '%' + e.key + '%')) dirty = true;
    }
    if (dirty) {
      backup(pkgPath, 'ext');
      writeJson(pkgPath, pkg);
      log('已本地化扩展贡献点: ' + name + ' (' + entries.length + ' 个字段)');
      changed = true;
    }
  }
  return { ext: true, changed };
}

// ───────────────────────── 第 3 层：webapp i18next ─────────────────────────
// webapp-host 的 i18n 入口在 entry-host-editor-mode-menu-*.js：
//     function Eu({pseudoLocale:e=!1,englishOverrides:t}={}){
//       ... Mt.use(Mn).init({resources:n, lng:"en", fallbackLng:"en", ...}),
//       t && Mt.addResourceBundle("en","translation",t,!0,!0), Mt }
//     ...
//     Mt.isInitialized||Eu()
// 也就是：Devin 自己只注册 en/ja/pt/es，英文资源在 en 命名空间下。
// 做法是把锚点那句扩成「初始化 + 把中文深合并进 en 资源」：
//     Mt.isInitialized||Eu(), Mt.addResourceBundle("en","translation",{...},!0,!0)
// 不新增 locale、不改 lng、不动任何组件代码，因此也不会影响 ja/pt/es 用户。
const WEBAPP_DIR = 'out/vs/workbench/devin-webapp-host';
const HOST_ANCHOR = 'Mt.isInitialized||Eu()';
const HOST_MARK = '/*devin-zh*/';
const HOST_END = '/*/devin-zh*/';

function findHostChunk(app) {
  const dir = path.join(app, WEBAPP_DIR, 'assets');
  if (!fs.existsSync(dir)) return null;
  for (const f of fs.readdirSync(dir)) {
    if (!f.startsWith('entry-host-editor-mode-menu') || !f.endsWith('.js')) continue;
    const p = path.join(dir, f);
    try {
      if (fs.readFileSync(p, 'utf8').includes(HOST_ANCHOR)) return p;
    } catch { }
  }
  return null;
}

function applyWebappI18n(ctx) {
  const inst = findDevinInstall();
  if (!inst) return { webapp: false, changed: false };
  const app = path.join(inst, 'resources', 'app');

  const zh = readJson(path.join(ctx.extensionPath, 'assets', 'webapp-i18n.json'));
  if (!zh) { log('缺少 webapp-i18n.json，跳过 webapp 层'); return { webapp: false, changed: false }; }

  const chunk = findHostChunk(app);
  if (!chunk) {
    log('未找到 webapp-host 的 i18n 入口（Devin 版本可能已变更），跳过 webapp 层');
    return { webapp: false, changed: false };
  }

  const payload = HOST_MARK
    + 'Mt.isInitialized||Eu(),Mt.addResourceBundle("en","translation",'
    + JSON.stringify(zh) + ',!0,!0)'
    + HOST_END;

  let s = fs.readFileSync(chunk, 'utf8');

  // 已注入：只替换载荷（译文随插件升级而变）
  const a = s.indexOf(HOST_MARK);
  const b = s.indexOf(HOST_END);
  if (a >= 0 && b > a) {
    const old = s.slice(a, b + HOST_END.length);
    if (old === payload) return { webapp: true, changed: false };
    backup(chunk, 'webapp');
    fs.writeFileSync(chunk, s.slice(0, a) + payload + s.slice(b + HOST_END.length), 'utf8');
    log('已更新 webapp i18next 覆盖载荷');
    return { webapp: true, changed: true };
  }

  const at = s.indexOf(HOST_ANCHOR);
  if (at < 0) return { webapp: false, changed: false };
  backup(chunk, 'webapp');
  s = s.slice(0, at) + payload + s.slice(at + HOST_ANCHOR.length);
  fs.writeFileSync(chunk, s, 'utf8');
  log('已注入 webapp i18next 覆盖（' + Object.keys(zh).length + ' 个命名空间根）');
  return { webapp: true, changed: true };
}

// ───────────────────────── 第 4 层：DOM 翻译器 ─────────────────────────
function applyDomLayer(ctx) {
  const inst = findDevinInstall();
  if (!inst) { log('未找到 Devin 安装目录，跳过 DOM 层'); return { dom: false, changed: false }; }
  const app = path.join(inst, 'resources', 'app');
  const runtimeSrc = path.join(ctx.extensionPath, 'dist', 'devin-zh-dom.js');
  const productPath = path.join(app, 'product.json');
  const product = readJson(productPath);

  let changed = false;
  for (const [rel, anchor] of PAGES) {
    const html = path.join(app, rel);
    if (!fs.existsSync(html)) continue;
    const jsName = 'devin-zh-dom.js';
    const jsDst = path.join(path.dirname(html), jsName);

    if (!sameFile(runtimeSrc, jsDst)) {
      try {
        fs.writeFileSync(jsDst, fs.readFileSync(runtimeSrc));
        log('已写入 ' + rel.replace(/\/[^/]+$/, '/') + jsName);
        changed = true;
      } catch (e) { log('写入运行时失败:', e.message); continue; }
    }

    let s = '';
    try { s = fs.readFileSync(html, 'utf8'); } catch { continue; }
    const tag = '<script src="./' + jsName + '"></script>';
    if (!s.includes(tag)) {
      const a = '<script src="' + anchor + '" type="module"></script>';
      if (!s.includes(a)) { log('HTML 锚点缺失: ' + rel); continue; }
      backup(html, 'dom');
      fs.writeFileSync(html, s.replace(a, tag + '\n\t' + a), 'utf8');
      log('已注入 script 标签: ' + rel);
      changed = true;
    }
  }

  // 同步 checksums：受保护文件被改过就必须更新哈希，否则启动时告警
  if (product && product.checksums) {
    let dirty = false;
    for (const key of Object.keys(product.checksums)) {
      const p = path.join(app, 'out', key);
      if (!fs.existsSync(p)) continue;
      const h = sha256b64(p);
      if (product.checksums[key] !== h) { product.checksums[key] = h; dirty = true; }
    }
    if (dirty) {
      try {
        backup(productPath, 'dom');
        writeJson(productPath, product);
        log('已同步 product.json.checksums');
        changed = true;
      } catch (e) { log('同步 checksums 失败:', e.message); }
    }
  }
  return { dom: true, changed };
}

// ───────────────────────── 状态 ─────────────────────────
function collectStatus(ctx) {
  const inst = findDevinInstall();
  const lp = findLangpack();
  const out = [];
  out.push('Devin 安装目录 : ' + (inst || '未找到'));
  out.push('官方中文语言包 : ' + (lp || '未找到（将使用 VSIX 自带 localizations）'));

  if (lp) {
    try {
      const c = readJson(path.join(lp, 'translations', 'main.i18n.json')).contents;
      let n = 0;
      for (const f of Object.keys(c)) n += Object.keys(c[f] || {}).length;
      out.push('语言包译文总量 : ' + n.toLocaleString());
    } catch { }
  }

  if (inst) {
    const app = path.join(inst, 'resources', 'app');

    // 扩展贡献点
    let extOk = 0, extTotal = 0;
    for (const name of EXT_FAMILY) {
      const dir = path.join(app, 'extensions', name);
      const pkgPath = path.join(dir, 'package.json');
      if (!fs.existsSync(pkgPath)) continue;
      extTotal++;
      const zh = readJson(path.join(dir, 'package.nls.zh-cn.json'));
      const pkg = readJson(pkgPath);
      const s = JSON.stringify(pkg || {});
      if (zh && s.includes('%"') === false && /%[\w.]{6,}%/.test(s)) extOk++;
    }
    if (extTotal) out.push('扩展贡献点汉化 : ' + extOk + ' / ' + extTotal);

    // webapp i18next
    const chunk = findHostChunk(app);
    let wa = false;
    try { wa = !!(chunk && fs.readFileSync(chunk, 'utf8').includes(HOST_MARK)); } catch { }
    out.push('Agent UI i18next : ' + (chunk ? (wa ? '✓ 已注入' : '✗ 未注入') : '未找到入口'));

    // DOM
    for (const [rel] of PAGES) {
      let ok = false;
      try { ok = fs.readFileSync(path.join(app, rel), 'utf8').includes('devin-zh-dom.js'); } catch { }
      out.push('DOM 注入 ' + (rel.includes('sessions') ? 'Sessions 窗口' : '主窗口') + ' : ' + (ok ? '✓' : '✗'));
    }

    // checksums
    try {
      const prod = readJson(path.join(app, 'product.json'));
      let ok = 0, bad = 0;
      for (const [k, exp] of Object.entries(prod.checksums || {})) {
        const p = path.join(app, 'out', k);
        if (!fs.existsSync(p)) { bad++; continue; }
        (sha256b64(p) === exp ? ok++ : bad++);
      }
      out.push('完整性校验自洽 : ' + ok + ' / ' + (ok + bad) + (bad === 0 ? '  ✓ 不会告警' : '  ✗ 有 ' + bad + ' 项不一致'));
    } catch { }
  }
  return out;
}

// ───────────────────────── 激活 ─────────────────────────
function activate(context) {
  const ctx = { extensionPath: context.extensionPath };
  log('扩展已激活, 路径 =', context.extensionPath);

  const run = (silent) => {
    let changed = false;
    const steps = [
      ['语言包', applyLanguagePack],
      ['扩展贡献点', applyExtensionManifests],
      ['webapp i18next', applyWebappI18n],
      ['DOM', applyDomLayer],
    ];
    for (const [name, fn] of steps) {
      try {
        const r = fn(ctx);
        if (r && r.changed) changed = true;
      } catch (e) {
        log(name + ' 层失败:', e.message);
      }
    }
    if (changed) {
      log('汉化已落地 —— 需重启一次 Devin 才能完全生效。');
      vscode.window.showInformationMessage(
        'Devin 简体中文已应用。语言包与界面注入需要重启 Devin 一次才能完全生效。', '知道了'
      ).then(() => { }, () => { });
    } else if (!silent) {
      log('汉化已是最新状态，无需改动。');
    }
    return changed;
  };

  run(true);

  context.subscriptions.push(
    vscode.commands.registerCommand('devin-zh.status', async () => {
      const lines = collectStatus(ctx);
      log('状态:\n' + lines.join('\n'));
      await vscode.window.showInformationMessage('Devin 中文状态：' + lines.join(' | '), { modal: true }, '确定');
    }),
    vscode.commands.registerCommand('devin-zh.apply', async () => {
      const changed = run(false);
      await vscode.window.showInformationMessage(
        changed ? '已重新应用汉化，请重启 Devin。' : '汉化已是最新，无需改动。');
    }),
    vscode.commands.registerCommand('devin-zh.uninstall', async () => {
      const dirs = fs.existsSync(BACKUP_ROOT)
        ? fs.readdirSync(BACKUP_ROOT).filter((d) => d.startsWith('vsix-')).sort() : [];
      if (!dirs.length) {
        vscode.window.showWarningMessage('没有找到本插件产生的备份，无法自动回滚。');
        return;
      }
      const pick = await vscode.window.showWarningMessage(
        '将回滚到本插件安装前的状态（最近的备份）。继续？', { modal: true }, '回滚', '取消');
      if (pick !== '回滚') return;

      const src = path.join(BACKUP_ROOT, dirs[dirs.length - 1]);
      const inst = findDevinInstall();
      const lp = findLangpack();
      const targets = [];
      if (lp) {
        targets.push([path.join(src, 'main.i18n.json'), path.join(lp, 'translations', 'main.i18n.json')]);
        targets.push([path.join(src, 'windsurf.i18n.json'), path.join(lp, 'translations', 'extensions', 'windsurf.i18n.json')]);
        targets.push([path.join(src, 'package.json'), path.join(lp, 'package.json')]);
      }
      if (inst) {
        const app = path.join(inst, 'resources', 'app');
        targets.push([path.join(src, 'workbench.html'), path.join(app, 'out/vs/code/electron-browser/workbench/workbench.html')]);
        targets.push([path.join(src, 'sessions.html'), path.join(app, 'out/vs/sessions/electron-browser/sessions.html')]);
        targets.push([path.join(src, 'product.json'), path.join(app, 'product.json')]);
        for (const name of EXT_FAMILY) {
          targets.push([path.join(src, 'package.json'), path.join(app, 'extensions', name, 'package.json')]);
        }
        const chunk = findHostChunk(app);
        if (chunk) targets.push([path.join(src, path.basename(chunk)), chunk]);
      }
      for (const [b, t] of targets) {
        try {
          if (fs.existsSync(b) && fs.existsSync(t)) { fs.copyFileSync(b, t); log('已还原 ' + t); }
        } catch (e) { log('还原失败 ' + t + ': ' + e.message); }
      }
      await vscode.window.showInformationMessage('已回滚，请重启 Devin。');
    })
  );
}

function deactivate() { }

module.exports = { activate, deactivate };

