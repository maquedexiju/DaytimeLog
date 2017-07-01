# -*- mode: python -*-

block_cipher = None


a = Analysis(['DaytimeLog.py'],
             pathex=['/Users/XuXiaotian/Git/DaytimeLog'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='DaytimeLog',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,Tree('/Users/XuXiaotian/Git/DaytimeLog/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='DaytimeLog')
app = BUNDLE(coll,
             name='DaytimeLog.app',
             icon=None,
             bundle_identifier=None)
