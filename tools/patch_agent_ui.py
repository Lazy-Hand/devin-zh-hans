# -*- coding: utf-8 -*-
"""
patch_agent_ui.py — 给 Devin 的 Agent UI 注入简体中文

Devin 有两套 i18next 实例，结构完全一致：

  A) vs/sessions/sessions.desktop.main.js            (44 MB) — Sessions 窗口
  B) vs/workbench/windsurf-chat-client/index.js      (25 MB) — Agent 侧边栏/对话面板

两者都是：
      let n = { en: { translation: jr, review: ji } };
      Ua.use(UW).init({ resources: n, lng: "en", fallbackLng: "en", ... });
      t && Ua.addResourceBundle("en","translation", t, !0, !0);
    }({ englishOverrides: JSON.parse('{"transcript":{...}}') })

即：只注册英文资源、lng 硬编码 "en"，但给了一个**深合并覆盖 en 资源**的入口。
把这个 overrides JSON 换成含中文的版本，界面就会显示中文，无需碰 lng。

该文件在 product.json.checksums 内，所以必须同步更新期望哈希（product.json 自身不在
checksums 内，因此自洽）。
"""
import hashlib, base64, json, os, re, shutil, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
APP = _APP
PRODUCT = os.path.join(APP, "product.json")
DICT = _SHARED
ANCHOR = "englishOverrides:JSON.parse('"

TARGETS = [
    # ★ 真正渲染 Agent 侧边栏/对话面板的就是这一份（npm 包，未打包，且不在 checksums 内）
    ("Agent chat-client (实际加载)", os.path.join(APP, "node_modules", "@exa", "chat-client", "index.js"),
     None),
    ("Sessions 窗口", os.path.join(APP, "out", "vs", "sessions", "sessions.desktop.main.js"),
     "vs/sessions/sessions.desktop.main.js"),
    ("Agent 侧边栏 (workbench 副本)", os.path.join(APP, "out", "vs", "workbench", "windsurf-chat-client", "index.js"),
     "vs/workbench/windsurf-chat-client/index.js"),
]

# 非 i18n 的硬编码显示文案（精确字符串替换，只挑纯显示用 prop）
HARDCODED = [
    ('label:"Spaces"', 'label:"空间"'),
    ('displayTitle:"Spaces"', 'displayTitle:"空间"'),
    ('searchPlaceholder:"Search sessions"', 'searchPlaceholder:"搜索会话"'),
]

def rd(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f: return f.read()

def sha256_b64(p):
    return base64.b64encode(hashlib.sha256(open(p, "rb").read()).digest()).decode().rstrip("=")

def load_zh():
    f = os.path.join(DICT, "agent-ui-zh.json")
    with open(f, "r", encoding="utf-8") as fh: return json.load(fh)

def deep_merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict): deep_merge(dst[k], v)
        else: dst[k] = v
    return dst

def patch_one(label, path, ck_key, zh, dry, bak):
    print("\n── %s ──" % label)
    print("   %s" % path)
    if not os.path.exists(path):
        print("   ✗ 文件不存在"); return False
    s = rd(path)
    n = s.count(ANCHOR)
    print("   大小 %d bytes, 锚点 %d 处" % (len(s), n))
    if n != 1:
        print("   ✗ 锚点不唯一或缺失，跳过"); return False

    a = s.index(ANCHOR) + len(ANCHOR)
    j, esc = a, False
    while j < len(s):
        c = s[j]
        if esc: esc = False
        elif c == "\\": esc = True
        elif c == "'": break
        j += 1
    raw = s[a:j]
    orig = json.loads(raw)
    merged = deep_merge(json.loads(json.dumps(orig)), zh)
    newjson = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    if "'" in newjson:
        print("   ✗ 译文含单引号，中止"); return False
    nk = sum(len(v) if isinstance(v, dict) else 1 for v in zh.values())
    print("   overrides: %d -> %d bytes (注入 %d 个中文 key)" % (len(raw), len(newjson), nk))

    if dry:
        print("   [dry-run] %s" % newjson[:160]); return True

    shutil.copy2(path, os.path.join(bak, os.path.basename(path)))
    s2 = s[:a] + newjson + s[j:]
    for old, new in HARDCODED:
        c = s2.count(old)
        if c:
            s2 = s2.replace(old, new)
            print("   硬编码 %-38s x%d -> %s" % (old, c, new))
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s2)
    print("   写入完成 %d -> %d bytes" % (len(s), len(s2)))

    prod = json.loads(rd(PRODUCT))
    if ck_key is None or ck_key not in prod.get("checksums", {}):
        print("   不在 product.json.checksums 内 —— 无需同步哈希 ✅")
        return True
    old_h = prod["checksums"].get(ck_key)
    prod["checksums"][ck_key] = sha256_b64(path)
    with open(PRODUCT, "w", encoding="utf-8") as f:
        json.dump(prod, f, ensure_ascii=False, indent='\t')
    print("   checksums[%s]: %s -> %s" % (ck_key.split('/')[-1],
          (old_h or "")[:12] + "...", prod["checksums"][ck_key][:12] + "..."))
    return True

def main():
    dry = "--dry-run" in sys.argv
    zh = load_zh()
    print("中文词典命名空间: %s" % list(zh.keys()))
    bak = os.path.join(os.path.expanduser("~"), ".devin", "devin-zh-backups",
                       "agent-ui-" + time.strftime("%Y%m%d-%H%M%S"))
    if not dry: os.makedirs(bak, exist_ok=True)
    print("备份目录: %s" % bak)
    okc = 0
    for label, path, key in TARGETS:
        if patch_one(label, path, key, zh, dry, bak): okc += 1
    print("\n完成: %d/%d 个 bundle" % (okc, len(TARGETS)))
    return 0 if okc == len(TARGETS) else 1

if __name__ == "__main__":
    sys.exit(main())
