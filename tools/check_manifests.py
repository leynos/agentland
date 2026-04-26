#!/usr/bin/env python3
"""Validate Agentland asset manifest structure.

This module enforces the canonical manifest schema defined in
``docs/asset-spec.md`` and ``assets/manifests/README.md``. It recursively
validates all JSON files under ``assets/manifests/``, checking required
fields, enum values, nested object structures, and optional path existence.
Validation functions return ``ValidationError`` values so domain validation stays
separate from command-line rendering.

Usage
-----
Run directly or via the Makefile target::

    python tools/check_manifests.py --root /path/to/repo
    make manifest-check

Exit code is non-zero if any manifest fails validation.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

ALLOWED_BUCKETS = {
    "direct-generated-reference",
    "generated-source-converted",
    "algorithmic",
}

ALLOWED_INTENT_CLASSES = {
    "reference-only",
    "sliceable-source",
    "ornament-source",
    "runtime-processed",
    "lightmask-source",
    "layout-reference",
}

ALLOWED_FAMILIES = {
    "style-guide",
    "character-reference",
    "animation-reference",
    "environment-reference",
    "prop-cutout",
    "ui-ornament-reference",
    "texture-reference",
    "atlas",
    "lightmask",
}

ALLOWED_STATUSES = {
    "approved-source",
    "approved-runtime",
    "reference-only",
    "rejected",
    "superseded",
}

REQUIRED_TOP_LEVEL = {
    "id",
    "family",
    "status",
    "bucket",
    "intent_class",
    "tool",
    "prompt",
    "files",
    "source_asset",
    "asset_contract",
    "postprocess",
    "validation",
    "runtime_use",
    "notes",
}

REQUIRED_FILES = {
    "codex_generated_path",
    "workspace_source_path",
    "processed_path",
    "atlas_image_path",
    "atlas_metadata_path",
    "validation_report_path",
}

REQUIRED_TOOL = {
    "mode",
    "model_family",
    "fallback_cli",
    "cli_reason",
}

REQUIRED_PROMPT = {
    "path",
    "use_case",
    "asset_type",
    "text",
    "input_images",
}

REQUIRED_SOURCE_ASSET = {
    "dimensions",
    "format",
    "has_alpha",
    "intended_scale",
    "source_kind",
}

REQUIRED_ASSET_CONTRACT = {
    "focal_role",
    "layer",
    "anchor",
    "hit_area",
    "screen_regions",
    "text_policy",
}

REQUIRED_POSTPROCESS = {
    "steps",
    "palette",
    "quantized_path",
    "crop",
    "slice",
    "nine_slice",
    "atlas",
    "background_removal",
}

REQUIRED_VALIDATION = {
    "subject_correct",
    "style_match",
    "text_accuracy",
    "alpha_valid",
    "transparent_corners",
    "visible_key_fringe",
    "palette_fit",
    "scale_check",
    "sprite_bounds_valid",
    "atlas_metadata_valid",
    "runtime_text_safe",
    "approved_by",
    "notes",
    "rejection_notes",
}

REQUIRED_RUNTIME_USE = {
    "kind",
    "consumer",
    "layer",
    "asset_id",
    "notes",
}


@dataclass(frozen=True)
class ValidationError:
    """A manifest validation failure for one logical field."""

    field: str
    message: str


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    argv : list[str] | None
        Command-line argument strings, or ``None`` to read from ``sys.argv``.

    Returns
    -------
    argparse.Namespace
        Parsed command arguments.

    Raises
    ------
    SystemExit
        Raised by ``argparse`` when arguments are invalid.
    """
    parser = argparse.ArgumentParser(
        description="Validate JSON manifests under assets/manifests."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    return parser.parse_args(argv)


def manifest_paths(root: Path) -> list[Path]:
    """Return manifest JSON files below the repository manifest directory.

    Parameters
    ----------
    root : Path
        Repository root used to locate ``assets/manifests``.

    Returns
    -------
    list[Path]
        Sorted manifest JSON file paths, or an empty list when the manifest
        directory does not exist.
    """
    manifest_root = root / "assets" / "manifests"
    if not manifest_root.exists():
        return []
    return sorted(manifest_root.rglob("*.json"))


def require_mapping(value: Any, field: str, errors: list[ValidationError]) -> bool:
    """Check that a value is an object before nested validation.

    Parameters
    ----------
    value : Any
        Candidate value to validate.
    field : str
        Logical field name used in validation errors.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    bool
        ``True`` when ``value`` is a dictionary, otherwise ``False``.
    """
    if isinstance(value, dict):
        return True
    errors.append(ValidationError(field, "must be an object"))
    return False


def require_keys(
    value: dict[str, Any],
    required: set[str],
    field: str,
    errors: list[ValidationError],
) -> None:
    """Append errors for missing required keys.

    Parameters
    ----------
    value : dict[str, Any]
        Mapping to inspect for required keys.
    required : set[str]
        Required key names.
    field : str
        Field prefix used in validation errors.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    missing = sorted(required.difference(value))
    errors.extend(ValidationError(f"{field}.{key}", "is required") for key in missing)


def validate_enum(
    value: Any, allowed: set[str], field: str, errors: list[ValidationError]
) -> None:
    """Validate a string enum value.

    Parameters
    ----------
    value : Any
        Candidate enum value.
    allowed : set[str]
        Accepted string values.
    field : str
        Logical field name used in validation errors.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    if not isinstance(value, str):
        errors.append(ValidationError(field, "must be a string"))
        return
    if value not in allowed:
        expected = ", ".join(sorted(allowed))
        errors.append(
            ValidationError(
                field,
                f"{field} has invalid value {value!r}; expected {expected}",
            )
        )


def _resolved_path_exists(root: Path, value: str) -> bool:
    """Return True when value resolves to an existing path inside root."""
    root_path = root.resolve()
    candidate = (root_path / Path(value)).resolve()
    try:
        candidate.relative_to(root_path)
    except ValueError:
        return False
    return candidate.exists()


def validate_optional_path(
    root: Path, value: Any, field: str, errors: list[ValidationError]
) -> None:
    """Validate an optional repository-relative path field.

    Parameters
    ----------
    root : Path
        Repository root that valid paths must stay within.
    value : Any
        Candidate repository-relative path, ``None``, or allowed Codex path.
    field : str
        Logical field name used in validation errors.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    if value is None:
        return
    if not isinstance(value, str):
        errors.append(ValidationError(field, "must be a string or null"))
        return
    if value.startswith("$CODEX_HOME/") and field == "files.codex_generated_path":
        return

    path = Path(value)
    if path.is_absolute():
        errors.append(ValidationError(field, f"must be repository-relative {value!r}"))
        return

    root_path = root.resolve()
    candidate = (root_path / path).resolve()
    try:
        candidate.relative_to(root_path)
    except ValueError:
        errors.append(ValidationError(field, f"escapes repository root {value!r}"))
        return

    if not _resolved_path_exists(root, value):
        errors.append(ValidationError(field, f"points to missing path {value!r}"))


def validate_top_level_fields(
    data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate required top-level fields and their enum values.

    Parameters
    ----------
    data : dict[str, Any]
        Parsed manifest object.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    require_keys(data, REQUIRED_TOP_LEVEL, "manifest", errors)
    validate_enum(data.get("family"), ALLOWED_FAMILIES, "family", errors)
    validate_enum(data.get("status"), ALLOWED_STATUSES, "status", errors)
    validate_enum(data.get("bucket"), ALLOWED_BUCKETS, "bucket", errors)
    validate_enum(
        data.get("intent_class"), ALLOWED_INTENT_CLASSES, "intent_class", errors
    )


def validate_files(
    root: Path, data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate manifest file path fields.

    Parameters
    ----------
    root : Path
        Repository root used for path checks.
    data : dict[str, Any]
        Parsed manifest object.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    files = data.get("files")
    if require_mapping(files, "files", errors):
        require_keys(files, REQUIRED_FILES, "files", errors)
        for field in sorted(REQUIRED_FILES):
            validate_optional_path(root, files.get(field), f"files.{field}", errors)


def validate_required_section(
    data: dict[str, Any],
    field: str,
    required: set[str],
    errors: list[ValidationError],
) -> None:
    """Validate a required manifest object section by key set.

    Parameters
    ----------
    data : dict[str, Any]
        Parsed manifest object.
    field : str
        Top-level section name.
    required : set[str]
        Required keys for the section.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    section = data.get(field)
    if require_mapping(section, field, errors):
        require_keys(section, required, field, errors)


def validate_manifest_fields(
    root: Path, data: dict[str, Any], errors: list[ValidationError]
) -> None:
    """Validate a parsed manifest object.

    Parameters
    ----------
    root : Path
        Repository root used for path checks.
    data : dict[str, Any]
        Parsed manifest object.
    errors : list[ValidationError]
        Mutable error collection updated in place.

    Returns
    -------
    None
        Errors are appended to ``errors``.
    """
    validate_top_level_fields(data, errors)
    validate_required_section(data, "tool", REQUIRED_TOOL, errors)
    validate_required_section(data, "prompt", REQUIRED_PROMPT, errors)
    validate_files(root, data, errors)
    validate_required_section(data, "source_asset", REQUIRED_SOURCE_ASSET, errors)
    validate_required_section(
        data, "asset_contract", REQUIRED_ASSET_CONTRACT, errors
    )
    validate_required_section(data, "postprocess", REQUIRED_POSTPROCESS, errors)
    validate_required_section(data, "validation", REQUIRED_VALIDATION, errors)
    validate_required_section(data, "runtime_use", REQUIRED_RUNTIME_USE, errors)

    if not isinstance(data.get("notes"), list):
        errors.append(ValidationError("notes", "must be an array"))


def load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[ValidationError]]:
    """Read and parse one manifest file.

    Parameters
    ----------
    path : Path
        Manifest JSON file path to read.

    Returns
    -------
    tuple[dict[str, Any] | None, list[ValidationError]]
        Parsed manifest data and validation errors. Data is ``None`` when the
        file cannot be read, parsed, or represented as a JSON object.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        return None, [ValidationError("manifest", f"cannot read file: {error}")]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        return None, [ValidationError("manifest", f"invalid JSON: {error}")]

    if not isinstance(data, dict):
        return None, [ValidationError("manifest", "must be an object")]

    return data, []


def validate_manifest(root: Path, path: Path) -> list[ValidationError]:
    """Validate one manifest and return domain validation errors.

    Parameters
    ----------
    root : Path
        Repository root used for path checks.
    path : Path
        Manifest JSON file path to validate.

    Returns
    -------
    list[ValidationError]
        Domain validation errors. The list is empty when the manifest is valid.
    """
    data, errors = load_manifest(path)
    if errors:
        return errors
    if data is None:
        return [ValidationError("manifest", "must be an object")]

    if not require_mapping(data, "manifest", errors):
        return errors

    validate_manifest_fields(root, data, errors)
    return errors


def render_errors(
    rel_path: Path, errors: list[ValidationError], output: TextIO
) -> None:
    """Write rendered validation errors for one manifest.

    Parameters
    ----------
    rel_path : Path
        Manifest path relative to the repository root.
    errors : list[ValidationError]
        Errors to render.
    output : TextIO
        Text stream that receives human-readable errors.

    Returns
    -------
    None
        Output is written to ``output``.
    """
    for error in errors:
        if error.message.startswith(error.field):
            message = error.message
        else:
            message = f"{error.field} {error.message}"
        print(f"{rel_path}: {message}", file=output)


def render_failure_log(
    rel_path: Path, errors: list[ValidationError], output: TextIO
) -> None:
    """Write one structured validation failure record.

    Parameters
    ----------
    rel_path : Path
        Manifest path relative to the repository root.
    errors : list[ValidationError]
        Errors counted in the structured record.
    output : TextIO
        Text stream that receives the JSON record.

    Returns
    -------
    None
        Output is written to ``output``.
    """
    print(
        json.dumps(
            {
                "op": "manifest-validation",
                "path": str(rel_path),
                "error_count": len(errors),
            }
        ),
        file=output,
    )


def render_stdout_log(
    record: dict[str, object], output: TextIO = sys.stdout
) -> None:
    """Write one structured manifest validation progress record.

    Parameters
    ----------
    record : dict[str, object]
        JSON-serializable progress record.
    output : TextIO
        Text stream that receives the JSON record.

    Returns
    -------
    None
        Output is written to ``output``.
    """
    print(json.dumps(record), file=output)


def main(argv: list[str] | None = None, output: TextIO = sys.stderr) -> int:
    """Run manifest validation.

    Parameters
    ----------
    argv : list[str] | None
        Command-line argument strings, or ``None`` to read from ``sys.argv``.
    output : TextIO
        Text stream that receives validation failures and summary errors.

    Returns
    -------
    int
        Process-style exit code. Returns ``0`` when all manifests pass and ``1``
        when any manifest fails validation.

    Raises
    ------
    SystemExit
        Raised by ``argparse`` when arguments are invalid.
    """
    started_at = time.perf_counter()
    args = parse_args(argv)
    root = args.root.resolve()
    paths = manifest_paths(root)
    failures = 0
    render_stdout_log(
        {"op": "manifest-validation", "manifests_found": len(paths)},
        output=sys.stdout,
    )

    for path in paths:
        errors = validate_manifest(root, path)
        if errors:
            failures += 1
            rel_path = path.relative_to(root)
            render_failure_log(rel_path, errors, output)
            render_errors(rel_path, errors, output)

    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 3)
    render_stdout_log(
        {"op": "manifest-validation", "elapsed_ms": elapsed_ms},
        output=sys.stdout,
    )

    if failures:
        print(f"Manifest validation failed for {failures} file(s).", file=output)
        return 1

    print(f"Validated {len(paths)} manifest file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
