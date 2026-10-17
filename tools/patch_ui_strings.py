# -*- coding: utf-8 -*-
"""
patch_ui_strings.py — 直接替换 Devin Agent UI 资源表里的英文值

Devin 的两套 React Agent UI（sessions / chat-client）把界面文案放在内联的
i18next 资源表里，形如  "cloudSettings":"Cloud settings" ，代码用模板字符串
动态拼 key（所以搜不到 "nav.xxx" 字面量）。

englishOverrides 那条路（addResourceBundle 深合并）实测对这个侧边栏无效，
因此直接改资源表的值：把  :"English"  替换成  :"中文"。
只匹配「冒号+引号」的值位置，不动键名，也不动代码字面量。
"""
import hashlib, base64, json, os, re, shutil, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
APP = _APP
PRODUCT = os.path.join(APP, "product.json")
HERE = os.path.dirname(os.path.abspath(__file__))

TARGETS = [
    (os.path.join(APP, "node_modules", "@exa", "chat-client", "index.js"), None),
    (os.path.join(APP, "out", "vs", "sessions", "sessions.desktop.main.js"),
     "vs/sessions/sessions.desktop.main.js"),
    (os.path.join(APP, "out", "vs", "workbench", "windsurf-chat-client", "index.js"),
     "vs/workbench/windsurf-chat-client/index.js"),
]

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def rd(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f: return f.read()

def sha256_b64(p):
    return base64.b64encode(hashlib.sha256(open(p, "rb").read()).digest()).decode().rstrip("=")

def main():
    dry = "--dry-run" in sys.argv
    with open(os.path.join(_SHARED, "ui-strings-zh.json"), "r", encoding="utf-8") as f:
        pairs = json.load(f)
    print("词条数: %d" % len(pairs))

    bak = os.path.join(os.path.expanduser("~"), ".devin", "devin-zh-backups",
                       "ui-strings-" + time.strftime("%Y%m%d-%H%M%S"))
    if not dry: os.makedirs(bak, exist_ok=True)
    print("备份: %s" % bak)

    for path, ck in TARGETS:
        name = os.path.relpath(path, APP)
        if not os.path.exists(path):
            print("\n-- %s : 不存在" % name); continue
        s = rd(path)
        total = 0
        parts = []
        # 按长度降序，避免长短语被子串先吃掉
        for en, zh in sorted(pairs.items(), key=lambda kv: -len(kv[0])):
            pat = '"' + en + '"'
            rep = '"' + zh + '"'
            c = s.count(pat)
            if c:
                s = s.replace(pat, rep)
                total += c
                parts.append("%s x%d" % (en, c))
        print("\n-- %s" % name)
        print("   替换 %d 处: %s" % (total, ", ".join(parts[:10]) + (" ..." if len(parts) > 10 else "")))
        if dry or total == 0:
            continue
        shutil.copy2(path, os.path.join(bak, os.path.basename(path)))
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("   写入完成")
        if ck:
            prod = json.loads(rd(PRODUCT))
            prod["checksums"][ck] = sha256_b64(path)
            with open(PRODUCT, "w", encoding="utf-8") as f:
                json.dump(prod, f, ensure_ascii=False, indent='\t')
            print("   checksums 已同步")
        else:
            print("   不在 checksums 内，无需同步")
    return 0

if __name__ == "__main__":
    sys.exit(main())
