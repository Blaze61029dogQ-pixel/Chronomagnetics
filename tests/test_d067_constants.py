"""Regression tests for the D067 SI photometric metrology fix (Section 5).

These pin down the exact-SI vs. engineering-approximation distinction:
K_cd/nu_cd are exact SI-defined constants, LAMBDA_CD_M is a *derived*,
unrounded quantity, and REFERENCE_WAVELENGTH_M is a clearly separate
engineering approximation.
"""
from __future__ import annotations

import math
from fractions import Fraction

from d067_art_v1 import constants as C


def test_k_cd_is_the_exact_si_luminous_efficacy():
    assert C.K_CD == 683.0


def test_nu_cd_is_the_exact_si_defining_frequency():
    assert C.NU_CD_HZ == 540e12


def test_c_light_is_exact_si_speed_of_light():
    assert C.C_LIGHT == 299792458.0


def test_lambda_cd_is_derived_from_c_and_nu_cd_exactly():
    assert C.LAMBDA_CD_M == C.C_LIGHT / C.NU_CD_HZ


def test_lambda_cd_matches_the_unrounded_closed_form_in_nanometres():
    # 299792458 / 540000000000000 m, reduced, equals 149896229/270000 nm.
    expected_nm = float(Fraction(149896229, 270000))
    assert math.isclose(C.LAMBDA_CD_M * 1e9, expected_nm, rel_tol=0, abs_tol=1e-9)


def test_lambda_cd_is_not_truncated_to_555nm():
    # The exact SI defining wavelength is ~555.1712 nm, not 555 nm -- these
    # must differ by more than rounding noise.
    assert abs(C.LAMBDA_CD_M - 555e-9) > 1e-10


def test_reference_wavelength_is_the_555nm_engineering_approximation():
    assert C.REFERENCE_WAVELENGTH_M == 555e-9


def test_reference_wavelength_and_lambda_cd_are_distinct_named_constants():
    # These must never be silently aliased to each other again.
    assert C.REFERENCE_WAVELENGTH_M != C.LAMBDA_CD_M


def test_no_ambiguous_555nm_constant_name_remains():
    assert not hasattr(C, "LUMINOUS_EFFICACY_555NM")
