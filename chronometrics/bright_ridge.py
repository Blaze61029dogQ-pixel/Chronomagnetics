"""Independent numeric search for the bright-ridge local maximum.

The registry's K_QP = (38/219)*q_Delta is presented as an *audited*
proxy for arg local max |V_proxy(kappa)|, not as an exact identity. This
module reruns that search independently (a bounded scalar optimisation
around the canonical K_QP) so the claim is checked rather than trusted.

Status: AUDITED, not exact.
"""
from __future__ import annotations

from dataclasses import dataclass

from scipy.optimize import minimize_scalar

from . import constants as C


def _abs_v_proxy(kappa: float) -> float:
    return float(abs(C.V_proxy(kappa)))


@dataclass
class BrightRidgeResult:
    canonical_k_qp: float
    located_kappa: float
    miss: float


def locate(window: float = 0.01) -> BrightRidgeResult:
    """Search for the local |V_proxy| maximum near the canonical K_QP."""
    k_qp = float(C.K_QP)
    result = minimize_scalar(
        lambda k: -_abs_v_proxy(k),
        bounds=(k_qp - window, k_qp + window),
        method='bounded',
        options={'xatol': 1e-12},
    )
    return BrightRidgeResult(
        canonical_k_qp=k_qp,
        located_kappa=result.x,
        miss=result.x - k_qp,
    )
