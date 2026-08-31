"""Mode counting and zero-point energy density (source: D1-D4, D8-D9, D14-D15).

Sign convention throughout: bosons contribute +g, fermions -g (anticommutators
flip the sign; D2/D33/S8). g is the number of physical polarizations:
scalar g=1, photon g=2 (D31, two transverse polarizations only), Dirac
fermion g=4 (D33, spin x particle/antiparticle), massive spin-1 (Proca)
g=3 (D32).
"""
from __future__ import annotations

import math

from .constants import HBAR, C_LIGHT


def density_of_states(omega: float, g: float = 1.0) -> float:
    """dN/(V dω) for a massless field (D1). Units: s m^-3."""
    return g * omega**2 / (2 * math.pi**2 * C_LIGHT**3)


def spectral_energy_density(omega: float, g: float = 1.0) -> float:
    """dρ/dω = g ħ ω^3 / (4π^2 c^3) (D4/S3). Units: J s m^-3."""
    return g * HBAR * omega**3 / (4 * math.pi**2 * C_LIGHT**3)


def zpe_density_massless(omega_c: float, g: float = 1.0) -> float:
    """Hard-cutoff ZPE density of a massless field (D2/S1).

    rho = g hbar omega_c^4 / (16 pi^2 c^3). Bosons: g > 0. Fermions: pass
    a negative g (e.g. g=-4 for one Dirac species, D33). Units: J/m^3.
    """
    return g * HBAR * omega_c**4 / (16 * math.pi**2 * C_LIGHT**3)


def zpe_density_massless_from_k(k_c: float, g: float = 1.0) -> float:
    """Route B of D2, momentum-cutoff form: rho = g hbar c k_c^4/(16 pi^2)."""
    return g * HBAR * C_LIGHT * k_c**4 / (16 * math.pi**2)


def zpe_density_massless_from_energy(e_c: float, g: float = 1.0) -> float:
    """Route C (D14): rho = g/(16 pi^2) * E_c^4/(hbar c)^3."""
    return g / (16 * math.pi**2) * e_c**4 / (HBAR * C_LIGHT) ** 3


def photon_zpe_density(omega_c: float) -> float:
    """Photon ZPE: only 2 transverse polarizations contribute (D31)."""
    return zpe_density_massless(omega_c, g=2.0)


def dirac_zpe_density_leading(e_c: float, g: float = 4.0) -> float:
    """Dirac fermion leading term, sign flipped, g=4 (D33).

    Exact only in the massless limit; corrections are O(m^2 E_c^2, m^4 ln E_c).
    """
    return -g / (16 * math.pi**2) * e_c**4 / (HBAR * C_LIGHT) ** 3


def _massive_cutoff_integral(k_c: float, a_m: float) -> float:
    """int_0^{k_c} k^2 sqrt(k^2+a_m^2) dk, closed form used in D3/D4."""
    K, am = k_c, a_m
    return (K * math.sqrt(K**2 + am**2) * (2 * K**2 + am**2) - am**4 * math.asinh(K / am)) / 8.0


def zpe_density_massive_exact(k_c: float, mass: float, g: float = 1.0) -> float:
    """Exact hard-cutoff ZPE density of a massive field (D3), no series truncation.

    rho = g hbar c / (4 pi^2) * int_0^{k_c} k^2 sqrt(k^2 + a_m^2) dk,
    a_m = m c / hbar. Valid for any k_c/a_m ratio (the closed form is exact;
    only the large-k_c *expansion* below is an asymptotic series).
    """
    a_m = mass * C_LIGHT / HBAR
    return g * HBAR * C_LIGHT / (4 * math.pi**2) * _massive_cutoff_integral(k_c, a_m)


def zpe_density_massive_asymptotic(k_c: float, mass: float, g: float = 1.0) -> float:
    """Large-k_c asymptotic expansion of D3 (D4/D32), through the log term.

    rho = g hbar c k_c^4/(16 pi^2)
        + g m^2 c^3 k_c^2/(16 pi^2 hbar)
        - g m^4 c^5/(32 pi^2 hbar^3) * ln(2 hbar k_c / (m c))
        + g m^4 c^5/(128 pi^2 hbar^3)
        + O(g hbar c a_m^6 / k_c^2).

    The remainder is dimensionally O(hbar c a_m^6/k_c^2); integrating this
    series through k_c=0 (a_m/k_c -> infinity) is invalid (D3 note). Use
    zpe_density_massive_exact for that regime.
    """
    hbar, c = HBAR, C_LIGHT
    m4c5 = mass**4 * c**5
    term1 = g * hbar * c * k_c**4 / (16 * math.pi**2)
    term2 = g * mass**2 * c**3 * k_c**2 / (16 * math.pi**2 * hbar)
    term3 = -g * m4c5 / (32 * math.pi**2 * hbar**3) * math.log(2 * hbar * k_c / (mass * c))
    term4 = g * m4c5 / (128 * math.pi**2 * hbar**3)
    return term1 + term2 + term3 + term4


def proca_zpe_density_exact(k_c: float, mass: float) -> float:
    """Massive spin-1 (Proca) field, g=3: exactly 3x the scalar result (D32)."""
    return zpe_density_massive_exact(k_c, mass, g=3.0)
