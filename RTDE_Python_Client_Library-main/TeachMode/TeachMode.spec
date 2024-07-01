# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['LogandMoveGUI.py'],
             pathex=[r'C:\Users\Engineering\Downloads\RTDE_Python_Client_Library-main\RTDE_Python_Client_Library-main\examples'],
             binaries=[],
             datas=[('eagle_composites_logo.ico', '.'), ('eagle_composites_logo.jpg', '.')],
             hiddenimports=['logJointValues', 'freedrive', 'move'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='TeachMode',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )