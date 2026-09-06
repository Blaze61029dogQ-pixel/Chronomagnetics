"""Self-check: verify internal algebraic consistency of the source monograph's own numbers.

Run with:

    python3 -m d067_art_v1.report

This does not re-derive the monograph's reduced-order model from first
principles (the underlying per-branch modal mass, stiffness, and stress
allowables are not specified in the condensed report). Instead, each
check below ties two or more independently quoted quantities from the
source document together through a documented formula and verifies they
agree at the document's own precision -- a regression here means a
transcription error in constants.py, not a change in the physics.
"""
from __future__ import annotations

from validation import ValidationError
from validation import check as _check

from . import electromechanical as em
from . import photonics
from .constants import (
    CAPACITANCE_CP,
    COUPLING_THETA,
    EFFECTIVE_Q,
    FIXED_POINT_ALL_DESIGN_WORST_CASE_W,
    HALF_POWER_BANDWIDTH_HZ,
    KAPPA_EFF_SQUARED,
    LOAD_RESISTANCE_OHM,
    MECH_TO_ELEC_EFFICIENCY,
    OPERATING_FREQUENCY_HZ,
    OPTICAL_POWER_W,
    PEAK_VOLTAGE_V,
    PHOTON_RATE_HZ,
    PHOTOPIC_LUMEN_EQUIVALENT,
    PIEZO_AC_POWER_W,
    PIEZO_SAFETY_FACTOR,
    REFERENCE_WAVELENGTH_M,
    ROBUST_WORST_CASE_OPTICAL_POWER_W,
    ROBUST_NOMINAL_OPTICAL_POWER_W,
    ROBUSTNESS_RATIO,
    SHELL_SAFETY_FACTOR,
    TOTAL_OPTICAL_EFFICIENCY,
)


def main() -> None:
    print("D067-ART-v1 -- self-check against the source monograph's own worked numbers")
    print("=" * 78)

    # Sec. 17: Q = f_r / BW.
    _check(
        "Effective Q from f_op / half-power bandwidth",
        em.quality_factor(OPERATING_FREQUENCY_HZ, HALF_POWER_BANDWIDTH_HZ),
        EFFECTIVE_Q,
        tolerance=1e-12,
    )

    # Sec. 19: the design point sits at the capacitive-reactance load match,
    # omega * R_L * C_p ~= 1.
    omega_op = em.angular_frequency_from_hz(OPERATING_FREQUENCY_HZ)
    _check(
        "omega_op * R_L * C_p ~= 1 (impedance-matched load, Sec. 19)",
        omega_op * LOAD_RESISTANCE_OHM * CAPACITANCE_CP,
        1.0,
        tolerance=1e-9,
    )

    # Sec. 19/20: P_load = 0.5 |V|^2 / R_L must invert to the quoted peak voltage.
    _check(
        "Peak voltage from P_piezo = 0.5 V^2 / R_L (Sec. 19/20)",
        em.voltage_from_power(PIEZO_AC_POWER_W, LOAD_RESISTANCE_OHM),
        PEAK_VOLTAGE_V,
        tolerance=1e-12,
    )

    # Sec. 14 physical closure: Theta = sqrt(kappa_eff^2 * K_eff * C_p) must be
    # invertible for a positive effective stiffness K_eff.
    k_eff = em.effective_stiffness_from_theta(COUPLING_THETA, KAPPA_EFF_SQUARED, CAPACITANCE_CP)
    _check(
        "Physical-closure round trip: Theta(K_eff) == COUPLING_THETA",
        em.coupling_theta_from_physical_closure(KAPPA_EFF_SQUARED, k_eff, CAPACITANCE_CP),
        COUPLING_THETA,
        tolerance=1e-12,
    )
    print(f"     (implied local effective stiffness K_eff = {k_eff:.6e} N/m)")

    # Sec. 20: photon rate at 555 nm from the modeled optical power.
    _check(
        "Photon rate @555 nm from optical power",
        photonics.photon_rate(OPTICAL_POWER_W, REFERENCE_WAVELENGTH_M),
        PHOTON_RATE_HZ,
        tolerance=1e-9,
    )

    # Sec. 20: idealized monochromatic photopic lumen equivalent (K_cd = 683
    # lm/W, exact SI value defined at 540e12 Hz, applied at ~555 nm).
    _check(
        "Idealized photopic lumen equivalent @555 nm",
        photonics.idealized_photopic_lumens(OPTICAL_POWER_W),
        PHOTOPIC_LUMEN_EQUIVALENT,
        tolerance=1e-9,
    )

    # Sec. 20: the optical/mechanical efficiency ratio must equal the
    # optical/piezo power ratio (same rectifier/DC/LED conversion chain).
    _check(
        "Efficiency ratio matches optical/piezo power ratio",
        TOTAL_OPTICAL_EFFICIENCY / MECH_TO_ELEC_EFFICIENCY,
        OPTICAL_POWER_W / PIEZO_AC_POWER_W,
        tolerance=1e-9,
    )

    # Sec. 16: robustness ratio R_robust = P_worst / P_nominal.
    _check(
        "Robustness ratio from worst-case / nominal optical power",
        em.robustness_ratio(ROBUST_WORST_CASE_OPTICAL_POWER_W, ROBUST_NOMINAL_OPTICAL_POWER_W),
        ROBUSTNESS_RATIO,
        tolerance=1e-9,
    )

    # Sec. 16: the reduced-order model must actually fail a >=1.0 (full
    # retention) robustness bar -- the finding motivating adaptive tracking.
    if not (ROBUSTNESS_RATIO < 0.5):
        raise ValidationError(
            "robustness ratio no longer supports rejecting passive fixed-frequency "
            f"operation: computed ROBUSTNESS_RATIO={ROBUSTNESS_RATIO!r}, reference=<0.5"
        )
    if not (FIXED_POINT_ALL_DESIGN_WORST_CASE_W < ROBUST_NOMINAL_OPTICAL_POWER_W):
        raise ValidationError(
            "fixed-point all-design worst case is not below the robust nominal "
            f"optical power: computed={FIXED_POINT_ALL_DESIGN_WORST_CASE_W!r}, "
            f"reference=<{ROBUST_NOMINAL_OPTICAL_POWER_W!r}"
        )

    # Sanity: both quoted safety factors exceed the physical-closure
    # requirement of >= 2.0 (Sec. 14), i.e. this is not a rejected design.
    if not (SHELL_SAFETY_FACTOR >= 2.0):
        raise ValidationError(
            f"shell safety factor below required minimum: computed={SHELL_SAFETY_FACTOR!r}, "
            "reference=>=2.0"
        )
    if not (PIEZO_SAFETY_FACTOR >= 2.0):
        raise ValidationError(
            f"piezo safety factor below required minimum: computed={PIEZO_SAFETY_FACTOR!r}, "
            "reference=>=2.0"
        )

    print("=" * 78)
    print("All checks passed. This verifies internal numerical consistency of the")
    print("monograph's own reduced-order results -- it is NOT experimental")
    print("validation and does NOT constitute a 3-D tensor piezoelectric FEM.")
    print()
    print("REDUCED-ORDER ARCHITECTURE FREEZE -- NOT EXPERIMENTALLY VALIDATED.")


if __name__ == "__main__":
    main()
