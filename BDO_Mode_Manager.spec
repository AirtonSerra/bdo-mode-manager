from pathlib import Path
import shutil
import os
from PyInstaller.utils.win32.versioninfo import (
    VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct,
    VarFileInfo, VarStruct,
)

root = Path(SPECPATH)
build_version = os.environ.get('BDO_BUILD_VERSION') or (root / 'VERSION').read_text().strip()
version_tuple = tuple(int(part) for part in build_version.split('.')) + (0,)
version_info = VSVersionInfo(
    ffi=FixedFileInfo(filevers=version_tuple, prodvers=version_tuple,
                      mask=0x3f, flags=0, OS=0x40004, fileType=1, subtype=0, date=(0, 0)),
    kids=[StringFileInfo([StringTable('041604B0', [
        StringStruct('CompanyName', 'Salazas Corp'),
        StringStruct('FileDescription', 'BDO Mode Manager'),
        StringStruct('FileVersion', build_version + '.0'),
        StringStruct('ProductName', 'BDO Mode Manager'),
        StringStruct('ProductVersion', build_version),
        StringStruct('OriginalFilename', 'BDO Mode Manager.exe'),
        StringStruct('LegalCopyright', 'Copyright (c) 2026 Airton Sena (Salazas)'),
    ])]), VarFileInfo([VarStruct('Translation', [0x0416, 1200])])],
)
a = Analysis(
    [str(root / 'BDO_Mode_Manager.pyw')],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / name), name) for name in ('assets', 'game_modes')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [], exclude_binaries=True,
    name='BDO Mode Manager', console=False, upx=False,
    icon=str(root / 'assets/bdo-mode-manager-spirit-outline.ico'),
    contents_directory='.',
    version=version_info,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False,
               name='BDO Mode Manager')
# DXVK é conteúdo destinado ao jogo, não uma dependência do executável.
# Copiar depois evita que a análise de DLLs coloque dxgi.dll na raiz do app.
shutil.copytree(root / 'bin64', Path(coll.name) / 'bin64', dirs_exist_ok=True)
