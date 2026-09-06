"""Physical constants and D067-ART-v1 reference values from the source monograph.

Every block below is transcribed from a specific section or appendix of
*"Adaptive-Resonance-Tracked Phononic Piezoelectric Light Source"*
(Lockwood, September 2026). Values are quoted at the monograph's own
precision; that precision reflects a sharply resonant reduced-order model,
not measurement precision -- no experiment has been performed (Appendix F).
"""
from __future__ import annotations

import math

# --- Fundamental constants (post-2019 SI, exact) --------------------------
H_PLANCK = 6.62607015e-34          # J s
C_LIGHT = 299792458.0              # m/s

# Peak photopic luminous efficacy, defined exactly at 555 nm (SI/CGPM).
LUMINOUS_EFFICACY_555NM = 683.0    # lm/W

# --- Appendix C: D067 physical reference parameters ------------------------
# "Current reduced-order engineering targets" for the physically
# constrained PZT-5A design.
BULB_RADIUS = 3.34444444444444439e-02          # m
ACTIVE_HEIGHT = 5.75000000000000000e-02        # m
SHELL_THICKNESS = 1.77333333333333338e-03      # m
PIEZO_MATERIAL = "PZT-5A"
PIEZO_COVERAGE = 6.50000000000000022e-01
PIEZO_THICKNESS = 6.49999999999999970e-04      # m
PIEZO_HEIGHT_FRACTION = 9.00000000000000022e-01
RESONATOR_MASS_SCALE = 1.00000000000000000e+00
LOCAL_STIFFNESS_SCALE = 1.75000000000000000e+00
DAMPING_SCALE = 1.25000000000000000e+00

CAPACITANCE_CP = 1.63686122094644199e-07       # F (piezoelectric capacitance)
COUPLING_THETA = 1.20949631597844637e-02       # electromechanical coupling
KAPPA_EFF_SQUARED = 1.23001189186170844e-03    # reduced effective coupling measure

MODE_1_HZ = 1.83592556468482883e+02            # lower mechanical branch
MODE_2_HZ = 7.53481662427537117e+02            # upper mechanical branch

# --- Section 15/20: physically constrained operating point -----------------
OPERATING_FREQUENCY_HZ = 1.83592556468478932e+02
LOAD_RESISTANCE_OHM = 5.29606372893091338e+03
REFERENCE_BASE_ACCEL = 1.00000000000000000e+00  # m/s^2 (peak)

PIEZO_AC_POWER_W = 1.29380171299124175e-04
OPTICAL_POWER_W = 4.42790698254122647e-05
MECH_TO_ELEC_EFFICIENCY = 1.83361290460046060e-02
TOTAL_OPTICAL_EFFICIENCY = 6.27535680470461734e-03
PEAK_VOLTAGE_V = 1.17064566155618577

SHELL_SAFETY_FACTOR = 4.47813800228649495
PIEZO_SAFETY_FACTOR = 2.01643731830532191

HALF_POWER_BANDWIDTH_HZ = 3.06168876413914859
EFFECTIVE_Q = 5.99644740572118309e+01

REFERENCE_WAVELENGTH_M = 555e-9                 # 555 nm reference
PHOTON_RATE_HZ = 1.23712829446936031e+14        # s^-1 at 555 nm
PHOTOPIC_LUMEN_EQUIVALENT = 3.02426046907565763e-02  # idealized monochromatic lm

# --- Section 16: robustness (Appendix D manufacturing corners) -------------
ROBUST_NOMINAL_OPTICAL_POWER_W = 4.42790698254155377e-05
ROBUST_WORST_CASE_OPTICAL_POWER_W = 1.98685301570967799e-06
ROBUSTNESS_RATIO = 4.48711552330138055e-02
FIXED_POINT_ALL_DESIGN_WORST_CASE_W = 2.28401432071939221e-06

# --- Appendix D: deterministic manufacturing-corner perturbations ----------
# Two-sided (+/-) perturbations; Cartesian product gives 2**5 = 32 corners.
MANUFACTURING_CORNERS = {
    "resonator_mass": 0.05,
    "local_coupling_stiffness": 0.05,
    "piezo_thickness": 0.05,
    "electrode_coverage": 0.03,
    "damping": 0.10,
}
N_MANUFACTURING_CORNERS = 2 ** len(MANUFACTURING_CORNERS)


def fractional_half_power_bandwidth() -> float:
    """BW / f_r, the fraction of the carrier the usable resonance spans (Sec. 17)."""
    return HALF_POWER_BANDWIDTH_HZ / OPERATING_FREQUENCY_HZ
