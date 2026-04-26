#!/usr/bin/env python3
"""Validate Agentland asset manifest structure.

This module enforces the canonical manifest schema defined in
``docs/asset-spec.md`` and ``assets/manifests/README.md``. It recursively
validates all JSON files under ``assets/manifests/``, checking required
fields, enum values, nested object structures, and optional path existence.
Validation functions return ``ValidationError`` values so domain validation stays
separate from command-line rendering.

Implementation is split across ``manifest_schema``, ``manifest_validators``,
and ``manifest_cli``. This module remains the public compatibility surface for
scripts and tests that import ``check_manifests`` directly.

Usage
-----
Run directly or via the Makefile target::

    python tools/check_manifests.py --root /path/to/repo
    make manifest-check

Exit code is non-zero if any manifest fails validation.
"""

from __future__ import annotations

from manifest_cli import (
    main,
    manifest_paths,
    parse_args,
    render_errors,
    render_failure_log,
    render_stdout_log,
)
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
from manifest_validators import (
    ValidationError,
    load_manifest,
    require_keys,
    require_mapping,
    validate_enum,
    validate_files,
    validate_manifest,
    validate_manifest_fields,
    validate_optional_path,
    validate_required_section,
    validate_top_level_fields,
)

__all__ = [
    "ALLOWED_BUCKETS",
    "ALLOWED_FAMILIES",
    "ALLOWED_INTENT_CLASSES",
    "ALLOWED_STATUSES",
    "REQUIRED_ASSET_CONTRACT",
    "REQUIRED_FILES",
    "REQUIRED_POSTPROCESS",
    "REQUIRED_PROMPT",
    "REQUIRED_RUNTIME_USE",
    "REQUIRED_SOURCE_ASSET",
    "REQUIRED_TOOL",
    "REQUIRED_TOP_LEVEL",
    "REQUIRED_VALIDATION",
    "ValidationError",
    "load_manifest",
    "main",
    "manifest_paths",
    "parse_args",
    "render_errors",
    "render_failure_log",
    "render_stdout_log",
    "require_keys",
    "require_mapping",
    "validate_enum",
    "validate_files",
    "validate_manifest",
    "validate_manifest_fields",
    "validate_optional_path",
    "validate_required_section",
    "validate_top_level_fields",
]


if __name__ == "__main__":
    raise SystemExit(main())
