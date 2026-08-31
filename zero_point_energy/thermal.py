"""Unruh/Hawking temperature, black-hole evaporation, and the Schwinger effect
(source: D37, D71-D74, D75).

Convention: acceleration a and Rindler-normalized surface gravity kappa
carry units of m/s^2 throughout (D70/D74) -- not frequency, and not
acceleration/c. exp(2*pi*omega*c/a) in D37 is dimensionless because
omega*c/a is dimensionless; do not insert an extra hbar there (C-item /
D37 note).
"""
from __future__ import annotations

import math

from .constants import C_LIGHT, G_NEWTON, HBAR, K_BOLTZMANN


def unruh_temperature(acceleration: float) -> float:
    """T_U = hbar*a / (2 pi c kB) for proper acceleration a [m/s^2] (D37/D74). Kelvin."""
    return HBAR * acceleration / (2 * math.pi * C_LIGHT * K_BOLTZMANN)


def rindler_thermal_occupation(omega: float, acceleration: float) -> float:
    """|beta_omega|^2 = 1/(exp(2 pi omega c / a) - 1) (D37). Dimensionless."""
    return 1.0 / (math.expm1(2 * math.pi * omega * C_LIGHT / acceleration))


def schwarzschild_surface_gravity(mass: float) -> float:
    """kappa = c^4/(4 G M), acceleration units (D71)."""
    return C_LIGHT**4 / (4 * G_NEWTON * mass)


def hawking_temperature(mass: float) -> float:
    """T_H = hbar c^3 / (8 pi G M kB) for a Schwarzschild black hole (D71). Kelvin."""
    return HBAR * C_LIGHT**3 / (8 * math.pi * G_NEWTON * mass * K_BOLTZMANN)


def hawking_power_benchmark(mass: float) -> float:
    """Ideal-blackbody benchmark power P_bb = hbar c^6/(15360 pi G^2 M^2) (D71).

    Uses Stefan-Boltzmann with the horizon area and two bosonic
    polarizations; it is not the exact graybody power of any single species
    (D71 note) -- actual Hawking luminosity depends on spin content, mass
    thresholds, and transmission (greybody) coefficients.
    """
    return HBAR * C_LIGHT**6 / (15360 * math.pi * G_NEWTON**2 * mass**2)


def evaporation_time_benchmark(mass: float) -> float:
    """t_evap ~= 5120 pi G^2 M^3 / (hbar c^4), integral of the benchmark power (D72). Seconds."""
    return 5120 * math.pi * G_NEWTON**2 * mass**3 / (HBAR * C_LIGHT**4)


def chiral_cft_thermal_flux(temperature: float, c_cft: float = 1.0) -> float:
    """<T_uu> = pi*c_CFT/(12 hbar) * (kB T)^2 for a 1+1D chiral CFT (D73).

    Units: J/s (power per one-dimensional channel) -- not a flux density;
    promoting this to J m^-2 s^-1 in 4D requires transverse mode density and
    graybody transmission factors (D73 note).
    """
    return math.pi * c_cft / (12 * HBAR) * (K_BOLTZMANN * temperature) ** 2


def schwinger_pair_rate_leading(field: float, mass: float, charge: float) -> float:
    """Leading (n=1) term of the Schwinger pair-production rate density (D75).

    w ~= (e E)^2/(4 pi^3 hbar^2 c) * exp(-pi m^2 c^3/(hbar e E)). This is
    nonperturbative vacuum decay in an external field, not a stationary ZPE
    contribution (D75 note); the full series sums 1/n^2 * exp(-n * ...).
    Units: s^-1 m^-3 (pair-production rate density).
    """
    prefactor = (charge * field) ** 2 / (4 * math.pi**3 * HBAR**2 * C_LIGHT)
    exponent = -math.pi * mass**2 * C_LIGHT**3 / (HBAR * charge * field)
    return prefactor * math.exp(exponent)


def schwinger_critical_field(mass: float, charge: float) -> float:
    """Critical Schwinger field E_S = m^2 c^3 / (e hbar) (D75). V/m."""
    return mass**2 * C_LIGHT**3 / (charge * HBAR)
