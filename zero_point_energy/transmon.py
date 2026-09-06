"""Cooper-pair-box / transmon qubit: exact charge-basis diagonalization and
the large-E_J/E_C asymptotic approximation (source: Koch et al., Phys. Rev.
A 76, 042319 (2007); see REFERENCES.bib).

MODEL

    H = 4*E_C*(n - n_g)^2 - E_J*cos(phi)

n is the Cooper-pair number operator (integer eigenvalues), phi the
superconducting phase, n_g the dimensionless gate charge, E_C the charging
energy, E_J the Josephson energy (all in the same energy units, e.g. h*GHz
or Joules -- this module is unit-agnostic as long as E_C and E_J share
units). In the charge basis {|n>: n in Z}, truncated to
n in {-n_max, ..., n_max}, cos(phi) = (1/2)(|n><n+1| + |n+1><n|) summed over
n (raising/lowering the charge by one Cooper pair), so H is exactly
tridiagonal:

    <n|H|n>   = 4*E_C*(n - n_g)^2
    <n|H|n+1> = <n+1|H|n> = -E_J/2

Diagonalized here directly (numpy.linalg.eigh on the real symmetric
tridiagonal-as-dense matrix) -- no approximation beyond the finite charge
truncation, whose convergence is checked in
`energies_vs_truncation`/tests/test_transmon.py.

LARGE-E_J/E_C (TRANSMON) ASYMPTOTIC APPROXIMATION

`asymptotic_energies` is a genuinely different computation, provided only
as a COMPARISON, not as the solver: expanding cos(phi) = 1 - phi^2/2 +
phi^4/24 - ... turns H into a harmonic oscillator, H0 = -E_J + hbar*omega_p*
(a-dagger a + 1/2) with hbar*omega_p = sqrt(8*E_J*E_C) (the same plasma
frequency already used in zero_point_energy.resonators.josephson_plasma_frequency),
plus a quartic perturbation -(E_J/24)*phi^4. Using the harmonic-oscillator
zero-point phase amplitude phi_zpf = (2*E_C/E_J)^(1/4) (also already in
resonators.josephson_zero_point) and the standard number-state matrix
element <m|(a+a-dagger)^4|m> = 6*m^2 + 6*m + 3, first-order perturbation
theory gives

    E_m ~= -E_J + sqrt(8*E_J*E_C)*(m + 1/2) - (E_C/12)*(6*m^2 + 6*m + 3)

This is the standard transmon-regime result developed by Koch et al.
(2007) for E_J/E_C >> 1; the specific derivation via the quartic
cos(phi) expansion and number-state matrix element above is reproduced
here as original code following that cited treatment (not a verbatim
transcription of a specific numbered equation from the paper, which this
implementation does not claim to cite precisely). It correctly predicts
the transmon's defining feature, anharmonicity -> -E_C as E_J/E_C -> inf
(from this formula: (E_2-E_1)-(E_1-E_0) = -E_C exactly, independent of
E_J/E_C, at this order) -- checked against the exact diagonalization in
tests/test_transmon.py.

SCOPE: the asymptotic formula is a leading-order (E_C/E_J)-expansion and
degrades as E_J/E_C approaches order unity (the Cooper-pair-box regime,
where charge dispersion is no longer negligible and the harmonic
approximation to cos(phi) breaks down); it is not claimed accurate there.
Empirically (tests/test_transmon.py), the anharmonicity's approach to its
asymptotic -E_C value is slow -- the relative error tracks roughly
E_C/sqrt(E_J*E_C) ~ 1/sqrt(E_J/E_C), not an exponentially fast approach --
so even at E_J/E_C = 1000 the exact anharmonicity still differs from -E_C
by a few percent; this is reported as an observed numerical fact, not a
claimed convergence rate derived from the perturbation series itself.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

import numpy as np


def _check_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite positive number, got {value!r}")
    return value


@dataclass
class TransmonSpectrum:
    """Diagonalization result: lowest eigenenergies (and, optionally,
    eigenvectors) of the truncated charge-basis Hamiltonian."""

    eigenvalues: np.ndarray  # ascending, length num_levels
    transition_frequencies: np.ndarray  # E_{m+1} - E_m, length num_levels-1
    anharmonicity: float  # (E_2-E_1) - (E_1-E_0); requires num_levels >= 3
    e_c: float
    e_j: float
    n_g: float
    n_max: int
    eigenvectors: Optional[np.ndarray] = field(default=None, repr=False)
    charge_basis: Optional[np.ndarray] = field(default=None, repr=False)


def hamiltonian_matrix(e_c: float, e_j: float, n_g: float = 0.0, n_max: int = 15) -> np.ndarray:
    """The (2*n_max+1) x (2*n_max+1) charge-basis Hamiltonian matrix.

    e_c, e_j must be > 0 (same energy units); n_g is dimensionless and may
    be any finite real number (physics is periodic in n_g with period 1,
    but this function does not restrict the input range); n_max >= 1.
    """
    e_c = _check_positive("e_c", e_c)
    e_j = _check_positive("e_j", e_j)
    if not math.isfinite(n_g):
        raise ValueError(f"n_g must be finite, got {n_g!r}")
    if not isinstance(n_max, (int, np.integer)) or n_max < 1:
        raise ValueError(f"n_max must be an integer >= 1, got {n_max!r}")

    charge = np.arange(-n_max, n_max + 1, dtype=float)
    dim = charge.size
    h = np.zeros((dim, dim), dtype=float)
    np.fill_diagonal(h, 4.0 * e_c * (charge - n_g) ** 2)
    off_diag = -e_j / 2.0
    idx = np.arange(dim - 1)
    h[idx, idx + 1] = off_diag
    h[idx + 1, idx] = off_diag
    return h


def diagonalize(
    e_c: float,
    e_j: float,
    n_g: float = 0.0,
    n_max: int = 15,
    num_levels: int = 5,
    return_eigenvectors: bool = False,
) -> TransmonSpectrum:
    """Exactly diagonalize the truncated charge-basis Hamiltonian and return
    the lowest `num_levels` eigenenergies.

    `num_levels` must be well below `2*n_max+1` (the full truncated
    dimension) for the low-lying levels to be converged; see
    `energies_vs_truncation` for an explicit convergence check.
    """
    if num_levels < 1:
        raise ValueError(f"num_levels must be >= 1, got {num_levels!r}")
    h = hamiltonian_matrix(e_c, e_j, n_g, n_max)
    if num_levels > h.shape[0]:
        raise ValueError(f"num_levels={num_levels} exceeds basis dimension {h.shape[0]}")

    if not np.allclose(h, h.T):
        raise RuntimeError("internal error: Hamiltonian is not symmetric")  # should be unreachable

    eigvals, eigvecs = np.linalg.eigh(h)
    lowest = eigvals[:num_levels]
    transitions = np.diff(lowest)
    anharm = float((transitions[1] - transitions[0])) if num_levels >= 3 else float("nan")

    return TransmonSpectrum(
        eigenvalues=lowest,
        transition_frequencies=transitions,
        anharmonicity=anharm,
        e_c=e_c,
        e_j=e_j,
        n_g=n_g,
        n_max=n_max,
        eigenvectors=eigvecs[:, :num_levels] if return_eigenvectors else None,
        charge_basis=np.arange(-n_max, n_max + 1) if return_eigenvectors else None,
    )


def asymptotic_energies(e_c: float, e_j: float, num_levels: int = 5) -> np.ndarray:
    """Leading-order large-E_J/E_C transmon asymptotic energies (see module
    docstring for the derivation): E_m = -E_J + sqrt(8*E_J*E_C)*(m+1/2)
    - (E_C/12)*(6*m^2+6*m+3), m = 0, ..., num_levels-1. Not exact; a
    comparison to `diagonalize`, not a replacement for it.
    """
    e_c = _check_positive("e_c", e_c)
    e_j = _check_positive("e_j", e_j)
    if num_levels < 1:
        raise ValueError(f"num_levels must be >= 1, got {num_levels!r}")
    m = np.arange(num_levels, dtype=float)
    omega_p_hbar = math.sqrt(8.0 * e_j * e_c)  # hbar*omega_p, same units as e_c/e_j
    return -e_j + omega_p_hbar * (m + 0.5) - (e_c / 12.0) * (6.0 * m**2 + 6.0 * m + 3.0)


def energies_vs_truncation(
    e_c: float,
    e_j: float,
    n_g: float = 0.0,
    n_max_values: Sequence[int] = (5, 10, 15, 20, 30),
    num_levels: int = 5,
) -> List[np.ndarray]:
    """Lowest `num_levels` eigenenergies at each charge-basis truncation in
    `n_max_values`, for an explicit convergence check (see
    tests/test_transmon.py's charge-basis-truncation test)."""
    return [
        diagonalize(e_c, e_j, n_g=n_g, n_max=n_max, num_levels=num_levels).eigenvalues
        for n_max in n_max_values
    ]
