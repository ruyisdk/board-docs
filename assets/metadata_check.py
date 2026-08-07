#!/usr/bin/env python3
"""Validate YAML front matter in board and example documentation."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


PLACEHOLDER = re.compile(r"^\[[^\[\]]+\]$")
EXCLUDED_ROOT_DIRECTORIES = {
    ".git",
    ".github",
    "assets",
    "boards",
    "templates",
    "tools",
}


class FieldRules(BaseModel):
    """Required, optional, and forbidden fields for one document type."""

    required: list[str]
    optional: list[str] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)


class MetadataRules(BaseModel):
    """Repository metadata rules loaded from metadata.yml."""

    board: FieldRules
    example: FieldRules
    categories: list[str]


class BoardMetadata(BaseModel):
    """Metadata consumed from a board README."""

    model_config = ConfigDict(extra="allow")

    product: str
    cpu: str
    cpu_core: str
    ram: str
    vendor: str
    silicon_vendor: str

    @field_validator("*", mode="after")
    @classmethod
    def reject_empty_strings(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            raise ValueError("must not be empty")
        return value


class ExampleMetadata(BaseModel):
    """Metadata consumed from an example document."""

    model_config = ConfigDict(extra="allow")

    sys: str
    sys_ver: str | None
    sys_var: str | None
    provider: str | None = None
    category: str
    last_update: dt.date
    model: str
    profile: str

    @field_validator("sys_ver", "sys_var", "profile", mode="before")
    @classmethod
    def convert_identifier_values_to_strings(cls, value: Any) -> str | None:
        if value is None:
            return None
        return str(value)

    @field_validator("*", mode="after")
    @classmethod
    def reject_empty_strings(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            raise ValueError("must not be empty")
        return value


@dataclass(frozen=True)
class CheckError:
    """One validation error associated with a repository path."""

    path: Path
    message: str


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Validate board-docs YAML front matter."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=repository_root,
        help="repository root (default: parent of the assets directory)",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=Path(__file__).with_name("metadata.yml"),
        help="metadata rules file",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def load_rules(path: Path) -> MetadataRules:
    """Load and validate repository metadata rules."""

    with path.open("r", encoding="utf-8") as stream:
        raw_rules = yaml.safe_load(stream)
    return MetadataRules.model_validate(raw_rules)


def relative_path(path: Path, root: Path) -> Path:
    """Return a repository-relative path for diagnostics."""

    try:
        return path.relative_to(root)
    except ValueError:
        return path


def has_frontmatter(text: str) -> bool:
    """Return whether a Markdown document starts with YAML front matter."""

    return text.startswith("---\n") or text.startswith("---\r\n")


def find_placeholder(value: Any, field: str = "") -> str | None:
    """Find a template placeholder left in parsed metadata."""

    if isinstance(value, str) and PLACEHOLDER.fullmatch(value.strip()):
        return field or "metadata"
    if isinstance(value, list):
        for index, item in enumerate(value):
            result = find_placeholder(item, f"{field}[{index}]")
            if result:
                return result
    if isinstance(value, dict):
        for key, item in value.items():
            result = find_placeholder(item, f"{field}.{key}" if field else str(key))
            if result:
                return result
    return None


def load_document_metadata(
    path: Path, root: Path, *, required: bool
) -> tuple[dict[str, Any] | None, list[CheckError]]:
    """Parse one Markdown document's front matter."""

    display_path = relative_path(path, root)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        return None, [CheckError(display_path, f"is not valid UTF-8: {error}")]

    if not has_frontmatter(text):
        if required:
            return None, [CheckError(display_path, "missing YAML front matter")]
        return None, []

    try:
        post = frontmatter.loads(text)
    except (yaml.YAMLError, TypeError, ValueError) as error:
        return None, [CheckError(display_path, f"invalid YAML front matter: {error}")]

    metadata = dict(post.metadata)
    placeholder = find_placeholder(metadata)
    if placeholder:
        return metadata, [
            CheckError(display_path, f"field {placeholder!r} contains a template placeholder")
        ]
    return metadata, []


def validation_errors(
    path: Path, root: Path, error: ValidationError, *, skip_missing: bool = False
) -> list[CheckError]:
    """Convert Pydantic errors to concise repository diagnostics."""

    display_path = relative_path(path, root)
    results: list[CheckError] = []
    for item in error.errors(include_url=False):
        if skip_missing and item["type"] == "missing":
            continue
        location = ".".join(str(part) for part in item["loc"]) or "metadata"
        results.append(CheckError(display_path, f"{location}: {item['msg']}"))
    return results


def missing_and_forbidden_errors(
    path: Path,
    root: Path,
    metadata: dict[str, Any],
    rules: FieldRules,
) -> list[CheckError]:
    """Check field presence before type validation."""

    display_path = relative_path(path, root)
    errors = [
        CheckError(display_path, f"missing required field {field!r}")
        for field in rules.required
        if field not in metadata
    ]
    errors.extend(
        CheckError(display_path, f"forbidden legacy field {field!r}")
        for field in rules.forbidden
        if field in metadata
    )
    return errors


def validate_board_document(
    path: Path,
    root: Path,
    rules: MetadataRules,
    *,
    required: bool,
) -> tuple[BoardMetadata | None, list[CheckError]]:
    """Validate one board document."""

    metadata, errors = load_document_metadata(path, root, required=required)
    if metadata is None:
        return None, errors

    field_errors = missing_and_forbidden_errors(path, root, metadata, rules.board)
    errors.extend(field_errors)

    try:
        return BoardMetadata.model_validate(metadata), errors
    except ValidationError as error:
        errors.extend(validation_errors(path, root, error, skip_missing=True))
        return None, errors


def validate_example_document(
    path: Path, root: Path, rules: MetadataRules
) -> tuple[ExampleMetadata | None, list[CheckError]]:
    """Validate one example document."""

    metadata, errors = load_document_metadata(path, root, required=True)
    if metadata is None:
        return None, errors

    field_errors = missing_and_forbidden_errors(path, root, metadata, rules.example)
    errors.extend(field_errors)

    raw_category = metadata.get("category")
    if isinstance(raw_category, str) and raw_category not in rules.categories:
        allowed = ", ".join(rules.categories)
        errors.append(
            CheckError(
                relative_path(path, root),
                f"category: unsupported value {raw_category!r}; allowed: {allowed}",
            )
        )

    try:
        parsed = ExampleMetadata.model_validate(metadata)
    except ValidationError as error:
        errors.extend(validation_errors(path, root, error, skip_missing=True))
        return None, errors

    return parsed, errors


def comparable_metadata(
    model: BaseModel, field_rules: FieldRules
) -> dict[str, Any]:
    """Return only documented fields for bilingual comparisons."""

    fields = set(field_rules.required + field_rules.optional)
    return model.model_dump(include=fields)


def compare_language_versions(
    first_path: Path,
    first: BaseModel | None,
    second_path: Path,
    second: BaseModel | None,
    root: Path,
    field_rules: FieldRules,
) -> list[CheckError]:
    """Require matching metadata when both language versions provide it."""

    if first is None or second is None:
        return []
    if comparable_metadata(first, field_rules) == comparable_metadata(second, field_rules):
        return []
    return [
        CheckError(
            relative_path(second_path, root),
            f"metadata does not match {relative_path(first_path, root)}",
        )
    ]


def board_directories(root: Path) -> list[Path]:
    """Discover current and future board directory layouts."""

    directories = {
        path
        for path in root.iterdir()
        if path.is_dir()
        and path.name not in EXCLUDED_ROOT_DIRECTORIES
        and not path.name.startswith(".")
    }
    boards_root = root / "boards"
    if boards_root.is_dir():
        directories.update(path for path in boards_root.iterdir() if path.is_dir())
    return sorted(directories)


def run_check(
    root: Path, rules: MetadataRules, *, verbose: bool = False
) -> tuple[list[CheckError], int, int]:
    """Validate all board and example documents in a repository."""

    errors: list[CheckError] = []
    board_count = 0
    example_document_count = 0

    for board_dir in board_directories(root):
        board_count += 1
        board_readme = board_dir / "README.md"
        board_zh_readme = board_dir / "README_zh.md"

        if not board_readme.is_file():
            errors.append(
                CheckError(relative_path(board_readme, root), "board README.md is missing")
            )
            continue

        if verbose:
            print(f"Checking board: {relative_path(board_readme, root)}")
        board, board_errors = validate_board_document(
            board_readme, root, rules, required=True
        )
        errors.extend(board_errors)

        board_zh: BoardMetadata | None = None
        if board_zh_readme.is_file():
            board_zh, board_zh_errors = validate_board_document(
                board_zh_readme, root, rules, required=False
            )
            errors.extend(board_zh_errors)
            errors.extend(
                compare_language_versions(
                    board_readme,
                    board,
                    board_zh_readme,
                    board_zh,
                    root,
                    rules.board,
                )
            )

        for example_dir in sorted(path for path in board_dir.iterdir() if path.is_dir()):
            markdown_files = [
                path
                for path in (
                    example_dir / "README.md",
                    example_dir / "README_zh.md",
                )
                if path.is_file()
            ]
            if not markdown_files:
                continue

            parsed_documents: dict[str, ExampleMetadata | None] = {}
            for document in markdown_files:
                example_document_count += 1
                if verbose:
                    print(f"Checking example: {relative_path(document, root)}")
                parsed, document_errors = validate_example_document(
                    document, root, rules
                )
                errors.extend(document_errors)
                parsed_documents[document.name] = parsed

            readme = example_dir / "README.md"
            readme_zh = example_dir / "README_zh.md"
            if readme.is_file() and readme_zh.is_file():
                errors.extend(
                    compare_language_versions(
                        readme,
                        parsed_documents.get("README.md"),
                        readme_zh,
                        parsed_documents.get("README_zh.md"),
                        root,
                        rules.example,
                    )
                )

    return errors, board_count, example_document_count


def main() -> int:
    """Run the metadata checker and return a process exit code."""

    arguments = parse_arguments()
    root = arguments.path.resolve()
    rules_path = arguments.rules.resolve()

    if not root.is_dir():
        print(f"error: repository path does not exist: {root}", file=sys.stderr)
        return 2

    try:
        rules = load_rules(rules_path)
    except (OSError, yaml.YAMLError, ValidationError) as error:
        print(f"error: cannot load metadata rules from {rules_path}: {error}", file=sys.stderr)
        return 2

    errors, board_count, example_document_count = run_check(
        root, rules, verbose=arguments.verbose
    )

    if errors:
        print(f"Metadata check failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error.path}: {error.message}", file=sys.stderr)
        return 1

    print(
        "Metadata check passed: "
        f"{board_count} board(s), {example_document_count} example document(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
