#!/usr/bin/env python3
"""Run deterministic Agentland asset metadata checks."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import check_manifests


@dataclass(frozen=True)
class AssetValidationError:
    """An asset metadata validation failure for one logical field."""

    field: str
    message: str


def _asset_errors_for_manifest(data: dict[str, Any]) -> list[AssetValidationError]:
    """Return asset metadata consistency errors for one parsed manifest."""
    errors: list[AssetValidationError] = []
    status = data.get("status")
    intent_class = data.get("intent_class")
    bucket = data.get("bucket")
    files = data.get("files", {})
    runtime_use = data.get("runtime_use", {})

    if not isinstance(files, dict) or not isinstance(runtime_use, dict):
        return errors

    runtime_kind = runtime_use.get("kind")
    has_runtime_file = bool(
        files.get("processed_path")
        or files.get("atlas_image_path")
        or files.get("atlas_metadata_path")
    )
    is_runtime = status == "approved-runtime" or intent_class == "runtime-processed"

    if is_runtime and not has_runtime_file:
        errors.append(
            AssetValidationError(
                "files",
                "runtime assets require processed_path, atlas_image_path, or "
                "atlas_metadata_path",
            )
        )

    if bucket == "direct-generated-reference" and runtime_kind != "reference only":
        errors.append(
            AssetValidationError(
                "runtime_use.kind",
                "direct-generated-reference assets must remain reference only",
            )
        )

    return errors


def _render_asset_errors(
    root: Path, path: Path, errors: list[AssetValidationError]
) -> None:
    """Write machine-parseable and human-readable asset validation errors."""
    rel_path = path.relative_to(root)
    print(
        json.dumps(
            {
                "op": "asset-validation",
                "path": str(rel_path),
                "error_count": len(errors),
            }
        ),
        file=sys.stderr,
    )
    for error in errors:
        print(f"{rel_path}: {error.field} {error.message}", file=sys.stderr)


def validate_assets_metadata(argv: list[str] | None = None) -> int:
    """Run asset-specific metadata validators.

    Parameters
    ----------
    argv : list[str] | None
        Command-line arguments passed to the asset validation entrypoint,
        including the optional repository ``--root``.

    Returns
    -------
    int
        Validation exit code. Returns ``0`` when no asset-specific metadata
        validation failures are present.
    """
    args = check_manifests.parse_args(argv)
    root = args.root.resolve()
    failures = 0

    for path in check_manifests.manifest_paths(root):
        data, load_errors = check_manifests.load_manifest(path)
        if load_errors:
            failures += 1
            rel_path = path.relative_to(root)
            print(
                json.dumps(
                    {
                        "op": "asset-validation",
                        "path": str(rel_path),
                        "error_count": len(load_errors),
                    }
                ),
                file=sys.stderr,
            )
            check_manifests.render_errors(rel_path, load_errors, sys.stderr)
            continue
        if data is None:
            continue

        errors = _asset_errors_for_manifest(data)
        if errors:
            failures += 1
            _render_asset_errors(root, path, errors)

    if failures:
        print(
            f"Asset metadata validation failed for {failures} file(s).",
            file=sys.stderr,
        )
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run manifest and asset metadata validation.

    Parameters
    ----------
    argv : list[str] | None
        Command-line argument strings, or ``None`` to let the manifest checker
        read from ``sys.argv``.

    Returns
    -------
    int
        Combined process-style exit code. Returns ``0`` when manifest and asset
        metadata validation pass; returns non-zero when either validation stage
        fails.
    """
    manifest_status = check_manifests.main(argv)
    asset_status = validate_assets_metadata(argv)
    return manifest_status | asset_status


if __name__ == "__main__":
    raise SystemExit(main())
