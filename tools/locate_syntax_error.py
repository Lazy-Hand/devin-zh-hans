# -*- coding: utf-8 -*-
"""
locate_syntax_error.py — 定位注入后 chunk 的语法错误位置

node --check 只给「Unexpected token ','」，没有行号（文件基本是单行）。
这里用二分法：把注入段切成前缀，逐段做 node --check，找出第一个非法边界。

思路：注入段是
    Object.assign(mu.a||(mu.a={}),{…}),Object.assign(mu.b||(mu.b={}),{…}),…
若整体是逗号表达式，前缀到任意一个 `)` 结束都应当合法（表达式未完成时 node 报
「Unexpected end of input」而非「Unexpected token」）。真正非法的位置会立刻报
别的错，从而定位到具体命名空间。
"""
import os, re, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP = os.path.join(os.environ["LOCALAPPDATA"], "Programs", "Devin", "resources", "app")
CH = os.path.join(APP, "out/vs/workbench/devin-webapp-host/assets/entry-host-editor-mode-menu-DUnUGWLA.js")
MARK, END = "/*devin-zh*/", "/*/devin-zh*/"


def check(code):
    fd, p = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    try:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(code)
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode == 0:
            return True, ""
        for line in (r.stderr or "").splitlines():
            if line.startswith("SyntaxError"):
                return False, line.strip()
        return False, "unknown"
    finally:
        os.unlink(p)


s = open(CH, encoding="utf-8", errors="ignore").read()
a, b = s.find(MARK), s.find(END)
if a < 0 or b < 0:
    print("没有注入段")
    sys.exit(1)
seg = s[a:b + len(END)]
print("注入段长度:", len(seg))

# 逐个顶层逗号切分注入段（括号深度 0）
parts, depth, start, q = [], 0, len(MARK), None
i = len(MARK)
while i < len(seg) - len(END):
    ch = seg[i]
    if q:
        if ch == "\\":
            i += 2
            continue
        if ch == q:
            q = None
        i += 1
        continue
    if ch in "\"'":
        q = ch
    elif ch in "([{":
        depth += 1
    elif ch in ")]}":
        depth -= 1
    elif ch == "," and depth == 0:
        parts.append(seg[start:i])
        start = i + 1
    i += 1
parts.append(seg[start:i])
print("表达式个数:", len(parts))

# 每个表达式单独检查
bad = []
for idx, p in enumerate(parts):
    ok, err = check(p.strip() + ";")
    if not ok:
        bad.append((idx, p[:90], err))
print("单独检查非法表达式:", len(bad))
for idx, head, err in bad[:8]:
    print("  #%d %s\n     %s" % (idx, head, err))

# 整体前 N 个表达式拼接检查
if bad:
    first = bad[0][0]
    if first > 0:
        ok, err = check(",".join(parts[:first]) + ";")
        print("\n前 %d 个表达式拼接: %s %s" % (first, "OK" if ok else "FAIL", err))
