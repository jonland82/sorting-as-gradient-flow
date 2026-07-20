"""Run every proof-verification script in an isolated Python process."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SUITE_DIRECTORY = Path(__file__).resolve().parent
SCRIPTS = (
    "verify_symbolic.py",
    "verify_combinatorial.py",
    "verify_numerical_geometry.py",
)


def main() -> int:
    print("Sorting as Gradient Flow — proof verification suite")
    print(f"Python: {sys.version.split()[0]}")

    for script_name in SCRIPTS:
        script_path = SUITE_DIRECTORY / script_name
        print(f"\n{'=' * 72}\nRunning {script_name}\n{'=' * 72}", flush=True)
        # check=True makes the full suite stop and return a nonzero status as
        # soon as one mathematical assertion or dependency import fails.
        subprocess.run([sys.executable, str(script_path)], check=True)

    print(f"\n{'=' * 72}")
    print(f"All {len(SCRIPTS)} verification scripts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
