# -*- coding: utf-8 -*-
"""
verify_integrity.py — 证明补丁「零完整性告警」的核心声明
1) 用 product.json 的 checksums 逐个校验 11 个受保护文件的实际哈希
2) 校验 windsurf package.json 里每个 %key% 都能在 package.nls.json 中解析
3) 校验语言包 bundle 注册与 667 条译文可查
"""
import hashlib, base64, json, os, io, re

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
APP = _APP
LP = _LP
DICT = _SHARED

buf = io.StringIO()
def P(*a): print(*a, file=buf)
def rd(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

# ── 1. checksums ──
P("## 1. product.json 完整性校验（补丁后重新计算）\n")
prod = rd(os.path.join(APP, "product.json"))
cks = prod.get("checksums", {})
P("| 结果 | 受保护文件 |")
P("|---|---|")
allok = True
for rel, expect in cks.items():
    p = os.path.join(APP, "out", rel)
    if not os.path.exists(p):
        P(f"| 缺失 | `{rel}` |"); allok = False; continue
    h = hashlib.sha256(open(p, "rb").read()).digest()
    got = base64.b64encode(h).decode().rstrip("=")
    ok = (got == expect)
    if not ok: allok = False
    P(f"| {'✅ 一致' if ok else '❌ 不一致'} | `vs/{rel}` |" if not rel.startswith("vs/") else f"| {'✅ 一致' if ok else '❌ 不一致'} | `{rel}` |")
P(f"\n**结论：{'全部 11 个受保护文件哈希与原始值完全一致 → 不会触发“Devin 安装似乎损坏”告警' if allok else '存在被修改的受保护文件'}**\n")

# ── 2. %key% 可解析性 ──
P("## 2. windsurf 扩展 %key% 占位符可解析性\n")
WS = os.path.join(APP, "extensions", "windsurf")
pkg = rd(os.path.join(WS, "package.json"))
nls = rd(os.path.join(WS, "package.nls.json"))
found = re.findall(r"%([^%]+)%", json.dumps(pkg, ensure_ascii=False))
found = sorted(set(found))
unresolved = [k for k in found if k not in nls]
P(f"- package.json 中的 %key% 占位符 : **{len(found)}** 个")
P(f"- package.nls.json 提供英文默认值 : **{len(nls)}** 条")
P(f"- 无法解析（会原样显示 %key%）  : **{len(unresolved)}**" + (f" -> {unresolved[:6]}" if unresolved else " ✅"))
zh = rd(os.path.join(WS, "package.nls.json"))  # 英文默认
ws_i18n = rd(os.path.join(LP, "translations", "extensions", "windsurf.i18n.json"))
pkgzh = ws_i18n.get("contents", {}).get("package", {})
nozh = [k for k in found if k not in pkgzh]
P(f"- windsurf.i18n.json 提供中文译文  : **{len(pkgzh)}** 条")
P(f"- 缺中文（会回落英文）            : **{len(nozh)}**" + (f" -> {nozh[:6]}" if nozh else " ✅"))
P("\n### 抽样对照\n")
P("| key | 英文默认 | 中文 |")
P("|---|---|---|")
for k in found[:8]:
    P(f"| `{k}` | {str(nls.get(k,''))[:40]} | {str(pkgzh.get(k,'—'))[:40]} |")

# ── 3. 语言包注册与译文可查 ──
P("\n## 3. 语言包 bundle 注册与译文可查性\n")
lp = rd(os.path.join(LP, "package.json"))
loc = lp.get("contributes", {}).get("localizations", [])
ids = [t["id"] for b in loc for t in b.get("translations", [])]
P(f"- 语言包版本 : {lp.get('version')}  (engines.vscode = {lp.get('engines',{}).get('vscode')})")
P(f"- 已注册 bundle 数 : **{len(ids)}**")
P(f"- 含 `windsurf` : {'✅' if 'windsurf' in ids else '❌'}")
main = rd(os.path.join(LP, "translations", "main.i18n.json"))
c = main.get("contents", {})
supp = rd(os.path.join(DICT, "nls-supplement.json"))
tot = sum(len(v) for v in supp.values())
hit = sum(1 for f, kv in supp.items() for k in kv if c.get(f) and k in c[f])
P(f"- vscode bundle 译文总量 : **{sum(len(v) for v in c.values()):,}** 条")
P(f"- 补丁 667 条可查 : **{hit}/{tot}** {'✅' if hit == tot else '❌'}")

P("\n### 补丁译文抽样（Devin 专有模块）\n")
P("| 源文件 | key | 英文 | 中文 |")
P("|---|---|---|---|")
en_map = {}
todo = rd(os.path.join(_DATA, "todo.json"))["by_file"]
shown = 0
for f in sorted(supp):
    if not re.search(r"windsurf|devin|cascade|lifeguard", f, re.I):
        continue
    for k in list(supp[f])[:2]:
        en = next((x["en"] for x in todo.get(f, []) if x["key"] == k), "")
        P(f"| `{f.split('/')[-1]}` | `{k[:34]}` | {en[:44]} | **{supp[f][k][:44]}** |")
        shown += 1
    if shown >= 14: break

# ── 4. 安全边界 ──
P("\n## 4. 改动清单（只列实际被写入的路径）\n")
ml = os.path.join(os.path.expanduser("~"), ".devin", "devin-zh-backups")
dirs = sorted(os.listdir(ml)) if os.path.isdir(ml) else []
if dirs:
    mf = rd(os.path.join(ml, dirs[-1], "manifest.json"))
    P(f"备份批次：`{dirs[-1]}`\n")
    P("| 文件 | 原本存在 |")
    P("|---|---|")
    for x in mf["files"]:
        P(f"| `{x['path']}` | {'是（已备份）' if x['existed'] else '否（新增）'} |")
    P(f"\n受保护的 11 个文件是否出现在改动清单中：**{'❌ 出现了' if any('vs/' in x['path'] or 'out' in x['path'] for x in mf['files']) else '✅ 一个都没有'}**")

open(os.path.join(_DATA, "verify-report.md"), "w", encoding="utf-8").write(buf.getvalue())
print("OK allok=", allok, "unresolved=", len(unresolved), "nozh=", len(nozh), "hit=", hit, "/", tot)
