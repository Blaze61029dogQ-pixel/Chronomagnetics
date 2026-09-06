"""Shared scientific-validation primitives.

Every ``report.py`` self-check script in this repository (zero_point_energy,
d067_art_v1, chronometrics) uses :class:`ValidationError` and :func:`check`
from this module instead of a bare ``assert`` statement. Python strips
``assert`` statements when run under ``python -O`` (optimized mode), which
would silently disable scientific PASS/FAIL logic; raising ``ValidationError``
is unaffected by ``-O`` and always propagates a nonzero exit code.
"""
from __future__ import annotations

import math


class ValidationError(RuntimeError):
    """A computed scientific result failed to match its reference value."""


def check(
    label: str,
    computed,
    reference,
    tolerance,
    *,
    mode: str = "rel",
    hard: bool = True,
) -> bool:
    """Compare ``computed`` against ``reference`` and print a PASS/FAIL line.

    mode="rel": ``tolerance`` is a relative tolerance, compared with
    ``math.isclose`` on ``float(computed)``/``float(reference)``.

    mode="abs": ``tolerance`` is an absolute tolerance on
    ``abs(computed - reference)``; both operands may be ``mpmath.mpf`` (or
    any type supporting subtraction and ``abs``), so callers doing
    high-precision chronometrics checks can pass ``mpmath.mpf`` values
    directly without a lossy ``float()`` cast.

    If ``hard`` is True and the check fails, raises :class:`ValidationError`
    with the computed value, reference value, and tolerance embedded in the
    message. If ``hard`` is False, a failure is printed as a WARN and does
    not raise -- use this only for checks that are documented as informative
    (e.g. an independent numeric solve landing within a few percent of an
    audited value, not an EXACT/FROZEN identity).
    """
    if mode == "rel":
        ok = math.isclose(float(computed), float(reference), rel_tol=tolerance)
        diff = abs(float(computed) - float(reference))
    elif mode == "abs":
        diff = abs(computed - reference)
        ok = diff <= tolerance
    else:
        raise ValueError(f"unknown check mode: {mode!r}")

    status = "OK  " if ok else ("FAIL" if hard else "WARN")
    print(f"[{status}] {label}: computed={computed!r} reference={reference!r} "
          f"|diff|={diff!r} tolerance={tolerance!r} (mode={mode})")

    if hard and not ok:
        raise ValidationError(
            f"{label}: computed={computed!r}, reference={reference!r}, "
            f"|diff|={diff!r}, tolerance={tolerance!r} (mode={mode})"
        )
    return ok
