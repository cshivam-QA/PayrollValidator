# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hidden = collect_submodules("jinja2")

a = Analysis(
    ['desktop_app.py'],
    pathex=[
        '.',
        './src',
    ],

    binaries=[],

    datas=[
        ('dashboard/templates', 'dashboard/templates'),
        ('dashboard/assets', 'dashboard/assets'),
    ],

    hiddenimports=hidden,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,

    [],

    name='XMLValidator',

    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,

    console=True,
)