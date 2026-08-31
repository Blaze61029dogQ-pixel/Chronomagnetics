"""Zero-point amplitudes of quantum electrical resonators (source: D59, D61).

These are ground-state root-mean-square amplitudes of an LC oscillator or a
Josephson junction's quadratic (harmonic) approximation -- not measured
voltages, but well-defined zero-point fluctuation scales.
"""
from __future__ import annotations

import math

from .constants import HBAR


def lc_zero_point(omega0: float, capacitance: float, inductance: float):
    """LC resonator zero-point V, I, Phi, Q (D59).

    H = Q^2/(2C) + Phi^2/(2L), omega0 = 1/sqrt(LC), Z = sqrt(L/C).
    Returns (V_zpf [V], I_zpf [A], Phi_zpf [Wb], Q_zpf [C]), satisfying
    V_zpf = Q_zpf/C = omega0*Phi_zpf and I_zpf = Phi_zpf/L = omega0*Q_zpf.
    """
    impedance = math.sqrt(inductance / capacitance)
    v_zpf = math.sqrt(HBAR * omega0 / (2 * capacitance))
    i_zpf = math.sqrt(HBAR * omega0 / (2 * inductance))
    phi_zpf = math.sqrt(HBAR * impedance / 2)
    q_zpf = math.sqrt(HBAR / (2 * impedance))
    return v_zpf, i_zpf, phi_zpf, q_zpf


def josephson_plasma_frequency(e_j: float, e_c: float) -> float:
    """Josephson plasma frequency omega_p = sqrt(8 E_J E_C)/hbar (D61)."""
    return math.sqrt(8 * e_j * e_c) / HBAR


def josephson_zero_point(e_j: float, e_c: float):
    """Josephson-junction zero-point phase and Cooper-pair-number fluctuations (D61).

    Quadratic Hamiltonian (1/2)(8 E_C n^2 + E_J phi^2) gives
    phi_zpf = (2 E_C/E_J)^(1/4), n_zpf = (E_J/(32 E_C))^(1/4). Dimensionless.
    """
    phi_zpf = (2 * e_c / e_j) ** 0.25
    n_zpf = (e_j / (32 * e_c)) ** 0.25
    return phi_zpf, n_zpf
