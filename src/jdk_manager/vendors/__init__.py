from pathlib import Path
from typing import Callable

from .zulu import install as _zulu
from .temurin import install as _temurin

# 새 vendor 추가 시 여기에 등록
REGISTRY: dict[str, Callable[[Path, int], Path]] = {
    "zulu": _zulu,
    "temurin": _temurin,
}
