# -*- coding: utf-8 -*-
"""
probe_keyecho.py — 找出「界面直接显示原始 i18n key」的原因

现象：侧边栏出现 `sidebar.automations`、`sidebar.recent` 这样的原始 key。

两种可能：
  A) i18next 里根本没有这个 key（我们的载荷漏了 / key 名不对）→ 回落成 key 本身
  B) 组件把 key 当文案直接渲染（bug 在 Devin 侧，或我们覆盖了一个本应是对象的节点）

本脚本：
  1) 把 i18n 入口 chunk 之外的**所有** chunk 也扫一遍，找 `sidebar.*` 这类点号 key 的引用
  2) 打印引用点上下文，看它是 t("sidebar.automations") 还是字符串拼接
  3) 顺带核对我们的载荷里有没有这些 key
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP, PLUGIN as _PLUGIN  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIR = os.path.join(_APP or "", "out", "vs", "workbench", "devin-webapp-host", "assets")
LOCALE = re.compile(r"^(ja|es|pt|zh|ko|fr|de|ru|it|xx)-")

WANT = ["sidebar.automations", "sidebar.recent", "sidebar.security", "sidebar.wiki",
        "sidebar.review", "sidebar.customize", "composerTips.sidebar"]

print("== 各 chunk 里对点号 key 的引用 ==")
for f in sorted(os.listdir(DIR)):
    if not f.endswith(".js") or LOCALE.match(f):
        continue
    s = open(os.path.join(DIR, f), encoding="utf-8", errors="ignore").read()
    for w in WANT:
        if w not in s:
            continue
        for m in list(re.finditer(re.escape(w), s))[:2]:
            a = max(0, m.start() - 240)
            b = min(len(s), m.end() + 160)
            print("\n-- %s  [%s]" % (f, w))
            print("   " + s[a:b].replace("\n", " "))

print("\n\n== 载荷里这些 key 是否存在 ==")
chunk = None
for f in sorted(os.listdir(DIR)):
    if f.startswith("entry-host-editor-mode-menu") and f.endswith(".js"):
        p = os.path.join(DIR, f)
        if "/*devin-zh*/" in open(p, encoding="utf-8", errors="ignore").read():
            chunk = p
            break
if chunk:
    s = open(chunk, encoding="utf-8", errors="ignore").read()
    i, j = s.find("/*devin-zh*/"), s.find("/*/devin-zh*/")
    m = re.search(r'"en","translation",(\{.*\}),!0,!0\)$', s[i:j], re.S)
    if m:
        payload = json.loads(m.group(1))
        for w in WANT:
            ns, _, rest = w.partition(".")
            v = payload.get(ns, {}).get(rest) if rest else None
            print("  %-26s %s" % (w, v or "(载荷缺失)"))
else:
    print("  未找到已注入的载荷")
