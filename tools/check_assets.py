#!/usr/bin/env python3
"""Run deterministic Agentland asset metadata checks."""

from __future__ import annotations

import check_manifests


def main(argv: list[str] | None = None) -> int:
    """Run the combined asset validation entrypoint."""
    return check_manifests.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
