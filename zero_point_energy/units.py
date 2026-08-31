"""Natural-unit <-> SI conversion for vacuum energy densities (source: D13/S6).

Post-2019 SI defining constants (e, h, c) make 1 GeV^4 -> J/m^3 exact once
GeV is fixed by e; downstream physical quantities built from a measured
input (e.g. G) are not exact even if this conversion is (C9 note).
"""
from __future__ import annotations

from .constants import GEV_TO_JOULE, HBAR_C

#: 1 GeV^4 in J/m^3 (D13/S6): GEV_TO_JOULE**4 / (hbar*c)**3.
GEV4_TO_JOULE_PER_M3 = GEV_TO_JOULE**4 / HBAR_C**3


def gev4_to_si(rho_gev4: float) -> float:
    """Convert an energy density from GeV^4 (natural units, hbar=c=1) to J/m^3."""
    return rho_gev4 * GEV4_TO_JOULE_PER_M3


def si_to_gev4(rho_si: float) -> float:
    """Convert an energy density from J/m^3 to GeV^4 (natural units)."""
    return rho_si / GEV4_TO_JOULE_PER_M3
