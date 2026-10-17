# -*- coding: utf-8 -*-
"""
build_vsix.py — 把 plugins/<name>/ 打包成可安装的 .vsix

用法:
    python tools/build_vsix.py                 # 打包 plugins/zh-hans
    python tools/build_vsix.py --plugin zh-hans
    python tools/build_vsix.py --all           # 打包 plugins/ 下所有插件
    python tools/build_vsix.py --out dist      # 指定产物目录（默认 dist/）

VSIX 就是一个 zip：
    [Content_Types].xml
    extension.vsixmanifest
    extension/**        (扩展本体 = plugins/<name>/ 的内容)
关键 manifest 属性：
    Microsoft.VisualStudio.Code.Engine             = 引擎版本范围
    Microsoft.VisualStudio.Code.LocalizedLanguages = zh-cn   ← 语言包标识
"""
import argparse, json, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PLUGINS = os.path.join(ROOT, "plugins")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MANIFEST = '''<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="{name}" Version="{version}" Publisher="{publisher}" />
    <DisplayName>{displayName}</DisplayName>
    <Description xml:space="preserve">{description}</Description>
    <Tags>{tags}</Tags>
    <Categories>{categories}</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{engine}" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionSettings" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value="{languages}" />
    </Properties>
    <License>extension/LICENSE.txt</License>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code"/>
  </Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.License" Path="extension/LICENSE.txt" Addressable="true" />
  </Assets>
</PackageManifest>
'''

CONTENT_TYPES = '''<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension=".json" ContentType="application/json"/>
  <Default Extension=".js" ContentType="application/javascript"/>
  <Default Extension=".md" ContentType="text/markdown"/>
  <Default Extension=".txt" ContentType="text/plain"/>
  <Default Extension=".vsixmanifest" ContentType="text/xml"/>
  <Default Extension=".xml" ContentType="text/xml"/>
  <Default Extension=".png" ContentType="image/png"/>
</Types>
'''

# 打包时排除的开发期文件
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".vscode"}
EXCLUDE_FILES = {"CHANGELOG.md"}


def localized_languages(pkg):
    langs = []
    for loc in (pkg.get("contributes", {}) or {}).get("localizations", []) or []:
        if loc.get("languageId"):
            langs.append(loc["languageId"])
    return ",".join(langs)


def pack(plugin_dir, out_dir):
    pkg_path = os.path.join(plugin_dir, "package.json")
    if not os.path.exists(pkg_path):
        print("✗ 没有 package.json: %s" % plugin_dir)
        return None
    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)
    for req in ("name", "version", "publisher", "displayName", "description", "engines"):
        if req not in pkg:
            print("✗ package.json 缺少字段 %s (%s)" % (req, plugin_dir))
            return None

    manifest = MANIFEST.format(
        name=pkg["name"], version=pkg["version"], publisher=pkg["publisher"],
        displayName=pkg["displayName"], description=pkg["description"],
        engine=pkg["engines"]["vscode"],
        tags=",".join(pkg.get("keywords", [])),
        categories=",".join(pkg.get("categories", ["Other"])),
        languages=localized_languages(pkg),
    )
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "%s-%s.vsix" % (pkg["name"], pkg["version"]))
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("extension.vsixmanifest", manifest)
        for root, dirs, files in os.walk(plugin_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fn in files:
                if fn in EXCLUDE_FILES:
                    continue
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, plugin_dir).replace("\\", "/")
                z.write(p, "extension/" + rel)
                n += 1
    print("✓ %-14s -> %s" % (pkg["name"], out))
    print("    %d 个文件, %.2f MB, ID = %s.%s @ %s"
          % (n, os.path.getsize(out) / 1048576, pkg["publisher"], pkg["name"], pkg["version"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin", default=None, help="插件目录名（plugins/ 下）")
    ap.add_argument("--all", action="store_true", help="打包全部插件")
    ap.add_argument("--out", default=os.path.join(ROOT, "dist"), help="产物目录")
    args = ap.parse_args()

    if args.all:
        names = sorted(d for d in os.listdir(PLUGINS)
                       if os.path.isdir(os.path.join(PLUGINS, d))
                       and os.path.exists(os.path.join(PLUGINS, d, "package.json")))
    else:
        names = [args.plugin or "zh-hans"]

    made = []
    for name in names:
        r = pack(os.path.join(PLUGINS, name), args.out)
        if r:
            made.append(r)
    print("\n共生成 %d 个 VSIX" % len(made))
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
