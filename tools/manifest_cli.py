"""Command-line and output helpers for Agentland manifest validation."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import TextIO

from manifest_validators import ValidationError, validate_manifest


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
