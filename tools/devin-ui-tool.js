#!/usr/bin/env node
/**
 * devin-ui-tool.js — Devin Agent UI (React) 中文注入 / 英文提取
 *
 * 背景：Devin 的 Agent 界面（vs/sessions，React SPA）字符串硬编码在编译后的 JSX 里，
 *       VS Code 的语言包机制覆盖不到，且其 bundle 被 product.json.checksums 保护，
 *       不能改文件。所以这一层走 Chromium DevTools Protocol，运行时替换文本节点。
 *
 * 用法：
 *   1) 让 Devin 带调试端口启动（单实例，需先退出正在运行的 Devin）：
 *        & "$env:LOCALAPPDATA\Programs\Devin\Devin.exe" --remote-debugging-port=9222
 *      或直接：  node devin-ui-tool.js --launch
 *   2) 注入中文：
 *        node devin-ui-tool.js --inject
 *   3) 抓取当前界面上尚未翻译的英文（用于扩充词典）：
 *        node devin-ui-tool.js --extract --out new-strings.json
 *
 * 运行方式（零依赖，用 Devin 自带 Electron 当 Node）：
 *   $env:ELECTRON_RUN_AS_NODE=1; & "...\Devin.exe" devin-ui-tool.js --inject
 */
'use strict';
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
const flag = (n) => argv.includes(n);
const opt = (n, d) => { const i = argv.indexOf(n); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };

const PORT = parseInt(opt('--port', '9222'), 10);
const HERE = __dirname;
const DICT_FILE = opt('--dict', path.join(HERE, 'dict', 'ui-dict.json'));
const OUT = opt('--out', path.join(HERE, 'new-strings.json'));
const WATCH = flag('--watch');
const LAUNCH = flag('--launch');

// ───────────── 给页面注入的运行时翻译器（必须自包含） ─────────────
function PAGE_TRANSLATOR(dict, opts) {
  if (window.__devinZh) { window.__devinZh.update(dict); return 'updated'; }
  var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, CODE: 1, PRE: 1, KBD: 1, SAMP: 1, SVG: 1, CANVAS: 1, INPUT: 1 };
  // 代码 / 终端 / 消息正文 / 输入框等绝不翻译
  var SKIP_SEL = (opts.skip || []).join(',');
  var hits = 0;
  var seen = new WeakSet();

  function skipParent(node) {
    for (var el = node.parentElement; el; el = el.parentElement) {
      if (SKIP_TAGS[el.tagName]) return true;
      if (el.isContentEditable) return true;
      if (el.getAttribute && el.getAttribute('translate') === 'no') return true;
      if (SKIP_SEL && el.matches && el.matches(SKIP_SEL)) return true;
    }
    return false;
  }

  function translateText(node) {
    if (!node || seen.has(node)) return;
    var t = node.nodeValue;
    if (!t) return;
    var key = t.trim();
    if (!key || key.length > 60) return;
    var zh = dict[key];
    if (!zh || zh === key) return;
    if (skipParent(node)) return;
    seen.add(node);
    node.nodeValue = t.replace(key, zh);
    hits++;
  }

  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { translateText(root); return; }
    if (root.nodeType !== 1) return;
    if (root.tagName && SKIP_TAGS[root.tagName]) return;
    if (root.id === 'devin-zh-indicator') return;
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.nodeValue && n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var n; while ((n = w.nextNode())) translateText(n);
  }

  var queue = [];
  var scheduled = false;
  function schedule(nodes) {
    for (var i = 0; i < nodes.length; i++) queue.push(nodes[i]);
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      var batch = queue.slice(0, 128); queue = queue.slice(128);
      batch.forEach(walk);
      if (queue.length) schedule([]);
    });
  }

  var mo = new MutationObserver(function (muts) {
    var add = [];
    for (var i = 0; i < muts.length; i++) {
      var m = muts[i];
      if (m.type === 'characterData') add.push(m.target);
      else for (var j = 0; j < m.addedNodes.length; j++) add.push(m.addedNodes[j]);
    }
    if (add.length) schedule(add);
  });
  mo.observe(document.documentElement, { childList: true, subtree: true, characterData: true });

  walk(document.body);

  function update(d) { for (var k in d) dict[k] = d[k]; walk(document.body); }

  var badge = document.createElement('div');
  badge.id = 'devin-zh-indicator';
  badge.textContent = '中';
  badge.title = 'Devin 中文化已启用 (CDP)';
  badge.style.cssText = 'position:fixed;right:6px;bottom:4px;z-index:2147483647;font:11px/1.4 system-ui;' +
    'color:#8ab4f8;background:rgba(0,0,0,.45);padding:1px 5px;border-radius:6px;pointer-events:none;opacity:.75';
  document.body.appendChild(badge);

  window.__devinZh = { update: update, hits: function () { return hits; }, dict: dict };
  return 'installed:' + hits;
}

// 抓取页面上"看起来是英文 UI 但词典里没有"的文本
function PAGE_EXTRACT(dict) {
  var out = [];
  var seenTxt = {};
  var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, TEXTAREA: 1, CODE: 1, PRE: 1, SVG: 1, CANVAS: 1 };
  var SKIP_SEL = '.monaco-editor,.xterm,[data-streamdown],.prose,[data-slate-editor],[data-testid*="message-content"],[data-testid*="terminal-output"]';
  function bad(el) {
    for (var e = el; e; e = e.parentElement) {
      if (SKIP_TAGS[e.tagName] || e.isContentEditable) return true;
      if (e.getAttribute && e.getAttribute('translate') === 'no') return true;
      if (e.matches && e.matches(SKIP_SEL)) return true;
    }
    return false;
  }
  var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  var n;
  while ((n = w.nextNode())) {
    var t = (n.nodeValue || '').trim();
    if (!t || t.length < 2 || t.length > 70) continue;
    if (!/[A-Za-z]/.test(t)) continue;
    if (!/^[A-Za-z]/.test(t)) continue;
    if (dict[t]) continue;
    if (seenTxt[t]) continue;
    if (n.parentElement && bad(n.parentElement)) continue;
    seenTxt[t] = 1;
    out.push({ en: t, tag: n.parentElement ? n.parentElement.tagName : '', cls: n.parentElement ? String(n.parentElement.className).slice(0, 60) : '' });
  }
  return out;
}

// ───────────── 极简 CDP 客户端 ─────────────
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function listTargets() {
  const r = await fetch(`http://127.0.0.1:${PORT}/json/list`);
  return r.json();
}

function connect(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    let id = 0;
    const pend = new Map();
    const ready = new Promise((res, rej) => {
      ws.addEventListener('open', () => res());
      ws.addEventListener('error', (e) => rej(new Error('WebSocket 连接失败: ' + (e.message || 'error'))));
    });
    ws.addEventListener('message', (ev) => {
      let msg; try { msg = JSON.parse(ev.data); } catch { return; }
      if (msg.id && pend.has(msg.id)) {
        const { res, rej } = pend.get(msg.id); pend.delete(msg.id);
        msg.error ? rej(new Error(JSON.stringify(msg.error))) : res(msg.result);
      }
    });
    resolve({
      ready,
      close: () => ws.close(),
      send: (method, params) => new Promise((res, rej) => {
        const i = ++id; pend.set(i, { res, rej });
        ws.send(JSON.stringify({ id: i, method, params: params || {} }));
      }),
    });
  });
}

async function launchDevin() {
  const cp = require('child_process');
  const exe = [
    path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Devin', 'Devin.exe'),
    'C:\\Program Files\\Devin\\Devin.exe',
  ].find((p) => fs.existsSync(p));
  if (!exe) throw new Error('找不到 Devin.exe');

  // 关键：本工具自身是靠 ELECTRON_RUN_AS_NODE=1 由 Devin.exe 跑起来的。
  // 若把这个变量透传给新进程，Devin 会以 Node 模式启动 —— 没有窗口、exit 0、
  // 看起来像“启动失败”。必须显式剔除。
  const env = Object.assign({}, process.env);
  delete env.ELECTRON_RUN_AS_NODE;

  console.log('· 启动 Devin --remote-debugging-port=' + PORT + '（已剔除 ELECTRON_RUN_AS_NODE）');
  cp.spawn(exe, ['--remote-debugging-port=' + String(PORT)], {
    detached: true, stdio: 'ignore', env,
  }).unref();
}

async function waitPort(timeoutMs) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    try { await listTargets(); return true; } catch { await sleep(700); }
  }
  return false;
}

async function applyToTargets(mode, dict) {
  const targets = (await listTargets()).filter((t) => t.type === 'page' && t.webSocketDebuggerUrl);
  let done = 0;
  for (const t of targets) {
    try {
      const c = await connect(t.webSocketDebuggerUrl);
      await c.ready;
      await c.send('Runtime.enable');
      const expr = mode === 'inject'
        ? `(${PAGE_TRANSLATOR.toString()})(${JSON.stringify(dict)},${JSON.stringify({ skip: [
            '.monaco-editor', '.monaco-diff-editor', '.xterm', '.cm-editor', '.ace_editor',
            '[data-streamdown]', '.prose', '[data-slate-editor]', '[data-transcript-row-key]',
            '[data-testid*="message-content"]', '[data-testid*="terminal-output"]',
            '[data-devin-input-box]', '[data-user-content]',
          ] })})`
        : `(${PAGE_EXTRACT.toString()})(${JSON.stringify(dict)})`;
      const r = await c.send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: false });
      const v = r.result && r.result.value;
      if (mode === 'inject') {
        console.log(`  ✓ ${t.title || t.url}  ->  ${v} (累计译 ${await (async () => {
          const r2 = await c.send('Runtime.evaluate', { expression: 'window.__devinZh?window.__devinZh.hits():0', returnByValue: true });
          return r2.result.value;
        })()})`);
      } else {
        console.log(`  · ${t.title || t.url}  ->  ${Array.isArray(v) ? v.length : 0} 条未译文本`);
      }
      const res = { target: t.title || t.url, value: v };
      c.close();
      done++;
      if (mode === 'extract') return res;
    } catch (e) {
      console.log('  ✗ ' + (t.title || t.url) + ' : ' + e.message);
    }
  }
  return { done };
}

(async () => {
  console.log('\nDevin Agent UI 中文化工具  (CDP, port ' + PORT + ')');
  if (LAUNCH) {
    await launchDevin();
    if (!(await waitPort(45000))) { console.error('✗ 等待调试端口超时。请确认 Devin 已完全退出后重试。'); process.exit(2); }
  } else if (!(await waitPort(2500))) {
    console.error('✗ 连不上 http://127.0.0.1:' + PORT + '/json/list');
    console.error('  Devin 必须带 --remote-debugging-port=' + PORT + ' 启动（单实例，需先完全退出）。');
    console.error('  可加 --launch 让本工具代你启动。');
    process.exit(2);
  }

  const dict = JSON.parse(fs.readFileSync(DICT_FILE, 'utf8'));
  console.log('· 词典: ' + Object.keys(dict).length.toLocaleString() + ' 条  (' + DICT_FILE + ')');

  const mode = flag('--extract') ? 'extract' : 'inject';
  const res = await applyToTargets(mode, dict);

  if (mode === 'extract') {
    const list = Array.isArray(res.value) ? res.value : [];
    fs.writeFileSync(OUT, JSON.stringify(list, null, 1), 'utf8');
    console.log('\n已导出 ' + list.length + ' 条候选到 ' + OUT);
    console.log('把它们译成中文后合并进 dict/ui-dict.json 即可扩充词典。');
  } else {
    console.log('\n注入完成。翻译在页面内持续生效（MutationObserver）。');
    if (WATCH) {
      console.log('进入监听模式，每 20s 对新出现的 target 重新注入…');
      setInterval(() => applyToTargets('inject', dict).catch(() => { }), 20000);
    }
  }
})();
