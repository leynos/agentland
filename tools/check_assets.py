#!/usr/bin/env python3
"""Run deterministic Agentland asset metadata checks."""

from __future__ import annotations

import check_manifests


def validate_assets_metadata(argv: list[str] | None = None) -> int:
    """Run asset-specific metadata validators.

    Parameters
    ----------
    argv : list[str] | None
        Command-line arguments passed to the asset validation entrypoint. The
        current placeholder validators do not inspect these arguments.

    Returns
    -------
    int
        Validation exit code. Returns ``0`` when no asset-specific metadata
        validation failures are present.
    """
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
