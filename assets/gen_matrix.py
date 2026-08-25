#!/usr/bin/env python3
"""Generate the supported development board matrices in the root READMEs."""

from __future__ import annotations

import argparse
import difflib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import frontmatter
import yaml

from metadata_check import EXCLUDED_ROOT_DIRECTORIES


BEGIN_MARKER = "<!-- MATRIX:BEGIN -->"
END_MARKER = "<!-- MATRIX:END -->"


@dataclass(frozen=True)
class BoardMetadata:
    """Metadata needed to render one board matrix row."""

    directory: Path
    product: str
    silicon_vendor: str


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Generate the supported development board matrices."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=repository_root,
        help="repository root (default: parent of the assets directory)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check whether the root README matrices are up to date",
    )
    return parser.parse_args()


def load_board_metadata(path: Path) -> BoardMetadata:
    """Load the product and silicon vendor fields from one board README."""

    post = frontmatter.loads(path.read_text(encoding="utf-8"))
    metadata: dict[str, Any] = post.metadata
    missing = [
        field
        for field in ("product", "silicon_vendor")
        if field not in metadata
    ]
    if missing:
        fields = ", ".join(missing)
        raise ValueError(f"{path}: missing frontmatter field(s): {fields}")

    product = metadata["product"]
    silicon_vendor = metadata["silicon_vendor"]
    if not isinstance(product, str) or not product.strip():
        raise ValueError(f"{path}: product must be a non-empty string")
    if not isinstance(silicon_vendor, str) or not silicon_vendor.strip():
        raise ValueError(f"{path}: silicon_vendor must be a non-empty string")

    return BoardMetadata(path.parent, product, silicon_vendor)


def discover_boards(root: Path) -> list[BoardMetadata]:
    """Discover top-level board directories with a README.md."""

    boards = [
        load_board_metadata(board_dir / "README.md")
        for board_dir in root.iterdir()
        if board_dir.is_dir()
        and not board_dir.name.startswith(".")
        and board_dir.name not in EXCLUDED_ROOT_DIRECTORIES
        and (board_dir / "README.md").is_file()
    ]
    return sorted(boards, key=lambda board: board.product.casefold())


def load_vendor_links(path: Path) -> dict[str, dict[str, str]]:
    """Load and validate the localized silicon vendor URL mapping."""

    raw_rules = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw_rules, dict):
        raise ValueError(f"{path}: metadata must be a mapping")
    links = raw_rules.get("silicon_vendor_links")
    if not isinstance(links, dict):
        raise ValueError(f"{path}: silicon_vendor_links must be a mapping")

    validated_links: dict[str, dict[str, str]] = {}
    for vendor, raw_urls in links.items():
        if not isinstance(vendor, str) or not isinstance(raw_urls, dict):
            raise ValueError(
                f"{path}: silicon_vendor_links entries must map names to language URLs"
            )
        localized_urls: dict[str, str] = {}
        for language in ("en", "zh"):
            url = raw_urls.get(language)
            parsed_url = urlparse(url) if isinstance(url, str) else None
            if (
                parsed_url is None
                or parsed_url.scheme not in {"http", "https"}
                or not parsed_url.netloc
            ):
                raise ValueError(
                    f"{path}: {vendor!r} must define a non-empty HTTP(S) "
                    f"{language!r} URL"
                )
            localized_urls[language] = url
        validated_links[vendor] = localized_urls
    return validated_links


def resolve_vendor_links(
    boards: list[BoardMetadata], links: dict[str, dict[str, str]]
) -> dict[str, tuple[str, dict[str, str] | None]]:
    """Resolve vendor labels and localized URLs, warning once for missing mappings."""

    folded_links = {vendor.casefold(): (vendor, url) for vendor, url in links.items()}
    resolved: dict[str, tuple[str, dict[str, str] | None]] = {}
    for board in boards:
        vendor = board.silicon_vendor
        if vendor in resolved:
            continue
        if vendor in links:
            resolved[vendor] = (vendor, links[vendor])
            continue
        match = folded_links.get(vendor.casefold())
        if match is None:
            print(
                f"warning: no URL configured for silicon vendor {vendor!r}; "
                "using plain text",
                file=sys.stderr,
            )
            resolved[vendor] = (vendor, None)
        else:
            resolved[vendor] = match
    return resolved


def render_matrix(
    boards: list[BoardMetadata],
    vendor_links: dict[str, tuple[str, dict[str, str] | None]],
    *,
    chinese: bool,
) -> str:
    """Render one language-specific Markdown support matrix."""

    if chinese:
        header = "| 支持设备 | 开发板文档 | 芯片厂商 |"
    else:
        header = "| Supported Device | Board Documentation | Chip Vendor |"
    rows = [header, "| --- | --- | --- |"]

    for board in boards:
        readme_name = "README_zh.md" if chinese else "README.md"
        readme_path = board.directory / readme_name
        if not readme_path.is_file():
            readme_name = "README.md"
            readme_path = board.directory / readme_name
        board_link = f"./{board.directory.name}/{readme_path.name}"
        vendor_name, localized_urls = vendor_links[board.silicon_vendor]
        vendor_url = (
            localized_urls.get("zh" if chinese else "en")
            if localized_urls is not None
            else None
        )
        vendor_cell = (
            f"[{vendor_name}]({vendor_url})"
            if vendor_url is not None
            else vendor_name
        )
        rows.append(
            f"| {board.product} | [{board.directory.name}]({board_link}) | "
            f"{vendor_cell} |"
        )
    return "\n".join(rows)


def replace_matrix(document: str, matrix: str) -> str:
    """Replace the content between the matrix markers in one README."""

    if document.count(BEGIN_MARKER) != 1 or document.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one pair of matrix markers")
    begin = document.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = document.index(END_MARKER, begin)
    if end < begin:
        raise ValueError("README matrix markers are out of order")
    return f"{document[:begin]}\n{matrix}\n{document[end:]}"


def expected_document(path: Path, matrix: str) -> str:
    """Return a README with its matrix replaced by generated content."""

    return replace_matrix(path.read_text(encoding="utf-8"), matrix)


def print_diff(path: Path, current: str, expected: str) -> None:
    """Print a unified diff for an out-of-date README matrix."""

    diff = difflib.unified_diff(
        current.splitlines(keepends=True),
        expected.splitlines(keepends=True),
        fromfile=str(path),
        tofile=f"{path} (generated)",
    )
    print(f"README matrix is out of date: {path}", file=sys.stderr)
    sys.stderr.writelines(diff)


def main() -> int:
    """Generate or check both root README support matrices."""

    arguments = parse_arguments()
    root = arguments.path.resolve()
    rules_path = Path(__file__).with_name("metadata.yml")

    try:
        boards = discover_boards(root)
        links = load_vendor_links(rules_path)
        vendor_links = resolve_vendor_links(boards, links)
        matrices = {
            root / "README.md": render_matrix(boards, vendor_links, chinese=False),
            root / "README_zh.md": render_matrix(boards, vendor_links, chinese=True),
        }
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    mismatches = 0
    for path, matrix in matrices.items():
        try:
            current = path.read_text(encoding="utf-8")
            expected = replace_matrix(current, matrix)
        except (OSError, ValueError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 2

        if arguments.check:
            if current != expected:
                print_diff(path, current, expected)
                mismatches += 1
        elif current != expected:
            path.write_text(expected, encoding="utf-8")
            print(f"Updated {path}")

    if arguments.check and mismatches:
        return 1
    if arguments.check:
        print("README matrices are up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
