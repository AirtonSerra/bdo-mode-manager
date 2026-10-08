"""Monta o pacote do usuário final, sem compilar um executável."""

import argparse
import hashlib
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "BDO Mode Manager.lnk",
    "launch.vbs",
    "BDO_Mode_Manager.pyw",
    "README.md",
    "LICENSE",
    "assets/bdo-mode-manager-spirit-outline.ico",
    "assets/bdo-mode-manager-title.png",
    "bin64/d3d11.dll",
    "bin64/dxgi.dll",
    "game_modes/Batata/dxvk.conf",
    "game_modes/Normal/dxvk.conf",
)


def package(version, output):
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        raise ValueError("Use uma versão no formato v1.0.0.")
    for name in FILES:
        if not (ROOT / name).is_file():
            raise FileNotFoundError(name)
    compile((ROOT / "BDO_Mode_Manager.pyw").read_text(encoding="utf-8"), "app", "exec")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"BDO-Mode-Manager-{version}-Windows.zip"
    folder = f"BDO-Mode-Manager-{version}"
    with ZipFile(archive, "w", ZIP_DEFLATED) as zipped:
        for name in FILES:
            zipped.write(ROOT / name, f"{folder}/{name}")
    with ZipFile(archive) as zipped:
        assert zipped.testzip() is None
        assert set(zipped.namelist()) == {f"{folder}/{name}" for name in FILES}
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(
        f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version")
    parser.add_argument("--output", default="dist")
    arguments = parser.parse_args()
    print(package(arguments.version, arguments.output))
