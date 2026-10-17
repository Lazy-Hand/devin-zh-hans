# -*- coding: utf-8 -*-
"""
_paths.py — 仓库内所有工具的公共路径解析

不写死任何用户目录：Devin 安装位置按常规顺序探测，也可用环境变量覆盖：
    DEVIN_INSTALL   例如 D:\Apps\Devin
    DEVIN_HOME      例如 ~/.devin
    DEVIN_PLUGIN    指定 plugins/ 下的插件目录名（默认 zh-hans）
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PLUGIN_NAME = os.environ.get("DEVIN_PLUGIN", "zh-hans")
PLUGIN = os.path.join(ROOT, "plugins", PLUGIN_NAME)
SHARED = os.path.join(ROOT, "shared", "dict")
DATA = os.path.join(HERE, "data")
OUT = os.path.join(ROOT, "dist")

_LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~/AppData/Local")
DEVIN_HOME = os.environ.get("DEVIN_HOME") or os.path.join(os.path.expanduser("~"), ".devin")
EXT_ROOT = os.path.join(DEVIN_HOME, "extensions")
BACKUP_ROOT = os.path.join(DEVIN_HOME, "devin-zh-backups")


def find_devin_install():
    """返回 Devin 安装根目录（含 Devin.exe），找不到返回 None。"""
    cands = [
        os.environ.get("DEVIN_INSTALL"),
        os.path.join(_LOCALAPPDATA, "Programs", "Devin"),
        r"C:\Program Files\Devin",
    ]
    for c in cands:
        if c and os.path.exists(os.path.join(c, "Devin.exe")):
            return c
    return None


def find_langpack():
    """返回已安装的简体中文语言包目录，找不到返回 None。"""
    if not os.path.isdir(EXT_ROOT):
        return None
    for d in sorted(os.listdir(EXT_ROOT)):
        if "language-pack-zh-hans" in d:
            p = os.path.join(EXT_ROOT, d)
            if os.path.exists(os.path.join(p, "translations", "main.i18n.json")):
                return p
    return None


DEVIN_INSTALL = find_devin_install()
DEVIN_APP = os.path.join(DEVIN_INSTALL, "resources", "app") if DEVIN_INSTALL else None
LANGPACK = find_langpack()

# 语言包清单（VS Code 的语言包缓存索引）
APPDATA = os.environ.get("APPDATA") or os.path.expanduser("~/AppData/Roaming")
LANGPACKS_JSON = os.path.join(APPDATA, "devin", "languagepacks.json")

CLI = os.path.join(DEVIN_INSTALL, "bin", "devin-desktop.cmd") if DEVIN_INSTALL else None
