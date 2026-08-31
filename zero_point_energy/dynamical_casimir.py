"""Dynamical Casimir effect: driven-boundary photon pair production (D7, D57, D62).

The dynamical Casimir effect is *not* extraction from a stationary vacuum:
in periodic steady state the boundary drive supplies all radiated energy
(D57 energy-balance note, D34 vacuum passivity).
"""
from __future__ import annotations


def interaction_hamiltonian_coefficient(omega0: float, omega_dot: float) -> float:
    """Coefficient of (a^2 + a_dagger^2) in H_int = hbar*omega_dot/(4*omega) * (...) (D7/D62).

    Returns hbar_omega_dot_over_4omega; caller multiplies by hbar externally
    if a bare rate is wanted, since this module keeps hbar explicit at the
    call site (see modes.py convention). Units: s^-1 (rate), given
    omega_dot in s^-2 and omega0 in s^-1.
    """
    return omega_dot / (4 * omega0)


def pair_production_rate(epsilon: float, omega0: float, quality_factor: float) -> float:
    """Resonant, weak-pump pair rate Gamma_pair ~= epsilon^2 * omega0 / (4 Q) (D7/D62).

    omega(t) = omega0 * [1 + epsilon * cos(2*omega0*t)], epsilon dimensionless
    modulation amplitude (not the elementary charge -- D62 note). Units: s^-1.
    """
    return epsilon**2 * omega0 / (4 * quality_factor)
