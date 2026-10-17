# shared

跨插件共享的资源。

## dict/

| 文件 | 说明 |
|---|---|
| `ui-strings-zh.json` | **人工维护**的 Devin 专用词表（界面短语 → 中文）。DOM 翻译器与字符串替换都用它，新增文案只需改这里。 |
| `agent-ui-zh.json` | Agent UI 的 i18n 命名空间词表（当前只用到 `nav.*`）。 |

运行时实际加载的合并词典由 `tools/build_patch.py` 生成到 `plugins/*/assets/`，
生成时会以官方中文语言包的译文为底、用本目录的词表覆盖，
因此这里只需要放**官方没有的** Devin 专有文案。

## 加词条的流程

1. 编辑 `dict/ui-strings-zh.json`（键是界面上显示的英文原文）
2. `python tools/build_patch.py` 重新生成词典
3. `python tools/build_vsix.py --plugin zh-hans` 重新打包