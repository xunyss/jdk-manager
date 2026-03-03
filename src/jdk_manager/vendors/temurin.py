import shutil
from pathlib import Path


def install(work_dir: Path, major: int) -> Path:
    # 압축 해제 후 최상위 디렉토리 1개 (예: jdk-17.0.18+8)
    top_dirs = [p for p in work_dir.iterdir() if p.is_dir()]
    if len(top_dirs) != 1:
        raise RuntimeError(f"Expected one top-level dir in {work_dir}, got: {[p.name for p in top_dirs]}")
    top = top_dirs[0]

    # 이름을 temurin-{major}.jdk 으로 변경하며 설치 디렉토리로 이동
    jdk_dir_name = f"temurin-{major}.jdk"
    jdks_dir = Path.home() / "Library" / "Java" / "JavaVirtualMachines"
    jdks_dir.mkdir(parents=True, exist_ok=True)
    dest = jdks_dir / jdk_dir_name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(top), str(dest))

    return dest.resolve()

