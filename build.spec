# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for MarkItDown App."""

import importlib.util
import sys
from pathlib import Path

block_cipher = None


def collect_package_data(package_name):
    """Collect all non-Python data files from a package."""
    spec = importlib.util.find_spec(package_name)
    if spec is None or spec.origin is None:
        return []
    pkg_dir = str(Path(spec.origin).parent)
    datas = []
    for p in Path(pkg_dir).rglob("*"):
        if p.is_file() and p.suffix not in (".py", ".pyc"):
            datas.append((str(p), str(p.parent.relative_to(Path(pkg_dir).parent))))
    return datas


# Collect magika model files and config (required at runtime)
magika_datas = collect_package_data("magika")

a = Analysis(
    ["src/markitdown_app/main.py"],
    pathex=["src"],
    binaries=[],
    datas=magika_datas,
    hiddenimports=[
        "markitdown",
        "markitdown._markitdown",
        "markitdown._base_converter",
        "markitdown._stream_info",
        "markdownify",
        "beautifulsoup4",
        "bs4",
        "magika",
        "magika.magika",
        "magika.types",
        "magika.types.magika_error",
        "charset_normalizer",
        "defusedxml",
        "pdfminer",
        "pdfminer.high_level",
        "pptx",
        "openpyxl",
        "xlrd",
        "docx",
        "PIL",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="MarkItDown",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add .ico path here for custom icon
)
