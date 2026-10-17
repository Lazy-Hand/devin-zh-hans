# -*- coding: utf-8 -*-
"""
release.py — 发布到 GitHub Releases

本仓库只维护一个插件，所以不需要任何"按插件区分"的机制：
`releases/latest` 指向的就是它。

让下载链接永久稳定的关键只有一条：**asset 文件名不带版本号**。
GitHub 的 `releases/latest/download/<asset>` 会解析到"最新正式 release 的那个 asset"，
所以下面这条 URL 永远有效，README 里放的就是它：

    https://github.com/<owner>/<repo>/releases/latest/download/devin-zh-hans.vsix

同时也会传一份带版本号的副本，方便归档与"我要 v1.0.2 那个"的场景。

用法：
    python tools/release.py                 # 发布当前 package.json 的 version
    python tools/release.py --dry-run       # 只显示将要做什么
    python tools/release.py --latest-only   # 只刷新 latest release 的 asset（版本号不变时用）
    python tools/release.py --status        # 查看当前发布状态与链接
"""
import argparse, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build")

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, HERE)

REPO = os.environ.get("DEVIN_PLUGIN_REPO", "klarkxy/devin-zh-hans")
ASSET_STABLE = "devin-zh-hans.vsix"        # 固定名 —— 稳定 URL 靠它


def sh(args, check=True):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise RuntimeError("命令失败: %s\n%s" % (" ".join(args), (r.stderr or r.stdout or "").strip()))
    return r


def gh(*a, check=True):
    return sh(["gh"] + list(a), check=check)


def pkg():
    with open(os.path.join(ROOT, "package.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def release_exists(tag):
    return gh("release", "view", tag, "--repo", REPO, "--json", "tagName", check=False).returncode == 0


def changelog_section(version):
    p = os.path.join(ROOT, "CHANGELOG.md")
    if not os.path.exists(p):
        return ""
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"^##\s+%s\s*$(.*?)(?=^##\s|\Z)" % re.escape(version), txt, re.M | re.S)
    return m.group(0).strip() if m else ""


def build():
    """构建并准备两个 asset：稳定名 + 带版本名。"""
    sh([sys.executable, os.path.join(HERE, "build_vsix.py")])
    p = pkg()
    versioned = os.path.join(BUILD, "%s-%s.vsix" % (p["name"], p["version"]))
    if not os.path.exists(versioned):
        raise RuntimeError("构建未产出 %s" % versioned)
    stable = os.path.join(BUILD, ASSET_STABLE)
    shutil.copyfile(versioned, stable)
    return versioned, stable


def do_status():
    p = pkg()
    tag = "v" + p["version"]
    print("\n仓库      : %s" % REPO)
    print("插件      : %s (%s)" % (p["displayName"], p["name"]))
    print("当前版本  : %s" % p["version"])
    print("对应 tag  : %s  %s" % (tag, "✓ 已发布" if release_exists(tag) else "✗ 未发布"))
    print("\n用户下载入口:")
    print("  直接下载最新版 : https://github.com/%s/releases/latest/download/%s" % (REPO, ASSET_STABLE))
    print("  查看所有版本   : https://github.com/%s/releases" % REPO)
    print("  指定版本下载   : https://github.com/%s/releases/download/%s/%s-%s.vsix"
          % (REPO, tag, p["name"], p["version"]))
    r = gh("release", "list", "--repo", REPO, "--limit", "5", check=False)
    if r.returncode == 0 and r.stdout.strip():
        print("\n最近的 release:")
        for line in r.stdout.strip().splitlines():
            print("   " + line)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--latest-only", action="store_true", help="只刷新 latest 的 asset（不改 tag）")
    ap.add_argument("--status", action="store_true", help="只看状态")
    args = ap.parse_args()

    if args.status:
        return do_status()

    p = pkg()
    version = p["version"]
    tag = "v" + version
    repo_slug = p["name"]

    print("\n%s v%s  ->  %s" % (p["displayName"], version, REPO))
    if args.dry_run:
        print("  [dry-run] 将构建 %s-%s.vsix 与 %s" % (repo_slug, version, ASSET_STABLE))
        print("  [dry-run] 将发布 tag %s（已存在则更新 asset）" % tag)
        print("  [dry-run] 稳定下载 URL: https://github.com/%s/releases/latest/download/%s"
              % (REPO, ASSET_STABLE))
        return 0

    versioned, stable = build()
    print("  产物: %s / %s" % (os.path.basename(versioned), os.path.basename(stable)))

    if release_exists(tag):
        print("  · tag %s 已存在，更新 asset" % tag)
        gh("release", "upload", tag, versioned, stable, "--repo", REPO, "--clobber")
    else:
        sec = changelog_section(version)
        notes = "%s v%s\n\n%s\n\n---\n\n" \
                "**安装**（首次装完需重启一次 Devin）\n\n" \
                "```powershell\n" \
                "Get-Process Devin -ErrorAction SilentlyContinue | Stop-Process -Force\n" \
                "& \"$env:LOCALAPPDATA\\Programs\\Devin\\bin\\devin-desktop.cmd\" " \
                "--install-extension .\\%s\n" \
                "Remove-Item Env:\\ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue\n" \
                "Start-Process \"$env:LOCALAPPDATA\\Programs\\Devin\\Devin.exe\"\n" \
                "```\n" % (p["displayName"], version, sec or "见 CHANGELOG。", ASSET_STABLE)
        gh("release", "create", tag, versioned, stable,
           "--repo", REPO,
           "--title", "%s v%s" % (p["displayName"], version),
           "--notes", notes)
        print("  ✓ 已创建 release %s" % tag)

    print("\n完成。用户下载入口:")
    print("  最新版 : https://github.com/%s/releases/latest/download/%s" % (REPO, ASSET_STABLE))
    print("  所有版 : https://github.com/%s/releases" % REPO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
