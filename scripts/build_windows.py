"""Gera o executável e o instalador por usuário (Windows x64)."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def build(version, iscc=None):
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        raise ValueError("Use uma versão no formato v1.0.0.")
    if sys.platform != "win32" or sys.maxsize <= 2**32:
        raise RuntimeError("Execute com Python de 64 bits no Windows.")
    compiler = iscc or shutil.which("ISCC")
    if not compiler:
        for variable in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"):
            base = Path(os.environ.get(variable, "C:/"))
            for candidate in (base / "Inno Setup 6/ISCC.exe",
                              base / "Programs/Inno Setup 6/ISCC.exe"):
                if candidate.is_file():
                    compiler = str(candidate)
                    break
            if compiler:
                break
    if not compiler:
        raise RuntimeError("Instale Inno Setup 6 ou informe --iscc caminho/ISCC.exe.")
    subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
                    str(ROOT / "BDO_Mode_Manager.spec")], cwd=ROOT, check=True,
                   env=dict(os.environ, BDO_BUILD_VERSION=version[1:]))
    bundle = ROOT / "dist/BDO Mode Manager"
    for name in ("BDO Mode Manager.exe", "assets/bdo-mode-manager-spirit-outline.ico",
                 "assets/bdo-mode-manager-title.png", "bin64/d3d11.dll", "bin64/dxgi.dll",
                 "game_modes/Normal/dxvk.conf", "game_modes/Batata/dxvk.conf"):
        if not (bundle / name).is_file():
            raise FileNotFoundError(bundle / name)
    if (bundle / "config.json").exists():
        raise RuntimeError("O pacote não deve incluir configuração pessoal.")
    if (bundle / "dxgi.dll").exists() or (bundle / "d3d11.dll").exists():
        raise RuntimeError("As DLLs DXVK devem ficar apenas em bin64, destinadas ao jogo.")
    subprocess.run([compiler, f"/DAppVersion={version[1:]}", f"/DBuildDir={bundle}",
                    f"/DOutputDir={ROOT / 'dist'}",
                    str(ROOT / "installer/BDO_Mode_Manager.iss")], check=True, cwd=ROOT)
    installer = ROOT / f"dist/BDO-Mode-Manager-{version}-Setup.exe"
    digest = hashlib.sha256(installer.read_bytes()).hexdigest()
    installer.with_suffix(".exe.sha256").write_text(
        f"{digest}  {installer.name}\n", encoding="utf-8")
    return installer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", default="v" + (ROOT / "VERSION").read_text().strip())
    parser.add_argument("--iscc")
    args = parser.parse_args()
    print(build(args.version, args.iscc))
