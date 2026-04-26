"""Domain validation logic for Agentland asset manifests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from manifest_schema import (
    ALLOWED_BUCKETS,
    ALLOWED_FAMILIES,
    ALLOWED_INTENT_CLASSES,
    ALLOWED_STATUSES,
    REQUIRED_ASSET_CONTRACT,
    REQUIRED_FILES,
    REQUIRED_POSTPROCESS,
    REQUIRED_PROMPT,
    REQUIRED_RUNTIME_USE,
    REQUIRED_SOURCE_ASSET,
    REQUIRED_TOOL,
    REQUIRED_TOP_LEVEL,
    REQUIRED_VALIDATION,
)


@dataclass(frozen=True)
class ValidationError:
    """A manifest validation failure for one logical field."""

    field: str
    message: str


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
