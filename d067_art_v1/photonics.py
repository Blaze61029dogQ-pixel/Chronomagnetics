"""Optical-power to photon-rate and idealized luminous-flux conversions (Sec. 20).

The luminous-flux conversion below is an idealized monochromatic reference
using the exact SI luminous efficacy K_cd (683 lm/W, defined at exactly
540e12 Hz) evaluated at the ~555 nm engineering reference wavelength, not
a prediction of an actual broadband LED spectrum (Appendix F). K_cd is not
"defined at 555 nm"; see constants.py for the exact SI definition and the
derived (unrounded) defining wavelength LAMBDA_CD_M.
"""
from __future__ import annotations

from .constants import C_LIGHT, H_PLANCK, K_CD


def photon_energy(wavelength_m: float) -> float:
    """E = h c / lambda."""
    return H_PLANCK * C_LIGHT / wavelength_m


def photon_rate(optical_power_w: float, wavelength_m: float) -> float:
    """Photon emission rate = P_optical / (h c / lambda) (Sec. 20)."""
    return optical_power_w / photon_energy(wavelength_m)


def idealized_photopic_lumens(optical_power_w: float) -> float:
    """Idealized monochromatic photopic-equivalent lumens at ~555 nm (Sec. 20).

    Uses the exact SI luminous efficacy K_cd = 683 lm/W (defined at exactly
    540e12 Hz, not "at 555 nm"), applied here as an idealization at the
    ~555 nm engineering reference wavelength -- not an actual broadband LED
    luminous efficacy.
    """
    return optical_power_w * K_CD
