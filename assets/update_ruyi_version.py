#!/usr/bin/env python3
"""Update pinned ruyi installation versions to the latest tagged version."""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


TAGS_MIRROR_URL = "https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/"
EXCLUDED_ROOT_DIRECTORIES = {".git", "assets", "templates"}
VERSION_PATTERN = re.compile(
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
)
TAG_LINK_PATTERN = re.compile(
    r'href=["\'](?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)/["\']'
)
RUYI_URL_PATTERN = re.compile(
    r"(ruyisdk/ruyi/tags/)\d+\.\d+\.\d+"
    r"(/ruyi-)\d+\.\d+\.\d+"
    r"(\.(?:amd64|arm64|riscv64))"
)
LOCAL_BINARY_PATTERN = re.compile(
    r"(\./ruyi-)\d+\.\d+\.\d+"
    r"(\.(?:amd64|arm64|riscv64))"
)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Update pinned ruyi versions in board documentation."
    )
    parser.add_argument(
        "--version",
        type=parse_version,
        help="use this X.Y.Z version instead of checking the tags mirror",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check for outdated URLs without changing files",
    )
    return parser.parse_args()


def parse_version(value: str) -> str:
    """Validate and return a semantic version string."""

    if VERSION_PATTERN.fullmatch(value) is None:
        raise argparse.ArgumentTypeError("version must use the X.Y.Z format")
    return value


def version_tuple(match: re.Match[str]) -> tuple[int, int, int]:
    """Return the numeric version represented by a regex match."""

    return tuple(
        int(match.group(name)) for name in ("major", "minor", "patch")
    )


def detect_latest_version() -> str:
    """Return the numerically greatest version listed by the tags mirror."""

    request = urllib.request.Request(
        TAGS_MIRROR_URL,
        headers={"User-Agent": "board-docs-ruyi-version-updater"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        listing = response.read().decode("utf-8")

    versions = [version_tuple(match) for match in TAG_LINK_PATTERN.finditer(listing)]
    if not versions:
        raise ValueError(f"no X.Y.Z versions found at {TAGS_MIRROR_URL}")
    return ".".join(str(part) for part in max(versions))


def markdown_paths(root: Path) -> list[Path]:
    """List Markdown files outside excluded top-level directories."""

    paths: list[Path] = []
    for directory, directory_names, file_names in os.walk(root):
        current_directory = Path(directory)
        if current_directory == root:
            directory_names[:] = [
                name
                for name in directory_names
                if name not in EXCLUDED_ROOT_DIRECTORIES
            ]
        paths.extend(
            current_directory / name
            for name in file_names
            if name.endswith(".md")
        )
    return sorted(paths)


def updated_document(document: str, version: str) -> str:
    """Return a document with its pinned ruyi versions replaced."""

    updated = RUYI_URL_PATTERN.sub(
        lambda match: (
            f"{match.group(1)}{version}{match.group(2)}"
            f"{version}{match.group(3)}"
        ),
        document,
    )
    return LOCAL_BINARY_PATTERN.sub(
        lambda match: f"{match.group(1)}{version}{match.group(2)}",
        updated,
    )


def collect_updates(
    root: Path, version: str
) -> list[tuple[Path, bytes, bytes]]:
    """Collect changed document bytes without writing them."""

    updates: list[tuple[Path, bytes, bytes]] = []
    for path in markdown_paths(root):
        original_bytes = path.read_bytes()
        original = original_bytes.decode("utf-8")
        updated = updated_document(original, version)
        updated_bytes = updated.encode("utf-8")
        if updated_bytes != original_bytes:
            updates.append((path, original_bytes, updated_bytes))
    return updates


def write_updates(updates: list[tuple[Path, bytes, bytes]]) -> None:
    """Write updates and restore attempted files if any write fails."""

    attempted: list[tuple[Path, bytes]] = []
    try:
        for path, original_bytes, updated_bytes in updates:
            attempted.append((path, original_bytes))
            path.write_bytes(updated_bytes)
    except OSError as write_error:
        try:
            for path, original_bytes in reversed(attempted):
                path.write_bytes(original_bytes)
        except OSError as rollback_error:
            raise OSError(
                f"{write_error}; rollback failed for {path}: {rollback_error}"
            ) from write_error
        raise


def display_paths(paths: list[Path], root: Path) -> None:
    """Print repository-relative paths in a stable format."""

    for path in paths:
        print(f"- {path.relative_to(root).as_posix()}")


def main() -> int:
    """Detect or select a version, then update or check documentation."""

    arguments = parse_arguments()
    repository_root = Path(__file__).resolve().parent.parent

    try:
        target_version = arguments.version or detect_latest_version()
        updates = collect_updates(repository_root, target_version)
    except (
        OSError,
        UnicodeError,
        ValueError,
        urllib.error.URLError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"Target version: {target_version}")
    changed_paths = [path for path, _, _ in updates]
    if arguments.check:
        if changed_paths:
            print("Files with outdated ruyi installation versions:")
            display_paths(changed_paths, repository_root)
            return 1
        print("All ruyi installation versions are up-to-date.")
        return 0

    if not updates:
        print("All ruyi installation versions are up-to-date.")
        return 0

    try:
        write_updates(updates)
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print("Updated files:")
    display_paths(changed_paths, repository_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
