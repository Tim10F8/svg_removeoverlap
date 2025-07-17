# this_file: svg_removeoverlap.spec
# PyInstaller spec file for building standalone binary

import sys
from pathlib import Path

# Get the source directory
src_dir = Path(__file__).parent / "src"

a = Analysis(
    [str(src_dir / "svg_removeoverlap" / "__main__.py")],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'svg_removeoverlap.remover',
        'svg_removeoverlap.remover_cairo_skia',
        'svg_removeoverlap.remover_skia',
        'picosvg.svg',
        'picosvg.svg_pathops',
        'cairosvg',
        'lxml',
        'tinycss2',
        'fire',
        'tqdm',
        'skia',
        'pathops',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='svg_removeoverlap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)