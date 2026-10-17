/**
 * Devin 简体中文 —— 扩展运行时
 *
 * 这个扩展做两件事：
 *   1) 语言包层：通过 contributes.localizations 提供 zh-cn 的 vscode / windsurf bundle。
 *      但 VS Code 在同一 locale 下按扩展顺序合并 translations，官方语言包
 *      （ms-ceintl.*）排序在后时会覆盖我们，所以还需要第 2 步做硬保证。
 *   2) 落地层：把合并版语言包写进已安装的官方中文语言包、注册 windsurf bundle，
 *      并向 Devin 的两个窗口 HTML 注入 DOM 翻译器（Agent 侧边栏文案不在 i18n 资源表里，
 *      只能靠 DOM 层覆盖），最后同步 product.json.checksums 以免出现完整性告警。
 *
 * 全程幂等：重复激活不会重复注入，也不会破坏已生效的安装。
 */
'use strict';
const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const TAG = '[devin-zh]';
const log = (...a) => console.log(TAG, ...a);
const BACKUP_ROOT = path.join(os.homedir(), '.devin', 'devin-zh-backups');

// ───────────────────────── 环境探测 ─────────────────────────
function findDevinInstall() {
  const cands = [
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Devin'),
    'C:\\Program Files\\Devin',
  ];
  for (const c of cands) {
    if (c && fs.existsSync(path.join(c, 'Devin.exe'))) return c;
  }
  return null;
}

function findLangpack() {
  const root = path.join(os.homedir(), '.devin', 'extensions');
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

function backup(p, tag) {
  try {
    if (!fs.existsSync(p)) return;
    const d = path.join(BACKUP_ROOT, 'vsix-' + tag);
    fs.mkdirSync(d, { recursive: true });
    const dst = path.join(d, path.basename(p));
    if (!fs.existsSync(dst)) fs.copyFileSync(p, dst);
  } catch (e) { log('备份失败(忽略):', e.message); }
}

// ───────────────────────── 第 1 层：语言包落地 ─────────────────────────
function applyLanguagePack(ctx) {
  const lp = findLangpack();
  if (!lp) {
    log('未检测到官方中文语言包 —— VSIX 自带的 localizations 会直接生效。');
    return { langpack: false };
  }
  const src = path.join(ctx.extensionPath, 'translations', 'main.i18n.json');
  const dst = path.join(lp, 'translations', 'main.i18n.json');
  let changed = false;

  // 1) main.i18n.json -> 合并版（官方 21,336 + 本插件 667）
  if (!sameFile(src, dst)) {
    backup(dst, 'langpack');
    fs.copyFileSync(src, dst);
    log('已写入合并版 main.i18n.json（22,003 条译文）');
    changed = true;
  }

  // 2) windsurf bundle 译文
  const wsSrc = path.join(ctx.extensionPath, 'translations', 'extensions', 'windsurf.i18n.json');
  const wsDst = path.join(lp, 'translations', 'extensions', 'windsurf.i18n.json');
  if (!sameFile(wsSrc, wsDst)) {
    backup(wsDst, 'langpack');
    fs.mkdirSync(path.dirname(wsDst), { recursive: true });
    fs.copyFileSync(wsSrc, wsDst);
    log('已写入 windsurf.i18n.json（176 条）');
    changed = true;
  }

  // 3) 在语言包清单里注册 windsurf bundle
  let registered = false;
  const pkgPath = path.join(lp, 'package.json');
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
    const locs = pkg.contributes && pkg.contributes.localizations;
    if (Array.isArray(locs) && locs[0]) {
      locs[0].translations = locs[0].translations || [];
      if (!locs[0].translations.some((t) => t.id === 'windsurf')) {
        backup(pkgPath, 'langpack');
        locs[0].translations.push({ id: 'windsurf', path: './translations/extensions/windsurf.i18n.json' });
        fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, '\t'), 'utf8');
        log('已在语言包清单注册 windsurf bundle');
        changed = true;
        registered = true;
      }
    }
  } catch (e) { log('注册 bundle 失败:', e.message); }

  // 4) 把新注册的 bundle 直接补进 VS Code 的语言包缓存清单。
  //    · 不要删这个文件 —— VS Code 要到下一次启动才重建它，用户就得多重启一次；
  //    · 也不要伪造里面的 hash —— VS Code 用 clp/<hash>.<locale> 当缓存目录名，
  //      伪造值会让它去 scandir 一个不存在的目录并抛 ENOENT。
  //    hash 只由「语言包扩展 id + 版本」决定、不含 bundle 列表，
  //    所以直接补 entry 不会让它失配，本次重启就能用上。
  if (registered) {
    const lpJson = path.join(process.env.APPDATA || '', 'devin', 'languagepacks.json');
    try {
      if (fs.existsSync(lpJson)) {
        const j = JSON.parse(fs.readFileSync(lpJson, 'utf8'));
        const zh = j['zh-cn'];
        if (zh) {
          zh.translations = zh.translations || {};
          const p = path.join(lp, 'translations', 'extensions', 'windsurf.i18n.json');
          if (zh.translations['windsurf'] !== p) {
            backup(lpJson, 'langpack');
            zh.translations['windsurf'] = p;
            fs.writeFileSync(lpJson, JSON.stringify(j), 'utf8');
            log('已把 windsurf bundle 补进 languagepacks.json');
          }
        }
      }
      // 文件不存在时什么都不做：VS Code 启动时会自行生成完整清单
    } catch (e) { log('补 languagepacks.json 失败(可忽略):', e.message); }
  }
  return { langpack: true, changed };
}

// ───────────────────────── 第 2 层：DOM 翻译器落地 ─────────────────────────
const PAGES = [
  ['out/vs/code/electron-browser/workbench/workbench.html', './workbench.js'],
  ['out/vs/sessions/electron-browser/sessions.html', './sessions.js'],
];

function applyDomLayer(ctx) {
  const inst = findDevinInstall();
  if (!inst) { log('未找到 Devin 安装目录，跳过 DOM 层'); return { dom: false }; }
  const app = path.join(inst, 'resources', 'app');
  const runtimeSrc = path.join(ctx.extensionPath, 'dist', 'devin-zh-dom.js');
  const productPath = path.join(app, 'product.json');
  let product = null;
  try { product = JSON.parse(fs.readFileSync(productPath, 'utf8')); } catch { }

  let changed = false;
  for (const [rel, anchor] of PAGES) {
    const html = path.join(app, rel);
    if (!fs.existsSync(html)) continue;
    const jsName = 'devin-zh-dom.js';
    const jsDst = path.join(path.dirname(html), jsName);

    // 2a) 运行时脚本
    if (!sameFile(runtimeSrc, jsDst)) {
      try {
        fs.writeFileSync(jsDst, fs.readFileSync(runtimeSrc));
        log('已写入 ' + rel.replace(/\/[^/]+$/, '/') + jsName);
        changed = true;
      } catch (e) { log('写入运行时失败:', e.message); continue; }
    }

    // 2b) script 标签
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

    // 2c) 同步 checksums（这两个 html 在受保护清单里）
    if (product && product.checksums) {
      const key = rel.replace('out/', '');
      if (key in product.checksums) {
        const h = sha256b64(html);
        if (product.checksums[key] !== h) { product.checksums[key] = h; changed = true; }
      }
    }
  }
  if (product && changed) {
    try {
      backup(productPath, 'dom');
      fs.writeFileSync(productPath, JSON.stringify(product, null, '\t'), 'utf8');
      log('已同步 product.json.checksums');
    } catch (e) { log('同步 checksums 失败:', e.message); }
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
      const c = JSON.parse(fs.readFileSync(path.join(lp, 'translations', 'main.i18n.json'), 'utf8')).contents;
      let n = 0; for (const f of Object.keys(c)) n += Object.keys(c[f] || {}).length;
      out.push('语言包译文总量 : ' + n.toLocaleString() + (n > 22000 ? '  （已注入本插件增量 ✓）' : '  （尚未注入）'));
    } catch { }
  }
  if (inst) {
    const app = path.join(inst, 'resources', 'app');
    for (const [rel] of PAGES) {
      const html = path.join(app, rel);
      let ok = false;
      try { ok = fs.readFileSync(html, 'utf8').includes('devin-zh-dom.js'); } catch { }
      out.push('DOM 注入 ' + (rel.includes('sessions') ? 'Sessions 窗口' : '主窗口') + ' : ' + (ok ? '✓' : '✗'));
    }
    try {
      const prod = JSON.parse(fs.readFileSync(path.join(app, 'product.json'), 'utf8'));
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
    let lpRes = { }, domRes = { };
    try { lpRes = applyLanguagePack(ctx); } catch (e) { log('语言包层失败:', e.message); }
    try { domRes = applyDomLayer(ctx); } catch (e) { log('DOM 层失败:', e.message); }
    const changed = lpRes.changed || domRes.changed;
    if (changed) {
      log('汉化已落地（语言包 + 窗口注入）—— 需重启一次 Devin 才能完全生效。');
      vscode.window.showInformationMessage(
        'Devin 简体中文已应用。语言包与界面注入需要重启 Devin 一次才能完全生效。', '知道了'
      ).then(() => { }, () => { });
    } else if (!silent) {
      log('汉化已是最新状态，无需改动。');
    }
    return changed;
  };

  // 启动后静默应用（幂等；无改动时不打扰用户）
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
        targets.push([path.join(src, 'package.json'), path.join(lp, 'package.json')]);
      }
      if (inst) {
        const app = path.join(inst, 'resources', 'app');
        targets.push([path.join(src, 'workbench.html'), path.join(app, 'out/vs/code/electron-browser/workbench/workbench.html')]);
        targets.push([path.join(src, 'sessions.html'), path.join(app, 'out/vs/sessions/electron-browser/sessions.html')]);
        targets.push([path.join(src, 'product.json'), path.join(app, 'product.json')]);
      }
      for (const [b, t] of targets) {
        try { if (fs.existsSync(b)) { fs.copyFileSync(b, t); log('已还原 ' + t); } } catch (e) { log('还原失败 ' + t + ': ' + e.message); }
      }
      await vscode.window.showInformationMessage('已回滚，请重启 Devin。');
    })
  );
}

function deactivate() { }

module.exports = { activate, deactivate };
