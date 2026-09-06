"""Tests for zero_point_energy.units: natural-unit <-> SI energy-density
conversion."""
import pytest

from zero_point_energy import units
from zero_point_energy.constants import E_CHARGE, HBAR_C


def test_gev4_conversion_factor_matches_independent_derivation():
    """1 GeV^4 -> J/m^3 = (1 GeV in Joules)^4 / (hbar*c)^3, recomputed
    directly from the exact SI charge rather than reusing constants.py's
    own GEV_TO_JOULE/HBAR_C combination inside units.py."""
    gev_in_joules = 1.0e9 * E_CHARGE
    expected = gev_in_joules**4 / HBAR_C**3
    assert units.GEV4_TO_JOULE_PER_M3 == pytest.approx(expected, rel=1e-14)


def test_gev4_conversion_matches_documented_reference_value():
    """The ZPE reference document (D13/S6) states 1 GeV^4 = 2.085215688e37 J/m^3."""
    assert units.GEV4_TO_JOULE_PER_M3 == pytest.approx(2.085215688e37, rel=1e-8)


def test_gev4_to_si_and_si_to_gev4_are_inverses():
    value_gev4 = 3.7
    round_trip = units.si_to_gev4(units.gev4_to_si(value_gev4))
    assert round_trip == pytest.approx(value_gev4, rel=1e-12)


def test_gev4_to_si_scales_linearly():
    assert units.gev4_to_si(2.0) == pytest.approx(2.0 * units.gev4_to_si(1.0), rel=1e-14)


def test_gev4_to_si_of_zero_is_zero():
    assert units.gev4_to_si(0.0) == 0.0


def test_gev4_to_si_preserves_sign():
    assert units.gev4_to_si(-1.181e8) < 0.0  # e.g. the electroweak Higgs vacuum value in GeV^4
