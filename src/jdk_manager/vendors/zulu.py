import shutil
from pathlib import Path


def install(work_dir: Path, major: int) -> Path:
    top_dirs = [p for p in work_dir.iterdir() if p.is_dir()]
    if len(top_dirs) != 1:
        raise RuntimeError(f"Expected one top-level dir in {work_dir}, got: {[p.name for p in top_dirs]}")
    top = top_dirs[0]

    # 심볼릭 링크 모두 삭제
    for entry in top.iterdir():
        if entry.is_symlink():
            entry.unlink()

    # zulu-{major}.jdk 디렉토리 찾기
    jdk_dir_name = f"zulu-{major}.jdk"
    jdk_dir = top / jdk_dir_name
    if not jdk_dir.exists():
        raise RuntimeError(f"{jdk_dir_name} not found in {top}")

    jdks_dir = Path.home() / "Library" / "Java" / "JavaVirtualMachines"
    jdks_dir.mkdir(parents=True, exist_ok=True)
    dest = jdks_dir / jdk_dir_name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(jdk_dir), str(dest))

    return dest.resolve()

