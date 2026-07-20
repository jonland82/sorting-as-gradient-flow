"""Small reporting helpers shared by the verification scripts.

The suite intentionally uses ordinary assertions instead of a large testing
framework.  A failed mathematical check raises immediately, gives a readable
description, and makes the process exit with a nonzero status.
"""

from __future__ import annotations

from collections.abc import Callable


def verify(description: str, condition: bool) -> None:
    """Record one human-readable check or fail with the same description."""

    if not condition:
        raise AssertionError(description)
    print(f"  [PASS] {description}")


def run_group(title: str, checks: list[tuple[str, Callable[[], bool]]]) -> int:
    """Run a related group of checks and return the number that passed."""

    print(f"\n{title}")
    for description, check in checks:
        verify(description, bool(check()))
    return len(checks)
