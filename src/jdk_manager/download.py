import hashlib
from pathlib import Path
from urllib.parse import urlparse

import requests


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def download_archive(url: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(urlparse(url).path).name
    dest_path = dest_dir / filename

    if dest_path.exists():
        print(f"Already downloaded: {dest_path}")
        return dest_path

    print(f"Downloading to {dest_path} ...")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        downloaded = 0
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded / total * 100
                        mb_done = downloaded / 1024 / 1024
                        mb_total = total / 1024 / 1024
                        print(f"\r  {mb_done:.1f} / {mb_total:.1f} MB ({pct:.0f}%)", end="", flush=True)
    print()

    return dest_path
