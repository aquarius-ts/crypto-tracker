# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['crypto_tracker_simple.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'websocket',
        'websocket._app',
        'websocket._core',
        'websocket._exceptions',
        'websocket._http',
        'websocket._socket',
        'websocket._ssl_compat',
        'websocket._url',
        'websocket._utils',
        'requests',
        'json',
        'threading',
        'tkinter',
        'tkinter.messagebox',
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
    name='CryptoTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Add icon file path here if you have one
)
