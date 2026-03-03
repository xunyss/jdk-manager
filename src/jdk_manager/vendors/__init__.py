from pathlib import Path
from typing import Callable

from .graalvm_community import install as _graalvm_community
from .temurin import install as _temurin
from .zulu import install as _zulu


# 새 vendor 추가 시 여기에 등록
REGISTRY: dict[str, Callable[[Path, int], Path]] = {
    "graalvm-community": _graalvm_community,
    "temurin": _temurin,
    "zulu": _zulu,
}

# 설치 디렉토리명 규칙 (vendor별로 다를 수 있음)
INSTALL_DIR_NAMES: dict[str, Callable[[int], str]] = {
    "graalvm-community": lambda major: f"graalvm-ce-{major}.jdk",
    "temurin": lambda major: f"temurin-{major}.jdk",
    "zulu": lambda major: f"zulu-{major}.jdk",
}

