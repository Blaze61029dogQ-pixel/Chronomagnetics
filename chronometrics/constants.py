"""Chronometric triangle, phase law, screen defect, and gate model.

Everything in this module traces back to one triangle:

    a = |BC| = 144
    b = |CA| = 138
    c = |AB| = 116

Status tags (see package docstring): EXACT, FROZEN, AUDITED, REJECTED.
"""
from __future__ import annotations

from fractions import Fraction

import mpmath as mp

mp.mp.dps = 50

# ---------------------------------------------------------------------------
# 1. Chronometric triangle seed                                      [EXACT]
# ---------------------------------------------------------------------------
A_SIDE, B_SIDE, C_SIDE = 144, 138, 116
PERIMETER = A_SIDE + B_SIDE + C_SIDE                       # 398
SEMIPERIMETER = Fraction(PERIMETER, 2)                     # 199

AREA_SQ = (SEMIPERIMETER
           * (SEMIPERIMETER - A_SIDE)
           * (SEMIPERIMETER - B_SIDE)
           * (SEMIPERIMETER - C_SIDE))                     # Heron's formula
assert AREA_SQ == 55414535, "Heron area-squared identity broke"
AREA_DELTA = mp.sqrt(int(AREA_SQ))                          # sqrt(55414535)

SUM_SQUARES = A_SIDE ** 2 + B_SIDE ** 2 + C_SIDE ** 2       # 53236
assert SUM_SQUARES == 53236
THIRTEEN_309 = Fraction(SUM_SQUARES, 4)                     # 13309
assert THIRTEEN_309 == 13309


def triangle_vertices():
    """Exact coordinate model: A=(0,0), B=(c,0), C=(2941/58, sqrt(55414535)/58)."""
    ax = Fraction(2941, 58)
    ay = mp.sqrt(int(AREA_SQ)) / 58
    return (mp.mpf(0), mp.mpf(0)), (mp.mpf(C_SIDE), mp.mpf(0)), (mp.mpf(ax), ay)


# ---------------------------------------------------------------------------
# 2. Brocard phase seed (triangle-derived)                            [EXACT]
# ---------------------------------------------------------------------------
# tan(beta_Delta) = 4*Area / (a^2+b^2+c^2) = Area / 13309
assert THIRTEEN_309 ** 2 + AREA_SQ == 232544016
BETA_DELTA = mp.atan(AREA_DELTA / int(THIRTEEN_309))

# ---------------------------------------------------------------------------
# 3. q-screen constant and exact leakage defect                      [EXACT]
# ---------------------------------------------------------------------------
Q_DELTA_NUMER = 7444
assert Q_DELTA_NUMER ** 2 == 55413136
Q_DELTA = Q_DELTA_NUMER / AREA_DELTA
Q_DELTA_SQ = Fraction(Q_DELTA_NUMER ** 2, int(AREA_SQ))     # 55413136/55414535
DELTA_Q_SQUARED = 1 - Q_DELTA_SQ                            # 1399/55414535
assert DELTA_Q_SQUARED == Fraction(1399, 55414535)


def Z_Delta_of_theta(theta) -> mp.mpf:
    """Screen projection Z_Delta(t) = q_Delta * cos(theta_Delta(t))."""
    return Q_DELTA * mp.cos(theta)


def L_dark_of_theta(theta) -> mp.mpf:
    """Exact leakage: cos^2(theta) - Z_Delta(theta)^2 = delta_q_squared * cos^2(theta)."""
    return mp.cos(theta) ** 2 - Z_Delta_of_theta(theta) ** 2


# ---------------------------------------------------------------------------
# 4. Frozen log-time scale and phase law                             [FROZEN]
# ---------------------------------------------------------------------------
LAMBDA_DELTA = Fraction(3722, 2705)
LAMBDA_DELTA_MPF = mp.mpf(3722) / 2705
LN_LAMBDA_DELTA = mp.log(LAMBDA_DELTA_MPF)
OMEGA_DELTA = 2 * mp.pi / LN_LAMBDA_DELTA


def kappa_log(t, t_c, T_0) -> mp.mpf:
    """Dimensionless log-time coordinate."""
    return mp.log((t + t_c) / T_0) / LN_LAMBDA_DELTA


def inverse_kappa_log(kappa, t_c, T_0) -> mp.mpf:
    """Inverse map: t + t_c = T_0 * lambda_Delta^kappa."""
    return T_0 * LAMBDA_DELTA_MPF ** kappa - t_c


def theta_Delta(kappa) -> mp.mpf:
    """theta_Delta(kappa_log) = 2*pi*kappa_log + beta_Delta."""
    return 2 * mp.pi * kappa + BETA_DELTA


# ---------------------------------------------------------------------------
# 5. Brocard leakage-null branch                             [EXACT, in form]
# ---------------------------------------------------------------------------
def kappa_null(n: int = 0) -> mp.mpf:
    """Coordinates where cos(theta_Delta)=0, i.e. exact leakage vanishes."""
    return mp.mpf(1) / 4 - BETA_DELTA / (2 * mp.pi) + mp.mpf(n) / 2


# ---------------------------------------------------------------------------
# 6. Locked recurrence gate and gate triplet                         [FROZEN]
# ---------------------------------------------------------------------------
SIGMA_KAPPA = Fraction(3, 40)
CHI = Fraction(7, 20)
MU = Fraction(1, 2)
assert CHI * MU == Fraction(7, 40)         # product-invariant lock
M_HARMONIC = 7

_W_REC_COEFF = mp.mpf(800) / 9             # 1/(2*sigma_kappa^2)


def W_rec(kappa, half_width: int = 8) -> mp.mpf:
    """Recurrence gate: sum over integers n of a narrow Gaussian bump at n."""
    kappa = mp.mpf(kappa)
    n0 = int(mp.floor(kappa))
    total = mp.mpf(0)
    for n in range(n0 - half_width, n0 + half_width + 1):
        total += mp.exp(-_W_REC_COEFF * (kappa - n) ** 2)
    return total


def _mpf(frac: Fraction) -> mp.mpf:
    return mp.mpf(frac.numerator) / frac.denominator


def G_gate(kappa) -> mp.mpf:
    """G(kappa) = chi * W_rec(kappa) * Z_Delta(kappa)."""
    return _mpf(CHI) * W_rec(kappa) * Z_Delta_of_theta(theta_Delta(kappa))


def Gamma_phase(kappa) -> mp.mpf:
    """Bounded phase: Gamma(kappa) = theta_Delta(kappa) + mu*tanh(G(kappa))."""
    return theta_Delta(kappa) + _mpf(MU) * mp.tanh(G_gate(kappa))


def dGamma_dkappa(kappa) -> mp.mpf:
    return mp.diff(Gamma_phase, kappa)


# ---------------------------------------------------------------------------
# 7. Effective readout and Josephson-style voltage proxy       [FROZEN model,
#                                                                 PROXY only]
# ---------------------------------------------------------------------------
HBAR = mp.mpf('1.054571817e-34')
E_CHARGE = mp.mpf('1.602176634e-19')
JOSEPHSON_COEFF = HBAR / (2 * E_CHARGE)


def kappa_eff(kappa, phi_star=1) -> mp.mpf:
    return (phi_star * dGamma_dkappa(kappa) * mp.sin(Gamma_phase(kappa))
            * mp.cos(theta_Delta(kappa) / M_HARMONIC))


def V_proxy(kappa, phi_star=1) -> mp.mpf:
    """Not a measured voltage -- a dimensioned proxy readout only."""
    return JOSEPHSON_COEFF * kappa_eff(kappa, phi_star)


# ---------------------------------------------------------------------------
# 8. Bright-ridge constant K_QP                        [AUDITED, not exact]
# ---------------------------------------------------------------------------
K_QP_RATIO = Fraction(38, 219)
K_QP = (mp.mpf(K_QP_RATIO.numerator) / K_QP_RATIO.denominator) * Q_DELTA  # canonical bright-ridge coordinate

# ---------------------------------------------------------------------------
# 9. Frozen spectral-operator coefficients          (see chronometrics.spectral)
# ---------------------------------------------------------------------------
B_GATE = Fraction(169702729, 2770726750)    # (1/2)*chi^2*q_Delta^2
D_DEFECT = Fraction(1399, 221658140)        # (1/4)*delta_q_squared

# ---------------------------------------------------------------------------
# 10. Iso-gap lock direction (transcribed, not re-derived here)  [FROZEN,
#                                                        first-order, not exact]
# ---------------------------------------------------------------------------
ISO_GAP_SLOPE = Fraction(-20, 7)            # delta_B_gate / delta_chi

# ---------------------------------------------------------------------------
# 11. Rejected lead: gap-16 target                                [REJECTED]
# ---------------------------------------------------------------------------
G_16_TARGET = 6 * (LAMBDA_DELTA - 1)        # = 6102/2705, rejected by audit
