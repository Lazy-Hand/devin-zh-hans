# -*- coding: utf-8 -*-
"""
probe_tips.py — 提取 webapp 里的 hint 族（输入框上方的提示行）

截图里的 "Tip: Move between sessions (Alt ↑ / Alt ↓)" 是 i18next 文案，
key 形如 sessionNav，值是带 `<shortcut/>` / `<up/>` 占位符的模板。
这类模板里的可见文字必须由 i18next 覆盖（DOM 层拿到的是渲染后的整串，匹配不到 key）。
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHUNK = os.path.join(_APP or "", "out/vs/workbench/devin-webapp-host/assets/entry-host-editor-mode-menu-DUnUGWLA.js")
s = open(CHUNK, encoding="utf-8", errors="ignore").read()

# 找出所有 "Tip: ..." 模板
print("== 所有 Tip: 模板 ==")
for m in re.finditer(r"([A-Za-z_$][\w$]*)\s*:\s*`(Tip:[^`]{1,200})`", s):
    print("  %-18s %s" % (m.group(1), m.group(2)))

print("\n== 上下文（hint 族）==")
i = s.find("Tip: Search sessions")
if i > 0:
    print(s[max(0, i - 500):i + 600].replace("\n", " "))
