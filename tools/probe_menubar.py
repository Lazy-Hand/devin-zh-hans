# -*- coding: utf-8 -*-
"""
probe_menubar.py — 定位「菜单栏 File/Edit/View/Go/Help」的文案来源

截图里菜单栏一直是英文，而语言包里 desktopShellMenubar 的 55 条译文都在。
两个可能：
  A) 菜单由 webapp 渲染，读的是它自己的 i18next（我们只覆盖了 en 的 translation 命名空间）
  B) 菜单由原生 Electron 绘制，走 product.json 的 menuBar，与语言包无关

本脚本在两个 bundle 里搜菜单标签，判断到底是哪条路径。
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

APP = _APP
LABELS = ["File", "Edit", "View", "Go", "Help", "Window", "Selection", "Terminal"]

targets = [
    ("webapp chunk", os.path.join(APP, "out/vs/workbench/devin-webapp-host/assets/entry-host-editor-mode-menu-DUnUGWLA.js")),
    ("workbench", os.path.join(APP, "out/vs/workbench/workbench.desktop.main.js")),
    ("main", os.path.join(APP, "out/main.js")),
]

print("== 各 bundle 里的菜单标签字面量 ==")
for name, p in targets:
    if not os.path.exists(p):
        print("  %-14s 不存在" % name)
        continue
    s = open(p, encoding="utf-8", errors="ignore").read()
    print("\n-- %s (%s bytes)" % (name, format(len(s), ",")))
    for lab in LABELS:
        # 反引号 / 单双引号三种字面量
        n = len(re.findall(r"[`'\"](%s)[`'\"]" % lab, s))
        if n:
            print("   %-9s %d 处" % (lab, n))
    for kw in ["menuBar", "setMenu", "Menu.buildFromTemplate", "applicationMenu"]:
        c = s.count(kw)
        if c:
            print("   %-24s %d 处" % (kw, c))

print("\n== webapp 里是否有菜单模板 ==")
wdir = os.path.join(APP, "out/vs/workbench/devin-webapp-host/assets")
if os.path.isdir(wdir):
    hits = []
    for f in os.listdir(wdir):
        if not f.endswith(".js"):
            continue
        s = open(os.path.join(wdir, f), encoding="utf-8", errors="ignore").read()
        score = s.count("desktopShell.menu") * 10 + s.count("menuBar") + s.count("MenuBar")
        if score >= 5:
            hits.append((score, f, s.count("desktopShell.menu"), s.count("menuBar")))
    hits.sort(reverse=True)
    for score, f, m1, m2 in hits[:8]:
        print("   %-52s score=%-4d desktopShell.menu=%d menuBar=%d" % (f, score, m1, m2))

print("\n== 语言包里 desktopShellMenubar 的译文 ==")
lp = os.path.join(os.path.expanduser("~"), ".devin", "extensions")
pack = None
if os.path.isdir(lp):
    for d in os.listdir(lp):
        if "language-pack-zh-hans" in d:
            p = os.path.join(lp, d, "translations", "main.i18n.json")
            if os.path.exists(p):
                pack = p
if pack:
    c = json.load(open(pack, encoding="utf-8"))["contents"]
    f = "vs/workbench/contrib/windsurfDesktopShell/browser/desktopShellMenubar"
    kv = c.get(f, {})
    print("   条数:", len(kv))
    for k, v in list(kv.items())[:8]:
        print("   %-18s %s" % (k, v))
