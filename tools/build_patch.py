# -*- coding: utf-8 -*-
"""
build_patch.py — 由词表生成插件产物

输入 (tools/data/):
  todo.json              NLS 缺口清单 [{file,key,en}]（由 analyze_nls.py 生成）
  zh/g1..g4.json         这些条目的 en -> 中文
  zh/g5.json             windsurf 扩展贡献点的 id -> 中文

输出 (仓库根):
  translations/main.i18n.json               官方译文 + 本插件补充的合并版语言包
  translations/extensions/windsurf.i18n.json
  assets/ui-dict.json                       DOM 翻译器词典
  assets/windsurf.en2key.json               值替换表
  assets/windsurf.package.nls.json          windsurf 扩展英文默认值
  assets/windsurf.pkgmap.json               字段路径 -> %key%（备查）

前提：本机已安装官方简体中文语言包（合并版的底子来自它）。
"""
import json, os, re, sys, collections, io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.path.join(_PLUGIN, "translations")
TRANS_EXT = os.path.join(TRANS, "extensions")
ASSETS = os.path.join(_PLUGIN, "assets")
DIST = _OUT
for _d in (TRANS, TRANS_EXT, ASSETS, _DATA, DIST):
    os.makedirs(_d, exist_ok=True)

log = []
def L(*a):
    s = " ".join(str(x) for x in a); log.append(s); print(s)

# ---------- 定位 Devin ----------
def find_devin():
    cands = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Devin"),
        r"C:\Program Files\Devin",
    ]
    for c in cands:
        if c and os.path.exists(os.path.join(c, "Devin.exe")):
            return c
    return None

DEVIN = find_devin()
HOME = os.path.expanduser("~")
EXTDIR = os.path.join(HOME, ".devin", "extensions")

def find_langpack():
    if not os.path.isdir(EXTDIR):
        return None
    for d in sorted(os.listdir(EXTDIR)):
        if "language-pack-zh-hans" in d:
            p = os.path.join(EXTDIR, d)
            if os.path.isfile(os.path.join(p, "translations", "main.i18n.json")):
                return p
    return None

LANGPACK = find_langpack()
L("Devin 安装目录      :", DEVIN)
L("用户扩展目录        :", EXTDIR)
L("中文语言包          :", LANGPACK)

# ---------- 读译文 ----------
def rd(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

todo = rd(os.path.join(_DATA, "todo.json"))["by_file"]           # {file:[{key,en}]}
en2zh = {}
for i in (1, 2, 3, 4):
    d = rd(os.path.join(_DATA, "zh", f"g{i}.json"))
    en2zh.update(d)
L("NLS 译文条数        :", len(en2zh))

g5 = rd(os.path.join(_DATA, "zh", "g5.json"))                    # id -> zh
L("windsurf 译文条数   :", len(g5))

# 从 windsurf 扩展 package.json 现场提取 id -> en（id 格式与 g5 一致）
WS_PKG = os.path.join(DEVIN or "", "resources", "app", "extensions", "windsurf", "package.json")
raw = {}
if os.path.isfile(WS_PKG):
    _pkg = rd(WS_PKG)
    _c = _pkg.get("contributes", {})
    for _cmd in _c.get("commands", []):
        if isinstance(_cmd.get("title"), str) and not _cmd["title"].startswith("%"):
            raw["commands/%s/title" % _cmd["command"]] = _cmd["title"]
        if isinstance(_cmd.get("category"), str):
            raw["commands/%s/category" % _cmd["command"]] = _cmd["category"]
    for _a in _c.get("authentication") or []:
        if isinstance(_a.get("label"), str):
            raw["authentication/%s/label" % _a["id"]] = _a["label"]
    _cfgs = _c.get("configuration")
    _cfgs = _cfgs if isinstance(_cfgs, list) else ([_cfgs] if isinstance(_cfgs, dict) else [])
    for _b in _cfgs:
        if isinstance(_b.get("title"), str):
            raw["configuration/title"] = _b["title"]
        for _pk, _pv in (_b.get("properties") or {}).items():
            _d = _pv.get("markdownDescription") or _pv.get("description")
            if isinstance(_d, str):
                raw["configuration/%s/description" % _pk] = _d
L("windsurf 字段数     :", len(raw), f"(来源 {WS_PKG})")

# ---------- 1. NLS 补充表 (file -> {key: zh}) ----------
supp = {}
miss_en = []
for f, items in todo.items():
    for it in items:
        z = en2zh.get(it["en"])
        if not z:
            miss_en.append(it["en"]); continue
        supp.setdefault(f, {})[it["key"]] = z
n_supp = sum(len(v) for v in supp.values())
L("\n[1] NLS 补充表:", n_supp, "条 /", len(supp), "个源文件")
if miss_en:
    L("    未命中译文(键不一致):", len(miss_en), miss_en[:5])

with open(os.path.join(_DATA, "nls-supplement.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(supp, f, ensure_ascii=False, indent=1)

# ---------- 2. 合并进 main.i18n.json ----------
if LANGPACK:
    mpath = os.path.join(LANGPACK, "translations", "main.i18n.json")
    with open(mpath, "r", encoding="utf-8") as f:
        main = json.load(f)
    contents = main.setdefault("contents", {})
    added = 0
    for f, kv in supp.items():
        tgt = contents.setdefault(f, {})
        for k, v in kv.items():
            if k not in tgt:
                tgt[k] = v; added += 1
    out = os.path.join(TRANS, "main.i18n.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(main, f, ensure_ascii=False)
    L(f"[2] main.i18n.json 合并: 新增 {added} 条, 总 {sum(len(v) for v in contents.values()):,} 条")
    L("    输出:", out, f"({os.path.getsize(out)/1048576:.2f} MB)")

    # ---------- 3. React UI 通用词典: 英文原文 -> 中文 ----------
    pairs = {}
    for f, kv in contents.items():
        if not isinstance(kv, dict):
            continue
        for k, v in kv.items():
            if not isinstance(v, str):
                continue
            pairs.setdefault(k, v)
    bad = re.compile(r"[\n\r<>{}]|\$\(|//|https?:|\.js\b|\.json\b|=>|\bnull\b|\bundefined\b")
    ui = {}
    for en, zh in pairs.items():
        s = en.strip()
        if s != en or not (2 <= len(s) <= 60):
            continue
        if bad.search(s):
            continue
        if s.isupper() and len(s) > 2:
            continue
        if "%" in s or "&" in s:
            continue
        if not re.search(r"[A-Za-z]", s):
            continue
        ui[s] = zh
    with open(os.path.join(ASSETS, "ui-dict.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(ui, f, ensure_ascii=False, indent=0, sort_keys=True)
    L(f"[3] React UI 通用词典: {len(ui):,} 条 ({os.path.getsize(os.path.join(ASSETS,'ui-dict.json'))/1048576:.2f} MB)")
else:
    L("[2] 未找到语言包，跳过合并")

# ---------- 4. windsurf 扩展本地化 ----------
def keyfor(i):
    p = i.split("/")
    if len(p) == 3 and p[0] == "commands":
        return f"devin.cmd.{p[1]}.{'title' if p[2]=='title' else 'category'}"
    if len(p) == 3 and p[0] == "authentication":
        return f"devin.auth.{p[1]}.label"
    if len(p) == 2 and p[0] == "configuration" and p[1] == "title":
        return "devin.config.title"
    if len(p) == 3 and p[0] == "configuration" and p[2] == "description":
        return f"devin.config.{p[1]}.description"
    return None

pkgmap = {}      # id -> %key%
nlsdef = {}      # key -> en
pkgzh = {}       # key -> zh

# g5 按“英文原文”去重过，先建立 en -> zh，再按 id 全量映射
en2zh_ws = {}
for i, z in g5.items():
    e = raw.get(i)
    if e:
        en2zh_ws.setdefault(e, z)
L("windsurf 去重后译文  :", len(en2zh_ws), "条 unique 英文")

skipped = []
for i, en in raw.items():
    k = keyfor(i)
    z = en2zh_ws.get(en)
    if not k:
        skipped.append(i); continue
    pkgmap[i] = f"%{k}%"
    nlsdef[k] = en
    if z:
        pkgzh[k] = z
    else:
        skipped.append(i)
L(f"\n[4] windsurf 扩展: 映射 {len(pkgmap)} 个字段, 生成 {len(pkgzh)} 条中文译文, 缺译文 {len(skipped)} 个")
if skipped:
    L("    缺译文:", skipped[:8])

# 值替换表：英文原文 -> %key%（扩展用它在 contributes 里做值替换，不依赖路径解析）
en2key = {}
for i, en in raw.items():
    k = keyfor(i)
    if k and en not in en2key:
        en2key[en] = f"%{k}%"


def _merge_existing(existing_path, current, label):
    """与已有产物合并。

    为什么需要：本脚本从「当前安装目录」的 windsurf/package.json 提取字段，
    但那个文件在插件装过之后已经被换成 %key% 了，提取结果会偏少（176 → 112）。
    直接覆盖就会把仓库里的完整产物写坏，所以已存在的条目一律保留。
    """
    if not os.path.exists(existing_path):
        return current
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            old = json.load(f)
    except Exception as e:
        L(f"    ⚠ 读取已有 {label} 失败(忽略): {e}")
        return current
    if not isinstance(old, dict):
        return current
    added = 0
    for k, v in old.items():
        if k not in current:
            current[k] = v
            added += 1
    if added:
        L(f"    + 与已有 {label} 合并，补回 {added} 条（安装目录已被本地化，提取不全）")
    return current


ASSETS_NLS = os.path.join(ASSETS, "windsurf.package.nls.json")
ASSETS_E2K = os.path.join(ASSETS, "windsurf.en2key.json")
TRANS_WS = os.path.join(TRANS_EXT, "windsurf.i18n.json")

if any("%" in str(v) for v in raw.values()) or len(raw) < 150:
    L("\n    ⚠ 注意：安装目录的 windsurf/package.json 已被本地化（含 %key%），")
    L("      本次提取的字段不完整，将与已有产物合并以保持完整。")

en2key = _merge_existing(ASSETS_E2K, en2key, "windsurf.en2key.json")
nlsdef = _merge_existing(ASSETS_NLS, nlsdef, "windsurf.package.nls.json")
try:
    if os.path.exists(TRANS_WS):
        with open(TRANS_WS, "r", encoding="utf-8") as f:
            old_ws = json.load(f).get("contents", {}).get("package", {})
        add = 0
        for k, v in old_ws.items():
            if k not in pkgzh:
                pkgzh[k] = v; add += 1
        if add:
            L(f"    + 与已有 windsurf.i18n.json 合并，补回 {add} 条")
except Exception as e:
    L(f"    ⚠ 合并 windsurf.i18n.json 失败(忽略): {e}")

with open(ASSETS_E2K, "w", encoding="utf-8", newline="\n") as f:
    json.dump(en2key, f, ensure_ascii=False, indent=1)
L(f"    值替换表: {len(en2key)} 条 -> windsurf.en2key.json")
# pkgmap 只是备查文件，属于中间产物，放 data/ 不进插件
with open(os.path.join(_DATA, "windsurf.pkgmap.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(pkgmap, f, ensure_ascii=False, indent=1)
if pkgmap:
    with open(os.path.join(_DATA, "windsurf.pkgmap.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(pkgmap, f, ensure_ascii=False, indent=1)
with open(ASSETS_NLS, "w", encoding="utf-8", newline="\n") as f:
    json.dump(nlsdef, f, ensure_ascii=False, indent=1)
with open(TRANS_WS, "w", encoding="utf-8", newline="\n") as f:
    json.dump({"": ["Devin 简体中文补丁 —— windsurf 扩展贡献点译文", "Do not edit this file."],
               "version": "1.0.0",
               "contents": {"package": pkgzh}}, f, ensure_ascii=False, indent=1)
L(f"    windsurf 产物: nls {len(nlsdef)} 条 / 译文 {len(pkgzh)} 条")

# ---------- 5. 汇总 ----------
meta = {
    "devinDir": DEVIN,
    "langpackDir": LANGPACK,
    "langpackVersion": None,
    "nlsPairs": n_supp,
    "nlsFiles": len(supp),
    "windsurfFields": len(pkgmap),
    "uiDict": None,
}
if LANGPACK:
    try:
        lp = rd(os.path.join(LANGPACK, "package.json"))
        meta["langpackVersion"] = lp.get("version")
    except Exception:
        pass
try:
    meta["uiDict"] = len(ui)
except NameError:
    pass
with open(os.path.join(_DATA, "meta.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)
L("\n" + json.dumps(meta, ensure_ascii=False, indent=1))

with open(os.path.join(_DATA, "build.log"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(log))
