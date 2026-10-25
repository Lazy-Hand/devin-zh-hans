# -*- coding: utf-8 -*-
"""
inspect_injected.py — 用花括号配平精确切出注入载荷，诊断「Extra data」原因

「Extra data」说明载荷 JSON 在 393127 字符处就结束了，后面还有内容 ——
很可能文件里存在**多段**注入（早期 dry-run/apply 的残留），或旧式载荷没摘干净。
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

APP = os.path.join(os.environ["LOCALAPPDATA"], "Programs", "Devin", "resources", "app")
P = os.path.join(APP, "out/vs/workbench/devin-webapp-host/assets/entry-host-editor-mode-menu-DUnUGWLA.js")

s = open(P, encoding="utf-8", errors="ignore").read()
print("文件长度:", len(s))
print("Object.assign(mu 出现:", s.count("Object.assign(mu||{},"))
print("/*devin-zh*/ 出现:", s.count("/*devin-zh*/"))
print("Mt.isInitialized||Eu() 出现:", s.count("Mt.isInitialized||Eu()"))
print("Mt.addResourceBundle(\"en\" 出现:", s.count('Mt.addResourceBundle("en"'))


def brace_end(text, start):
    """start 指向 '{'，返回配平后的 '}' 下标。"""
    depth = 0
    i = start
    q = None
    while i < len(text):
        ch = text[i]
        if q:
            if ch == "\\":
                i += 2
                continue
            if ch == q:
                q = None
            i += 1
            continue
        if ch in '`"':
            q = ch
            i += 1
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


pos = 0
seg = 0
while True:
    k = s.find("Object.assign(mu||{},", pos)
    if k < 0:
        break
    seg += 1
    ob = s.find("{", k + len("Object.assign(mu||{},") - 1)
    en = brace_end(s, ob)
    print("\n--- 第 %d 段 @%d  花括号 %d..%d  len=%d" % (seg, k, ob, en, en - ob + 1))
    try:
        obj = json.loads(s[ob:en + 1])
        print("    JSON OK, ns=%d" % len(obj))
    except Exception as e:
        print("    JSON FAIL:", e)
    print("    之后 40 字符:", repr(s[en + 1:en + 41]))
    pos = en + 1

# 锚点位置
for m in range(s.count("Mt.isInitialized||Eu()")):
    i = s.find("Mt.isInitialized||Eu()", 0 if m == 0 else 1)
print("\n锚点唯一下标:", s.find("Mt.isInitialized||Eu()"))
print("哨兵 /*/devin-zh*/ 位置:", s.find("/*/devin-zh*/"))
