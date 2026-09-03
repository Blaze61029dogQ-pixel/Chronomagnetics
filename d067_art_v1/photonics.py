"""Optical-power to photon-rate and idealized luminous-flux conversions (Sec. 20).

The 555 nm luminous-flux conversion is an idealized monochromatic
reference at the peak of the photopic luminosity function, not a
prediction of an actual broadband LED spectrum (Appendix F).
"""
from __future__ import annotations

from .constants import C_LIGHT, H_PLANCK, LUMINOUS_EFFICACY_555NM


def photon_energy(wavelength_m: float) -> float:
    """E = h c / lambda."""
    return H_PLANCK * C_LIGHT / wavelength_m


def photon_rate(optical_power_w: float, wavelength_m: float) -> float:
    """Photon emission rate = P_optical / (h c / lambda) (Sec. 20)."""
    return optical_power_w / photon_energy(wavelength_m)


def idealized_photopic_lumens(optical_power_w: float) -> float:
    """Idealized monochromatic photopic-equivalent lumens at 555 nm (Sec. 20).

    Uses the exact peak photopic luminous efficacy (683 lm/W at 555 nm),
    not an actual broadband LED luminous efficacy.
    """
    return optical_power_w * LUMINOUS_EFFICACY_555NM
