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
