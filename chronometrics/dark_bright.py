"""Block: Dark-to-Bright Chronometric Separation.

The null branch and the bright branch are different chronometric events:

  * The null branch is exact -- it is where the q-screen leakage
    L_dark(t) = delta_q_squared * cos^2(theta_Delta(t)) vanishes:

        kappa_null(0) = 1/4 - beta_Delta/(2*pi)

  * The bright branch is the audited bright-ridge coordinate:

        kappa_bright = K_QP = (38/219) * q_Delta

This module computes the separation between them:

  Delta_kappa_DB = kappa_bright - kappa_null(0)          (log-time units)
  Delta_theta_DB = 2*pi * Delta_kappa_DB                 (chronometric phase)
  R_DB           = lambda_Delta ** Delta_kappa_DB        (shifted-time ratio)

R_DB > 1 means the bright ridge occurs *after* the null branch in the
frozen log-time clock; R_DB < 1 would mean before.

Status: EXACT, given the (AUDITED, not exact) input K_QP -- i.e. this is a
closed-form consequence of the registry, not a new free parameter.
"""
from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from . import constants as C


@dataclass
class DarkBrightSeparation:
    kappa_null: mp.mpf
    kappa_bright: mp.mpf
    delta_kappa_db: mp.mpf
    delta_theta_db: mp.mpf
    r_db: mp.mpf


def compute() -> DarkBrightSeparation:
    kappa_null = C.kappa_null(0)
    kappa_bright = mp.mpf(C.K_QP)

    delta_kappa_db = kappa_bright - kappa_null
    delta_theta_db = 2 * mp.pi * delta_kappa_db
    r_db = C.LAMBDA_DELTA_MPF ** delta_kappa_db

    return DarkBrightSeparation(
        kappa_null=kappa_null,
        kappa_bright=kappa_bright,
        delta_kappa_db=delta_kappa_db,
        delta_theta_db=delta_theta_db,
        r_db=r_db,
    )
