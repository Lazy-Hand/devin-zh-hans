# -*- coding: utf-8 -*-
"""
inject_webapp.py — 从干净备份注入 webapp 中文资源（可直接执行，幂等）

为什么单独写成脚本:
  第 3 层要在 Devin 安装目录里改一个 2 MB 的 chunk，且必须满足三条硬约束：
    ① 载荷插在 `Mt.isInitialized||Eu()` **之前**（否则 init 已用旧 mu 完成）
    ② 逐命名空间 Object.assign（浅合并整个 mu 会删掉未翻译的英文 key）
    ③ 不能留下尾逗号（`,}` 会让 chunk 语法错误、Devin 起不来）
  这三条以前靠手写拼接，反复出错。这里固化成一个可重复执行、带语法自检的脚本。

用法:
    python tools/inject_webapp.py            # 注入（自动找干净源）
    python tools/inject_webapp.py --check    # 只检查当前状态
    python tools/inject_webapp.py --restore  # 恢复原始 chunk
"""
import json, os, re, shutil, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MARK = "/*devin-zh*/"
END = "/*/devin-zh*/"
ANCHOR = "Mt.isInitialized||Eu()"
CHUNK_NAME = "entry-host-editor-mode-menu-DUnUGWLA.js"


def devin_app():
    for c in (os.environ.get("DEVIN_INSTALL"),
              os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Devin"),
              r"C:\Program Files\Devin"):
        if c and os.path.exists(os.path.join(c, "Devin.exe")):
            return os.path.join(c, "resources", "app")
    return None


def find_clean(app):
    """找一个不含 devin-zh 标记、且带锚点的原始 chunk。"""
    cands = []
    # 插件自己的备份目录优先
    for root, _dirs, files in os.walk(os.path.join(os.environ.get("USERPROFILE", ""), ".devin", "devin-zh-backups")):
        for f in files:
            if f == CHUNK_NAME:
                cands.append(os.path.join(root, f))
    for p in cands:
        try:
            s = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if ANCHOR in s and MARK not in s:
            return p
    return None


def make_payload(zh):
    parts = []
    safe = re.compile(r"^[A-Za-z_$][\w$]*$")
    for ns, kv in zh.items():
        if safe.match(ns):
            init = "mu.%s||(mu.%s={})" % (ns, ns)
        else:
            q = json.dumps(ns, ensure_ascii=False)
            init = "mu[%s]||(mu[%s]={})" % (q, q)
        parts.append("Object.assign(%s,%s)" % (
            init, json.dumps(kv, ensure_ascii=False, separators=(",", ":"))))
    return MARK + ",".join(parts) + END


def syntax_ok(path):
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        err = [l for l in (r.stderr or "").splitlines() if "Error" in l]
        return False, err[-1] if err else "unknown"
    return True, ""


def main():
    app = devin_app()
    if not app:
        print("✗ 未找到 Devin 安装")
        return 1
    chunk = os.path.join(app, "out", "vs", "workbench", "devin-webapp-host",
                         "assets", CHUNK_NAME)
    if not os.path.exists(chunk):
        print("✗ chunk 不存在:", chunk)
        return 1

    cur = open(chunk, encoding="utf-8", errors="ignore").read()

    if "--check" in sys.argv:
        ok, err = syntax_ok(chunk)
        print("大小        :", len(cur))
        print("载荷标记    :", cur.count(MARK))
        print("锚点        :", cur.count(ANCHOR))
        print("载荷在锚点前:", cur.find(MARK) < cur.find(ANCHOR) if MARK in cur else "无载荷")
        print("逐命名空间  :", "Object.assign(mu." in cur)
        print("尾逗号      :", bool(re.search(r"Mt\.isInitialized\|\|Eu\(\)\s*,\s*\}", cur)))
        print("语法        :", "OK" if ok else "✗ " + err)
        return 0 if ok else 1

    if "--restore" in sys.argv:
        src = find_clean(app)
        if not src:
            print("✗ 找不到干净备份")
            return 1
        shutil.copyfile(src, chunk)
        print("✓ 已恢复:", os.path.basename(chunk))
        return 0

    # 注入：始终从干净源出发，避免叠加历史改动
    src = find_clean(app)
    if not src:
        print("✗ 找不到干净备份，无法安全注入")
        return 1
    base = open(src, encoding="utf-8", errors="ignore").read()

    at = base.find(ANCHOR)
    if at < 0:
        print("✗ 备份里没有锚点")
        return 1

    zh = json.load(open(os.path.join(ROOT, "assets", "webapp-i18n.json"), encoding="utf-8"))
    payload = make_payload(zh)

    # 插在锚点之前；锚点后面的字符原样保留（不额外加逗号）
    out = base[:at] + payload + "," + base[at:]

    tmp = os.path.join(tempfile.gettempdir(), CHUNK_NAME)
    open(tmp, "w", encoding="utf-8", newline="").write(out)
    ok, err = syntax_ok(tmp)
    if not ok:
        print("✗ 生成结果语法错误，已放弃写入:", err)
        return 1

    shutil.copyfile(tmp, chunk)
    ok2, err2 = syntax_ok(chunk)
    print("✓ 已注入 %d 个命名空间" % len(zh))
    print("  大小 %d -> %d" % (len(base), len(out)))
    print("  语法:", "OK" if ok2 else "✗ " + err2)
    return 0 if ok2 else 1


if __name__ == "__main__":
    sys.exit(main())
