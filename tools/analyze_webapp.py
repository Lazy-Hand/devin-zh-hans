# -*- coding: utf-8 -*-
"""
analyze_webapp.py — 分析新版 Agent UI（devin-webapp-host）的 i18n 资源与词典缺口

背景（Devin 3.11.216 起）：
  Agent 侧边栏不再是 `windsurf-chat-client/index.js`，而是新的 webapp-host：

      out/vs/workbench/devin-webapp-host/
          index.js            ← 稳定入口，被 workbench.desktop.main.js `import("@devin/webapp-host")`
          assets/*.js         ← 1800+ 个 rolldown chunk（约 91 MB）
          splash.html         ← 启动占位
          index.css

  它在渲染进程里自建 i18next 实例（`entry-host-editor-mode-menu-*.js` 里的 `Eu()`）：

      resources: { en: { translation: yl, review: lu } }, lng: "en", fallbackLng: "en"
      gu = [{code:"en"},{code:"ja",…},{code:"pt",…},{code:"es",…}]

  即：**有真实的多语言机制**（ja / pt / es 各有一份 chunk），但没有中文。

  本脚本据此产出三样东西：
    1) en 资源里的 (key, 英文)，并用 ja/es/pt chunk 的 key 集合交叉验证，
       只有出现在语言包里的 key 才算真 i18n key（把组件局部变量名过滤掉）；
    2) 与现有词典比对，算出缺口；
    3) 缺口按「短句优先」排序写成待译清单，供人工/agent 翻译。

输出：
    tools/data/webapp.json             完整结构化结果
    tools/data/webapp.md               覆盖率报告
    tools/data/webapp-todo.json        待译清单 {"en": ""}（值为空，等填）
"""
import json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DEVIN_APP as _APP, DATA as _DATA, DICT as _DICT, ASSETS as _ASSETS  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST = os.path.join(_APP or "", "out", "vs", "workbench", "devin-webapp-host")
ASSET_DIR = os.path.join(HOST, "assets")

LOCALE_CHUNK = re.compile(r"^(ja|es|pt|zh|ko|fr|de|ru|it|xx)-")
PAIR = re.compile(r"""([A-Za-z_$][\w$]{0,60})\s*:\s*(?:`([^`\\$]{1,400})`|"([^"\\$]{1,400})"|'([^'\\$]{1,400})')""")

# 值不像 UI 文案
BAD_VALUE = re.compile(
    r"\{\{"                                   # 插值模板，DOM 层匹配不到整串
    r"|=>|\)\s*&&|\)\s*\|\||^\s*[,)\]}]"
    r"|^#?[0-9a-fA-F]{3,8}$|^\d+(\.\d+)?(px|rem|em|ms|s|%)?$"
    r"|^[\W_]+$|\\\\|\\u[0-9a-f]{4}"
    r"|\.(js|mjs|ts|tsx|css|json|sh|yml|yaml)\b"
    r"|https?://|^\./|^/|^-{1,2}[a-z]"
    r"|^[a-z][A-Za-z0-9]*(\.[A-Za-z0-9_]+)+$"  # a.b.c 形式的 i18n key 引用
    r"|^[a-z][a-z0-9]*([A-Z][a-z0-9]+)+$"      # camelCase 标识符
    r"|^[A-Z][A-Z0-9_]+$"                      # CONSTANT
    r"|[A-Za-z0-9_]\.[A-Za-z0-9_]+\(\)"        # foo.bar() 调用串
)


def read(fn):
    try:
        return open(os.path.join(ASSET_DIR, fn), "r", encoding="utf-8", errors="ignore").read()
    except OSError:
        return ""


def pairs_of(text):
    out = {}
    for m in PAIR.finditer(text):
        v = (m.group(2) or m.group(3) or m.group(4) or "").strip()
        if v:
            out.setdefault(m.group(1), v)
    return out


def load_dict():
    d = {}
    for p in (os.path.join(_ASSETS, "ui-dict.json"), os.path.join(_ASSETS, "ui-strings-zh.json")):
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                d.update(json.load(f))
    p = os.path.join(_DICT, "webapp-zh.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            d.update(json.load(f))
    return d


def usable(en):
    if not en or len(en) < 2 or len(en) > 200:
        return False
    if not re.search(r"[A-Za-z]", en):
        return False
    if BAD_VALUE.search(en):
        return False
    if " " not in en and en[0].islower():
        return False
    if len(en.split()) > 30:
        return False
    return True


def main():
    if not os.path.isdir(ASSET_DIR):
        print("✗ 未找到 webapp-host 资产目录:", ASSET_DIR)
        return 1

    files = [f for f in sorted(os.listdir(ASSET_DIR)) if f.endswith(".js")]
    locale_files = [f for f in files if LOCALE_CHUNK.match(f)]
    en_files = [f for f in files if not LOCALE_CHUNK.match(f)]

    loc_keys, loc_count = set(), {}
    for f in locale_files:
        ks = pairs_of(read(f))
        loc_count[f] = len(ks)
        loc_keys |= set(ks)

    en = {}
    for f in en_files:
        for k, v in pairs_of(read(f)).items():
            en.setdefault(k, (v, f))

    keys = [(k, en[k][0], en[k][1]) for k in en if k in loc_keys]
    keys.sort()

    dict_ = load_dict()
    uniq_en = {v for _, v, _ in keys}
    uniq_hit = {e for e in uniq_en if e in dict_}
    missing = sorted(e for e in uniq_en if e not in dict_)

    todo = [e for e in missing if usable(e)]

    out = {
        "host": HOST,
        "chunks": len(en_files),
        "localeChunks": loc_count,
        "localeKeys": len(loc_keys),
        "keys": [{"key": k, "en": v, "chunk": c} for k, v, c in keys],
        "stats": {
            "i18nKeys": len(keys),
            "uniqueEnglish": len(uniq_en),
            "covered": len(uniq_hit),
            "missing": len(missing),
            "todo": len(todo),
        },
    }
    os.makedirs(_DATA, exist_ok=True)
    with open(os.path.join(_DATA, "webapp.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(os.path.join(_DATA, "webapp-todo.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({e: "" for e in todo}, f, ensure_ascii=False, indent=0)

    by_chunk = collections.Counter(c for _, _, c in keys)
    A = ["# webapp-host（新版 Agent UI）i18n 资源与词典覆盖\n",
         "- 目录: `%s`" % HOST,
         "- chunk 数: **%d**（另有语言包 chunk %d 个）" % (len(en_files), len(locale_files))]
    for f, n in sorted(loc_count.items()):
        A.append("  - `%s` → %d 个 key" % (f, n))
    A += ["- 语言包 key 并集: **%d**" % len(loc_keys),
          "- en 资源里能对上语言包 key 的: **%d**" % len(keys),
          "- 去重后英文原文: **%d**" % len(uniq_en),
          "- 词典已覆盖: **%d** (%.1f%%)" % (len(uniq_hit), len(uniq_hit) / max(len(uniq_en), 1) * 100),
          "- 仍缺中文: **%d**（其中可直接做整串替换的 %d）" % (len(missing), len(todo)),
          "\n## 英文资源最集中的 chunk\n", "| 条数 | chunk |", "|---:|---|"]
    for c, n in by_chunk.most_common(15):
        A.append("| %d | `%s` |" % (n, c))
    A += ["\n## 缺口样例（前 80）\n", "| key | 英文 |", "|---|---|"]
    seen, shown = set(), 0
    for k, v, c in keys:
        if v in dict_ or v in seen or not usable(v):
            continue
        seen.add(v)
        A.append("| `%s` | %s |" % (k, v.replace("|", "\\|")[:110]))
        shown += 1
        if shown >= 80:
            break
    with open(os.path.join(_DATA, "webapp.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(A) + "\n")

    print("OK i18nKeys=%d uniqueEn=%d covered=%d missing=%d todo=%d"
          % (len(keys), len(uniq_en), len(uniq_hit), len(missing), len(todo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
