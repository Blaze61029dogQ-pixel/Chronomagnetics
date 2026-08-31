"""Vacuum stress-energy tensor and equation of state (source: D6, D10, S4).

From S_vac = -int d^4x sqrt(-g) rho with rho constant, varying the action
gives T^mu_nu = rho * g^mu_nu identically (Lorentz invariance forces this
perfect-fluid form with p = -rho, w = p/rho = -1) -- independent of whether
one arrives at it by direct variation or by the perfect-fluid argument
(D6/D10, two independently-agreeing routes).
"""
from __future__ import annotations


def vacuum_pressure(rho_vac: float) -> float:
    """p_vac = -rho_vac (D6/D10/S4)."""
    return -rho_vac


def equation_of_state_w(rho_vac: float) -> float:
    """w = p/rho = -1 for the vacuum term, independent of rho_vac's value."""
    return -1.0


def stress_tensor_flat(rho_vac: float):
    """Flat-space diag(T^mu_nu) with signature (+---): (rho, -rho, -rho, -rho) (D10)."""
    return (rho_vac, -rho_vac, -rho_vac, -rho_vac)


def cosmological_constant(rho_vac: float, big_g: float, c_light: float) -> float:
    """Lambda = 8 pi G rho_ZPE / c^4, once the Einstein-equation sign convention is fixed (S1.6)."""
    import math

    return 8 * math.pi * big_g * rho_vac / c_light**4
