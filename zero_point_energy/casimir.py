"""Casimir energies and pressures (source: D5, D12, D18, D20, D25, D26, D40, S5).

All forms here are the finite, geometry-dependent *differences* left after
quartic/cubic/quadratic mode-counting divergences cancel between two
configurations (D27) -- not the bare vacuum level, which is regulator
dependent (D8-D9, D24).
"""
from __future__ import annotations

import math

from .constants import HBAR, C_LIGHT

PI2 = math.pi**2


def plate_energy_per_area(a: float) -> float:
    """Ideal-conductor parallel plates, T=0 (D5/S5): E/A = -pi^2 hbar c/(720 a^3). J/m^2."""
    return -PI2 * HBAR * C_LIGHT / (720 * a**3)


def plate_pressure(a: float) -> float:
    """Casimir pressure between ideal plates (D5/D16/S5): P = -pi^2 hbar c/(240 a^4). Pa.

    Attractive (negative). P(100 nm) ~= -13.0013 Pa (D16); see report.py.
    """
    return -PI2 * HBAR * C_LIGHT / (240 * a**4)


def plasma_model_pressure_ratio(a: float, delta0: float, order2: bool = True) -> float:
    """Finite-conductivity correction for identical plasma-model plates (D18).

    P/P0 = 1 - (16/3)(delta0/a) + 24 (delta0/a)^2 + O((delta0/a)^3), valid
    for delta0/a << 1. The coefficient 24 is specific to this nondissipative,
    T=0 plasma model -- it is not universal for Drude metals or dispersive
    media in general (D18 note).
    """
    x = delta0 / a
    ratio = 1 - (16.0 / 3.0) * x
    if order2:
        ratio += 24.0 * x**2
    return ratio


def sphere_plate_force_pfa(radius: float, a: float) -> float:
    """Sphere-plate force, proximity force approximation (D20): F ~= 2 pi R (E/A).

    F_PFA(a) = -pi^3 hbar c R/(360 a^3), valid for R >> a. Newtons.
    """
    return -math.pi**3 * HBAR * C_LIGHT * radius / (360 * a**3)


def geometry_scaling_energy(length: float, c_geom: float) -> float:
    """Dimensional scaling for a single-length-scale cavity (D12): E = -C hbar c / L."""
    return -c_geom * HBAR * C_LIGHT / length


def geometry_scaling_energy_density(length: float, c_geom_prime: float) -> float:
    """E/V = -C' hbar c / L^4 (D12). Parallel plates: C' = pi^2/720."""
    return -c_geom_prime * HBAR * C_LIGHT / length**4


def scalar_interval_energy(a: float) -> float:
    """Dirichlet scalar on [0,a] (D26): E0 = -pi hbar c/(24 a). Joules.

    Derived via zeta(-1) = -1/12 regularization of sum_n n*(pi/a); this is
    the analytically-continued value, not a convergent series sum (D23 note).
    """
    return -math.pi * HBAR * C_LIGHT / (24 * a)


def scalar_ring_energy(length: float) -> float:
    """Periodic scalar on a circle of length L (D25): E0 = -pi hbar c/(6 L). Joules."""
    return -math.pi * HBAR * C_LIGHT / (6 * length)


def boyer_sphere_energy(radius: float) -> float:
    """Boyer's perfectly-conducting thin spherical shell (D40): positive self-energy.

    E = +0.09235 hbar c/(2R) = +0.046175 hbar c/R. The stress is outward
    (opposite sign to the plate result); dropping the 1/2 doubles the energy.
    """
    return 0.09235 * HBAR * C_LIGHT / (2 * radius)


def high_temperature_pressure_ideal(a: float, temperature: float, k_boltzmann: float) -> float:
    """Classical high-T limit, ideal conductor / nondissipative plasma, TE0 retained (D28).

    P -> -zeta(3)/(4 pi) * kB T / a^3.
    """
    zeta3 = 1.2020569031595943
    return -zeta3 / (4 * math.pi) * k_boltzmann * temperature / a**3


def high_temperature_pressure_drude(a: float, temperature: float, k_boltzmann: float) -> float:
    """Classical high-T limit, Drude metal, TE zero-mode absent (D28).

    P -> -zeta(3)/(8 pi) * kB T / a^3 -- half the ideal-conductor value.
    """
    return 0.5 * high_temperature_pressure_ideal(a, temperature, k_boltzmann)


def stress_tensor_diagonal(a: float):
    """Renormalized <T^mu_nu> between ideal plates, signature (+---) (D29).

    Returns (T00, Txx, Tyy, Tzz) = pi^2 hbar c/(720 a^4) * (-1, 1, 1, -3).
    T_zz = P = -pi^2 hbar c/(240 a^4) recovers plate_pressure. Replacing the
    final entry by -1 (instead of -3) gives the wrong pressure (C1/D29 note).
    """
    coeff = PI2 * HBAR * C_LIGHT / (720 * a**4)
    return (-coeff, coeff, coeff, -3 * coeff)
