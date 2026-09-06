"""Prove scientific PASS/FAIL logic survives `python -O` (Sections 3 & 4).

`assert` statements are compiled away entirely under `python -O`. Every
report.py in this repository was migrated to raise `validation.ValidationError`
instead of using bare `assert` for scientific PASS/FAIL logic. These tests
demonstrate both the fix (ValidationError survives -O) and, for contrast,
the exact hazard it fixes (a bare `assert` does not).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run(code: str, optimized: bool) -> subprocess.CompletedProcess:
    args = [sys.executable]
    if optimized:
        args.append("-O")
    args += ["-c", code]
    return subprocess.run(args, capture_output=True, cwd=REPO_ROOT)


def test_validation_check_raises_under_normal_mode():
    code = "from validation import check; check('t', 1.0, 2.0, 0.01)"
    result = _run(code, optimized=False)
    assert result.returncode != 0
    assert b"ValidationError" in result.stderr


def test_validation_check_raises_under_optimized_mode():
    code = "from validation import check; check('t', 1.0, 2.0, 0.01)"
    result = _run(code, optimized=True)
    assert result.returncode != 0
    assert b"ValidationError" in result.stderr


def test_validation_check_passes_silently_when_within_tolerance():
    code = "from validation import check; check('t', 1.0, 1.0000000001, 1e-6)"
    result = _run(code, optimized=False)
    assert result.returncode == 0


def test_forced_validation_failure_exits_nonzero_under_optimized_mode():
    """Section 4: a forced validation failure must still exit nonzero under -O."""
    code = "from validation import check; check('forced-failure', 0.0, 1.0, 1e-9)"
    result = _run(code, optimized=True)
    assert result.returncode != 0


def test_bare_assert_is_the_hazard_this_migration_fixes():
    # Documents *why* the migration away from bare `assert` was necessary:
    # under -O, `assert` is compiled to a no-op and a real failure is
    # silently swallowed (exit 0) instead of raising.
    code = "assert 1.0 == 2.0, 'this must never pass'"
    normal = _run(code, optimized=False)
    optimized = _run(code, optimized=True)
    assert normal.returncode != 0
    assert optimized.returncode == 0


def test_zero_point_energy_report_identical_normal_and_optimized():
    normal = subprocess.run(
        [sys.executable, "-m", "zero_point_energy.report"], capture_output=True, cwd=REPO_ROOT
    )
    optimized = subprocess.run(
        [sys.executable, "-O", "-m", "zero_point_energy.report"], capture_output=True, cwd=REPO_ROOT
    )
    assert normal.returncode == 0
    assert optimized.returncode == 0
    assert normal.stdout == optimized.stdout


def test_d067_report_identical_normal_and_optimized():
    normal = subprocess.run(
        [sys.executable, "-m", "d067_art_v1.report"], capture_output=True, cwd=REPO_ROOT
    )
    optimized = subprocess.run(
        [sys.executable, "-O", "-m", "d067_art_v1.report"], capture_output=True, cwd=REPO_ROOT
    )
    assert normal.returncode == 0
    assert optimized.returncode == 0
    assert normal.stdout == optimized.stdout


def test_chronometrics_report_identical_normal_and_optimized():
    normal = subprocess.run(
        [sys.executable, "-m", "chronometrics.report"], capture_output=True, cwd=REPO_ROOT
    )
    optimized = subprocess.run(
        [sys.executable, "-O", "-m", "chronometrics.report"], capture_output=True, cwd=REPO_ROOT
    )
    assert normal.returncode == 0
    assert optimized.returncode == 0
    assert normal.stdout == optimized.stdout
