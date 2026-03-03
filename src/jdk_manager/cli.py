import shutil
import subprocess
import sys
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "jdk-manager"

from .db import fetch_db, find_package, list_vendors, parse_package
from .download import download_archive, sha256_file
from .install import extract_and_install


def cmd_download(package: str) -> None:
    vendor, major = parse_package(package)

    df = fetch_db()

    row = find_package(df, vendor, major)
    download_url = row["url"]
    java_version = row["java_version"]

    print(f"Found: {vendor}-{java_version}")
    print(f"URL:   {download_url}")

    dest_path = download_archive(download_url, CACHE_DIR)
    print(f"Downloaded: {dest_path.resolve()}")


def cmd_install(package: str) -> None:
    vendor, major = parse_package(package)

    df = fetch_db()

    row = find_package(df, vendor, major)
    download_url = row["url"]
    expected_checksum = str(row["checksum"]).removeprefix("sha256:").lower()
    java_version = row["java_version"]

    print(f"Found: {vendor}-{java_version}")
    print(f"URL:   {download_url}")

    dest_path = download_archive(download_url, CACHE_DIR)

    print("Verifying checksum...")
    actual = sha256_file(dest_path)
    if actual != expected_checksum:
        dest_path.unlink()
        raise RuntimeError(
            f"Checksum mismatch!\n  expected: {expected_checksum}\n  actual:   {actual}"
        )

    installed = extract_and_install(dest_path, vendor, major, java_version)
    print(f"Installed: {installed}")


def cmd_uninstall(package: str) -> None:
    vendor, major = parse_package(package)
    jdk_dir_name = f"{vendor}-{major}.jdk"
    target = Path.home() / "Library" / "Java" / "JavaVirtualMachines" / jdk_dir_name

    if not target.exists():
        raise FileNotFoundError(f"{jdk_dir_name} not found in {target.parent}")

    shutil.rmtree(target)
    print(f"Uninstalled: {target}")


def cmd_home() -> None:
    result = subprocess.run(["/usr/libexec/java_home", "-V"], capture_output=True, text=True)
    output = result.stdout + result.stderr  # java_home -V 는 stderr 로 출력함
    print(output, end="")


def cmd_vendor() -> None:
    df = fetch_db()
    for vendor in list_vendors(df):
        print(vendor)


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("usage: jdk [command] [jdk-package]")
        return

    command, *rest = args

    if command == "download":
        if not rest:
            print("usage: jdk download <vendor>-<major>  (e.g. jdk download zulu-11)")
            sys.exit(1)
        cmd_download(rest[0])
    elif command == "install":
        if not rest:
            print("usage: jdk install <vendor>-<major>  (e.g. jdk install zulu-11)")
            sys.exit(1)
        cmd_install(rest[0])
    elif command == "uninstall":
        if not rest:
            print("usage: jdk uninstall <vendor>-<major>  (e.g. jdk uninstall zulu-11)")
            sys.exit(1)
        cmd_uninstall(rest[0])
    elif command == "home":
        cmd_home()
    elif command == "vendor":
        cmd_vendor()
    else:
        print(f"Unknown command: {command!r}")
        print("usage: jdk [command] [jdk-package]")
        sys.exit(1)
