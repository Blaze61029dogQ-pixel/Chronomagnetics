"""Atom-surface Casimir-Polder interaction, SI units (source: D56).

Static polarizability alpha(0) has SI units C^2 m^2/J. Both potential and
force are negative in the retarded regime: the interaction is attractive
(D56 note -- do not mistake the sign for a repulsive result).
"""
from __future__ import annotations

import math

from .constants import EPS0, HBAR, C_LIGHT


def retarded_potential(z: float, alpha0: float) -> float:
    """U(z) = -3 hbar c alpha(0) / (32 pi^2 eps0 z^4), perfect conductor, retarded. Joules."""
    return -3 * HBAR * C_LIGHT * alpha0 / (32 * math.pi**2 * EPS0 * z**4)


def retarded_force(z: float, alpha0: float) -> float:
    """F_z = -3 hbar c alpha(0) / (8 pi^2 eps0 z^5), retarded regime. Newtons (attractive)."""
    return -3 * HBAR * C_LIGHT * alpha0 / (8 * math.pi**2 * EPS0 * z**5)
