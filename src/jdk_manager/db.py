import json
import re
import time
from pathlib import Path

import requests
import pandas as pd


API_URL = "https://mise-java.jdx.dev/jvm/ga/macosx/aarch64.json"
CACHE_FILE = Path.home() / ".cache" / "jdk-manager" / "db.json"
CACHE_TTL = 60 * 60  # 1시간 (초)


def version_key(v: str, width: int = 4, include_build: bool = True) -> tuple[int, ...]:
    """
    Examples:
      "21.0.10"      -> (21, 0, 10, 0, 0)  # build=0
      "8.0.345"      -> (8, 0, 345, 0, 0)
      "11.0.30+7"    -> (11, 0, 30, 0, 7)
      "11.0.20.1+1"  -> (11, 0, 20, 1, 1)
      "11.0.22+7.1"  -> (11, 0, 22, 0, 7)  # "+7.1"이면 build는 첫 숫자만
    """
    s = "" if pd.isna(v) else str(v).strip()
    m = re.match(r"(?P<num>\d+(?:\.\d+)*)(?:\+(?P<build>\d+)(?:\.\d+)*)?", s)
    if not m:
        base = [0] * width
        return tuple(base + ([0] if include_build else []))

    num = m.group("num") or ""
    build = int(m.group("build")) if (include_build and m.group("build")) else 0

    parts = [int(x) for x in num.split(".") if x != ""]
    parts = (parts + [0] * width)[:width]

    return tuple(parts + ([build] if include_build else []))


def parse_package(package: str) -> tuple[str, int]:
    """'zulu-11' -> ('zulu', 11)"""
    parts = package.rsplit("-", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid package format: {package!r}. Expected 'vendor-major' (e.g. zulu-11)")
    vendor, major_str = parts
    try:
        major = int(major_str)
    except ValueError:
        raise ValueError(f"Invalid major version: {major_str!r}")
    return vendor, major


def fetch_db() -> pd.DataFrame:
    if CACHE_FILE.exists() and (time.time() - CACHE_FILE.stat().st_mtime) < CACHE_TTL:
        print("Loading JDK database from cache...")
        data = json.loads(CACHE_FILE.read_text())
    else:
        print("Fetching JDK database...")
        resp = requests.get(API_URL, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(data))

    return pd.DataFrame(data)


def list_vendors(df: pd.DataFrame) -> list[str]:
    return sorted(df["vendor"].dropna().unique().tolist())


def find_package(df: pd.DataFrame, vendor: str, major: int) -> pd.Series:
    df = df.loc[
        (df["vendor"] == vendor) &
        (df["image_type"] == "jdk") &
        (df["file_type"] == "tar.gz") &
        (df["features"].str.len() == 0)
    ].copy()

    df["java_version_key"] = df["java_version"].map(version_key)
    df = df.loc[df["java_version_key"].str[0] == major]
    df = df.sort_values(by=["java_version_key", "version"], ascending=[False, False])
    if df.empty:
        raise ValueError(f"No package found for {vendor}-{major}")

    return df.iloc[0]

