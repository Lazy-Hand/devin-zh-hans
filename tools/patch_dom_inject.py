# -*- coding: utf-8 -*-
"""
patch_dom_inject.py — 窗口级 DOM 翻译注入（最终层，覆盖一切来源的英文文案）

为什么需要这一层：
  Devin 的 Agent 侧边栏文案「既不在 i18next 资源表里（useTranslation 调用 0 次），
  也不在 JS 字面量里」，实测改完资源表/字符串后侧边栏仍是英文 —— 说明它来自远端数据。
  唯一能覆盖所有来源的办法是在窗口里挂一个 DOM 翻译器。

做法：
  1) 往 workbench.html / sessions.html 各插一行 <script src="./devin-zh-dom.js">
     （CSP 是 script-src 'self'，同目录外链脚本完全合法；
       Trusted Types 只约束 innerHTML，而本翻译器只改 nodeValue，不触发）
  2) 生成 devin-zh-dom.js：TreeWalker + MutationObserver + 词典/正则
  3) 同步更新 product.json.checksums（这两个 html 在受保护清单里）
"""
import hashlib, base64, json, os, shutil, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
APP = _APP
PRODUCT = os.path.join(APP, "product.json")
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = _SHARED
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAGES = [
    (os.path.join(APP, "out", "vs", "code", "electron-browser", "workbench", "workbench.html"),
     "vs/code/electron-browser/workbench/workbench.html",
     '<script src="./workbench.js" type="module"></script>'),
    (os.path.join(APP, "out", "vs", "sessions", "electron-browser", "sessions.html"),
     "vs/sessions/electron-browser/sessions.html",
     '<script src="./sessions.js" type="module"></script>'),
]

def rd(p):
    with open(p, "r", encoding="utf-8", errors="replace") as f: return f.read()

def sha256_b64(p):
    return base64.b64encode(hashlib.sha256(open(p, "rb").read()).digest()).decode().rstrip("=")

RUNTIME = r"""
/* devin-zh-dom.js — Devin 界面简体中文（DOM 层）
   由 patch_dom_inject.py 生成。只修改文本节点的 nodeValue，不动 React 状态与事件。 */
(function () {
  if (window.__devinZhDom) { window.__devinZhDom.rescan(); return; }
  var DICT = __DICT__;
  var RULES = __RULES__;
  var SKIP_TAGS = { SCRIPT:1, STYLE:1, NOSCRIPT:1, TEXTAREA:1, INPUT:1, SELECT:1, CODE:1, PRE:1, KBD:1, SAMP:1, SVG:1, CANVAS:1, IFRAME:1 };
  var SKIP_SEL = '.monaco-editor,.monaco-diff-editor,.monaco-list-row .label-name,.xterm,.cm-editor,.ace_editor,' +
                 '[data-streamdown],.prose,[data-slate-editor],[translate="no"],' +
                 '[data-testid*="message-content"],[data-testid*="terminal-output"],[data-transcript-row-key]';
  var hits = 0, seen = new WeakSet();

  function skip(node) {
    for (var el = node.parentElement; el; el = el.parentElement) {
      if (SKIP_TAGS[el.tagName]) return true;
      if (el.isContentEditable) return true;
      if (el.getAttribute && el.getAttribute('translate') === 'no') return true;
      if (el.matches && el.matches(SKIP_SEL)) return true;
    }
    return false;
  }
  function tr(node) {
    if (!node || seen.has(node)) return;
    var t = node.nodeValue; if (!t) return;
    var key = t.trim(); if (!key || key.length > 80) return;
    var out = DICT[key];
    if (out === undefined) {
      for (var i = 0; i < RULES.length; i++) { var m = RULES[i][0].exec(key); if (m) { out = key.replace(RULES[i][0], RULES[i][1]); break; } }
    }
    if (out === undefined || out === key) return;
    if (skip(node)) return;
    seen.add(node);
    node.nodeValue = t.replace(key, out);
    hits++;
  }
  function walk(root) {
    if (!root) return;
    if (root.nodeType === 3) { tr(root); return; }
    if (root.nodeType !== 1) return;
    if (SKIP_TAGS[root.tagName]) return;
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return n.nodeValue && n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT; }
    });
    var n; while ((n = w.nextNode())) tr(n);
  }
  var q = [], sched = false;
  function schedule(nodes) {
    for (var i = 0; i < nodes.length; i++) q.push(nodes[i]);
    if (sched) return; sched = true;
    requestAnimationFrame(function () {
      sched = false;
      var batch = q.slice(0, 160); q = q.slice(160);
      for (var i = 0; i < batch.length; i++) walk(batch[i]);
      if (q.length) schedule([]);
    });
  }
  new MutationObserver(function (ms) {
    var add = [];
    for (var i = 0; i < ms.length; i++) {
      var m = ms[i];
      if (m.type === 'characterData') add.push(m.target);
      else for (var j = 0; j < m.addedNodes.length; j++) add.push(m.addedNodes[j]);
    }
    if (add.length) schedule(add);
  }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });

  function rescan() { seen = new WeakSet(); walk(document.body); }
  window.__devinZhDom = { rescan: rescan, hits: function () { return hits; }, dict: DICT };
  if (document.body) walk(document.body);
  else document.addEventListener('DOMContentLoaded', function () { walk(document.body); });
  console.log('[devin-zh] DOM 翻译器已加载, 词典 ' + Object.keys(DICT).length + ' 条 / 规则 ' + RULES.length + ' 条');
})();
"""

def build_runtime():
    with open(os.path.join(_PLUGIN, "assets", "ui-dict.json"), "r", encoding="utf-8") as f:
        base = json.load(f)
    with open(os.path.join(DICT, "agent-ui-zh.json"), "r", encoding="utf-8") as f:
        nav = json.load(f).get("nav", {})
    with open(os.path.join(DICT, "ui-strings-zh.json"), "r", encoding="utf-8") as f:
        extra = json.load(f)
    # 英文短语 -> 中文：先通用词典，再用 Devin 专用词覆盖
    d = dict(base)
    for en, zh in nav.items():
        pass  # nav 的 key 是 camelCase，不参与文本匹配
    d.update(extra)
    rules = [
        ["^(\\d+) MCP servers$", "$1 个 MCP 服务器"],
        ["^(\\d+) MCP server$", "$1 个 MCP 服务器"],
        ["^Tip: (.+)$", "提示：$1"],
        ["^You've used (\\d+)% of your quota\\. Quota resets (.+)\\.$", "你已使用 $1% 的配额，配额将于 $2 重置。"],
    ]
    out = RUNTIME.replace("__DICT__", json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    out = out.replace("__RULES__", json.dumps(rules, ensure_ascii=False, separators=(",", ":")))
    return out, len(d), len(rules)

def main():
    dry = "--dry-run" in sys.argv
    js, nd, nr = build_runtime()
    print("运行时脚本: 词典 %d 条, 正则 %d 条, 大小 %.2f MB" % (nd, nr, len(js) / 1048576))
    if dry:
        print("[dry-run] 将写入以下位置:")
        for p, ck, _ in PAGES:
            print("   %s" % p)
            print("   %s" % os.path.join(os.path.dirname(p), "devin-zh-dom.js"))
        return 0

    bak = os.path.join(os.path.expanduser("~"), ".devin", "devin-zh-backups",
                       "dom-inject-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(bak, exist_ok=True)
    print("备份: %s" % bak)

    prod = json.loads(rd(PRODUCT))
    for path, ck, anchor in PAGES:
        d = os.path.dirname(path)
        jsp = os.path.join(d, "devin-zh-dom.js")
        print("\n-- %s" % os.path.relpath(path, APP))
        if not os.path.exists(path):
            print("   ✗ 不存在"); continue
        shutil.copy2(path, os.path.join(bak, os.path.basename(path)))
        with open(jsp, "w", encoding="utf-8", newline="\n") as f:
            f.write(js)
        print("   ✓ 写入 %s (%.2f MB)" % (os.path.basename(jsp), len(js) / 1048576))

        s = rd(path)
        tag = '<script src="./devin-zh-dom.js"></script>'
        if tag in s:
            print("   · 已注入过，跳过 HTML 修改")
        else:
            if anchor not in s:
                print("   ✗ 找不到锚点，跳过"); continue
            s = s.replace(anchor, tag + "\n\t" + anchor, 1)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(s)
            print("   ✓ 已插入 <script> 标签")

        prod["checksums"][ck] = sha256_b64(path)
        print("   ✓ checksums 已同步")

    with open(PRODUCT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(prod, f, ensure_ascii=False, indent='\t')
    print("\n完成。重启 Devin 生效。")
    return 0

if __name__ == "__main__":
    sys.exit(main())
