# -*- coding: utf-8 -*-
"""
probe_i18n_instances.py — 查清 webapp 里到底有几个 i18next 实例

现象：载荷已注入 `lL()` 闭包里，但界面仍显示原始 key（`sidebar.automations`），
说明组件用的实例上没有这份 bundle。

要查的：
  1) 除 i18n 入口 chunk 外，还有哪些 chunk 创建了 i18next 实例（.init( / initReactI18next）
  2) 入口 chunk 里 `Mt` 被赋值的所有位置（可能有多个副本，或后面被覆盖）
  3) `t('sidebar.automations')` 的调用者用的是哪个实例
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIR = os.path.join(_APP or "", "out", "vs", "workbench", "devin-webapp-host", "assets")
LOCALE = re.compile(r"^(ja|es|pt|zh|ko|fr|de|ru|it|xx)-")

print("== 各 chunk 的 i18next 相关标记 ==")
rows = []
for f in sorted(os.listdir(DIR)):
    if not f.endswith(".js") or LOCALE.match(f):
        continue
    s = open(os.path.join(DIR, f), encoding="utf-8", errors="ignore").read()
    init = s.count(".init({") + s.count("initReactI18next") + s.count("createInstance()")
    ut = s.count("useTranslation")
    arb = s.count("addResourceBundle")
    if init or ut or arb:
        rows.append((init + ut + arb, f, init, ut, arb, len(s)))
rows.sort(reverse=True)
for n, f, i, u, a, ln in rows[:14]:
    print("  %-48s init/inst=%-3d useTranslation=%-3d addResourceBundle=%-3d" % (f, i, u, a))

print("\n== 入口 chunk 里 Mt 的赋值/创建 ==")
CH = os.path.join(DIR, "entry-host-editor-mode-menu-DUnUGWLA.js")
s = open(CH, encoding="utf-8", errors="ignore").read()
for m in re.finditer(r"\bMt\s*=", s):
    a = max(0, m.start() - 120)
    b = min(len(s), m.end() + 120)
    print("  @%d  %s" % (m.start(), s[a:b].replace("\n", " ")[:240]))

print("\n== 入口 chunk 里 .init( 的调用 ==")
for m in re.finditer(r"\.init\(\{", s):
    a = max(0, m.start() - 200)
    b = min(len(s), m.end() + 260)
    print("  @%d  %s" % (m.start(), s[a:b].replace("\n", " ")[:420]))
    print()
