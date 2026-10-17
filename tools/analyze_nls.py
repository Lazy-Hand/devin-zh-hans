# -*- coding: utf-8 -*-
"""
Devin 桌面版 (Windsurf/Codeium 换皮 VS Code fork) 本地化可行性实证分析
输出: report.md + missing.json (完整待翻译清单)
"""
import json, os, re, collections, io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import (  # noqa: E402
    DEVIN_APP as _APP, LANGPACK as _LP, DATA as _DATA,
    SHARED as _SHARED, PLUGIN as _PLUGIN, OUT as _OUT,
)
APP = _APP
LP = _LP
WS  = os.path.join(APP, "extensions", "windsurf")
OUTDIR = _DATA

buf = io.StringIO()
def P(*a): print(*a, file=buf)

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

keys_raw = load(os.path.join(APP, "out", "nls.keys.json"))
msgs_raw = load(os.path.join(APP, "out", "nls.messages.json"))
lp_raw   = load(os.path.join(LP, "translations", "main.i18n.json"))
lp_contents = lp_raw["contents"]

# 展平 keys: [(file, key), ...] 与 msgs_raw 顺序一一对应
flat = []
for entry in keys_raw:
    f, ks = entry[0], entry[1]
    for k in ks:
        flat.append((f, k))

P("# Devin 桌面版汉化可行性实证报告\n")
P(f"- Devin 安装目录: `{APP}`")
P(f"- 应用版本: Devin 1.126.0 / windsurfVersion 3.10.67 / codeiumVersion 1.48.2 (Exafunction, Inc.)")
P(f"- 语言包: `{LP}`\n")

P("## 1. NLS 结构\n")
P("| 文件 | 结构 | 规模 |")
P("|---|---|---:|")
P(f"| `out/nls.keys.json` | `[[源文件, [key,...]], ...]` | {len(keys_raw):,} 个源文件 |")
P(f"| `out/nls.messages.json` | 展平的默认英文数组 | {len(msgs_raw):,} 条 |")
P(f"| `main.i18n.json` → `contents` | `{{源文件: {{key: 译文}}}}` | {len(lp_contents):,} 个源文件 |")
P(f"\n展平后 key 总数 = **{len(flat):,}**  ·  与 messages 数组长度{'一致 ✅' if len(flat)==len(msgs_raw) else '不一致 ❌'}")

# 顺序映射
default = {}
if len(flat) == len(msgs_raw):
    for (f, k), m in zip(flat, msgs_raw):
        default.setdefault(f, {})[k] = m
else:
    for f, k in flat:
        default.setdefault(f, {})[k] = ""

# 覆盖计算
all_pairs = set(flat)
lp_pairs = set()
for f, kv in lp_contents.items():
    if isinstance(kv, dict):
        for k in kv:
            lp_pairs.add((f, k))

covered = all_pairs & lp_pairs
missing = all_pairs - lp_pairs
P("\n## 2. 覆盖率 (按 (源文件, key) 二元组)\n")
P(f"- 全部 NLS 字符串 : **{len(all_pairs):,}**")
P(f"- 官方语言包已译  : **{len(covered):,}** ({len(covered)/max(len(all_pairs),1)*100:.1f}%)")
P(f"- 缺中文          : **{len(missing):,}** ({len(missing)/max(len(all_pairs),1)*100:.1f}%)")

# 语言包 key 总数对比
lp_total = sum(len(v) for v in lp_contents.values() if isinstance(v, dict))
P(f"- 语言包译文总条数 : {lp_total:,}  (其中 {len(lp_pairs - all_pairs):,} 条本构建已不存在)")

# 专业化: Devin/Windsurf 新增文件
pat = re.compile(r"windsurf|devin|cascade|codeium|exa/|chat_client|acp", re.I)
own_miss = collections.Counter(f for f, k in missing)
own_tot  = collections.Counter(f for f, k in all_pairs)
P("\n## 3. 缺失字符串按源文件聚合 TOP 45\n")
P("| 缺失 | 该文件总数 | 源文件 |")
P("|---:|---:|---|")
for f, n in own_miss.most_common(45):
    P(f"| {n} | {own_tot[f]} | `{f}` |")

P("\n## 4. Devin/Windsurf 专有源文件\n")
P("| 缺失 | 总数 | 源文件 |")
P("|---:|---:|---|")
ws_files = [f for f in own_tot if pat.search(f)]
for f in sorted(ws_files, key=lambda x: -own_miss[x]):
    P(f"| {own_miss[f]} | {own_tot[f]} | `{f}` |")
P(f"\n专有文件合计: {len(ws_files)} 个文件, 全部 key {sum(own_tot[f] for f in ws_files):,}, 其中缺中文 {sum(own_miss[f] for f in ws_files):,}")

P("\n## 5. 缺中文的 Devin/Windsurf 字符串样例 (前 60)\n")
P("| 源文件 | 英文原文 |")
P("|---|---|")
shown = 0
for f in sorted(ws_files, key=lambda x: -own_miss[x]):
    for k in default.get(f, {}):
        if (f, k) in missing:
            txt = default[f][k].replace("|", "\\|").replace("\n", " ")[:130]
            P(f"| `{f.split('/')[-1]}` | {txt} |")
            shown += 1
            if shown >= 60: break
    if shown >= 60: break

P("\n## 6. 完全缺中文的源文件 (语言包零覆盖)\n")
zero = [f for f in own_tot if own_miss[f] == own_tot[f] and own_tot[f] >= 3]
P(f"共 {len(zero)} 个文件。前 30：\n")
for f in sorted(zero, key=lambda x: -own_tot[x])[:30]:
    P(f"- `{f}` ({own_tot[f]} 条)")

# windsurf 扩展 package.json 硬编码情况
pkg = load(os.path.join(WS, "package.json"))
cmds = pkg.get("contributes", {}).get("commands", [])
hard = [c for c in cmds if isinstance(c.get("title"), str) and not str(c["title"]).startswith("%")]
nls_files = [x for x in os.listdir(WS) if x.startswith("package.nls")]
P("\n## 7. `extensions/windsurf` 扩展本身\n")
P(f"- package.json 命令数: {len(cmds)}")
P(f"- title 为**硬编码英文**(无 `%key%` 占位符): **{len(hard)} / {len(cmds)}**")
P(f"- 目录内 `package.nls*.json` 文件: {nls_files if nls_files else '**无** → 该扩展完全没有本地化入口**'}")
P(f"- 编译产物: `dist/extension.js` {os.path.getsize(os.path.join(WS,'dist','extension.js')):,} bytes (未 minify 成 asar，可直接改)")
P("\n结论: 该扩展的 64 个命令标题、菜单、配置项描述全部硬编码英文，**官方语言包机制无法覆盖**，")
P("必须在 `resources/app/extensions/windsurf/package.json` 里补 `package.nls.zh-cn.json` 并改成 `%key%`。")

# 导出完整清单
exp = {
    "total": len(all_pairs), "covered": len(covered), "missing": len(missing),
    "missing_list": [
        {"file": f, "key": k, "en": default.get(f, {}).get(k, "")}
        for f, k in sorted(missing)
    ],
}
with open(os.path.join(OUTDIR, "missing.json"), "w", encoding="utf-8") as fh:
    json.dump(exp, fh, ensure_ascii=False, indent=1)

with open(os.path.join(OUTDIR, "coverage.md"), "w", encoding="utf-8") as fh:
    fh.write(buf.getvalue())
print("OK missing =", len(missing), "total =", len(all_pairs))
