"""Frozen spectral operator L_chrono = -d^2/dkappa^2 + U(kappa) on [0, 12].

This reproduces (independently, via a plain finite-difference solve) the
"frozen spectral gap" G_12 = E_12 - E_11 audited in the source registry
against the candidate closed form G_12 ~= (101/63) * q_Delta^2, and the
rejected candidate G_16 ~= 6*(lambda_Delta - 1) for G_16 = E_16 - E_15.

Status: AUDITED (a frozen-operator numerical relation), not an exact
identity, and not claimed to be universal across other operators.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np
from scipy.linalg import eigh_tridiagonal

from . import constants as C

BETA_DELTA_F = float(C.BETA_DELTA)
K_QP_F = float(C.K_QP)
B_GATE_F = float(C.B_GATE)
D_DEFECT_F = float(C.D_DEFECT)
DOMAIN_LENGTH = 12.0


def _theta(kappa: np.ndarray) -> np.ndarray:
    return 2 * np.pi * kappa + BETA_DELTA_F


def _w_rec(kappa: np.ndarray, half_width: int = 6) -> np.ndarray:
    coeff = 800.0 / 9.0
    total = np.zeros_like(kappa)
    lo = int(np.floor(kappa.min())) - half_width
    hi = int(np.ceil(kappa.max())) + half_width
    for n in range(lo, hi + 1):
        total += np.exp(-coeff * (kappa - n) ** 2)
    return total


def potential(kappa: np.ndarray) -> np.ndarray:
    """U(kappa) -- the fully-expanded frozen potential."""
    w = _w_rec(kappa)
    theta = _theta(kappa)
    return (1.0
            - w * np.cos(theta + K_QP_F)
            + B_GATE_F * w ** 2 * np.cos(theta) ** 2
            + D_DEFECT_F * (kappa + 1.0))


@dataclass
class SpectralResult:
    n_interior: int
    step: float
    eigenvalues: np.ndarray

    def gap(self, n_upper: int, n_lower: int) -> float:
        """G_{n_upper,n_lower} = E_{n_upper} - E_{n_lower}, 1-indexed E_1=ground state."""
        return float(self.eigenvalues[n_upper - 1] - self.eigenvalues[n_lower - 1])


def solve(n_interior: int = 4000, n_eigs: int = 20) -> SpectralResult:
    """Finite-difference Dirichlet solve of L_chrono on [0, 12]."""
    h = DOMAIN_LENGTH / (n_interior + 1)
    kappa_grid = np.linspace(h, DOMAIN_LENGTH - h, n_interior)
    diag = 2.0 / h ** 2 + potential(kappa_grid)
    offdiag = -np.ones(n_interior - 1) / h ** 2
    eigvals = eigh_tridiagonal(
        diag, offdiag, select='i', select_range=(0, n_eigs - 1),
        eigvals_only=True,
    )
    return SpectralResult(n_interior=n_interior, step=h, eigenvalues=eigvals)


def g12_target() -> Fraction:
    """Candidate closed form: G_12 ~= (101/63) * q_Delta^2."""
    return Fraction(101, 63) * C.Q_DELTA_SQ


def g16_target() -> Fraction:
    """Rejected candidate: G_16 ~= 6*(lambda_Delta - 1)."""
    return C.G_16_TARGET
