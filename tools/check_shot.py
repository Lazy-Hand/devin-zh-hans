# -*- coding: utf-8 -*-
"""
check_shot.py — 拿截图里的每一处英文，逐条问「重启后能不能翻译」

截图是 webapp 模式下的主窗口（shell_mode=webapp），文案来自三个不同的源：
  · 原生菜单/侧边栏骨架 → webapp 的 i18next（第 3 层）
  · 会话列表与时间戳     → 运行时数据（第 4 层 DOM）
  · 提示行与模式选择器   → i18next 插值（第 3 层）

本脚本对每一条同时查两层：i18next 覆盖表（按 key）与 DOM 词典（按英文原文），
给出「重启后是否会变中文」的判定，并列出两边都没覆盖的漏网条目。
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP, PLUGIN as _PLUGIN, DATA as _DATA  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 截图里可见的英文（按区域）
SHOT = [
    ("顶部菜单", ["Agents", "File", "Edit", "View", "Go", "Help"]),
    ("侧边栏", ["My Team", "New session", "Automations", "Security", "Review", "Wiki",
             "Customize", "Sessions", "Recent"]),
    ("会话时间", ["yesterday", "3 days ago", "7 days ago"]),
    ("输入区", ["Tip: Move between sessions", "Normal", "Devin"]),
    ("切换器", ["Cloud", "Local"]),
]

# ── 第 3 层：i18next 覆盖表 ──
wa = json.load(open(os.path.join(_PLUGIN, "assets", "webapp-i18n.json"), encoding="utf-8"))


def leaves(o, pre=""):
    for k, v in o.items():
        key = pre + "." + k if pre else k
        if isinstance(v, dict):
            yield from leaves(v, key)
        else:
            yield key, v


wa_flat = dict(leaves(wa))
wa_by_en = {}
for k, v in wa_flat.items():
    wa_by_en.setdefault(v, []).append(k)

# ── 第 4 层：DOM 词典 ──
dom = {}
for p in ("ui-dict.json", "ui-strings-zh.json"):
    dom.update(json.load(open(os.path.join(_PLUGIN, "assets", p), encoding="utf-8")))

# ── DOM 正则规则（与 build_dom.py 保持一致）──
RULES = [
    (r"^(\d+)\s+days?\s+ago$", r"\1 天前"),
    (r"^(\d+)\s+hours?\s+ago$", r"\1 小时前"),
    (r"^(\d+)\s+minutes?\s+ago$", r"\1 分钟前"),
    (r"^(\d+)\s+seconds?\s+ago$", r"\1 秒前"),
    (r"^Just now$", "刚刚"),
    (r"^Tip:\s*(.+)$", r"提示：\1"),
]


def dom_hit(s):
    if s in dom:
        return dom[s]
    for pat, rep in RULES:
        if re.search(pat, s):
            return re.sub(pat, rep, s)
    return None


print("第 3 层 i18next 覆盖: %s 个 key" % format(len(wa_flat), ","))
print("第 4 层 DOM 词典   : %s 条\n" % format(len(dom), ","))

miss = []
for zone, items in SHOT:
    print("── %s" % zone)
    for s in items:
        d = dom_hit(s)
        w = wa_by_en.get(s)
        mark = "✓" if (d or w) else "✗"
        src = []
        if w:
            src.append("i18next:" + w[0])
        if d:
            src.append("dom:" + d)
        print("  %s %-30s %s" % (mark, s, " / ".join(src) if src else "（两层都没覆盖）"))
        if not (d or w):
            miss.append((zone, s))
    print()

print("漏网 %d 条：%s" % (len(miss), [s for _, s in miss]))
