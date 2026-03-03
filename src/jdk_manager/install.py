import tarfile
from pathlib import Path

from .vendors import REGISTRY


def extract_and_install(archive_path: Path, vendor: str, major: int, java_version: str) -> Path:
    if vendor not in REGISTRY:
        raise NotImplementedError(f"Vendor '{vendor}' is not supported yet. Available: {list(REGISTRY)}")

    work_dir = archive_path.parent / f"{vendor}-{java_version}"
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"Extracting ...")
    with tarfile.open(archive_path) as tar:
        tar.extractall(work_dir)

    result = REGISTRY[vendor](work_dir, major)
    # shutil.rmtree(work_dir, ignore_errors=True)
    # archive_path.unlink(missing_ok=True)
    return result

