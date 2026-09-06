"""Tests for zero_point_energy.thermal: Unruh/Hawking temperature, black-hole
evaporation, chiral CFT flux, and the Schwinger effect."""
import math

import pytest

from zero_point_energy import thermal
from zero_point_energy.constants import C_LIGHT, G_NEWTON, HBAR, K_BOLTZMANN

SOLAR_MASS = 1.98847e30


def test_unruh_temperature_scales_linearly_with_acceleration():
    a1, a2 = 9.8, 98.0
    assert thermal.unruh_temperature(a2) / thermal.unruh_temperature(a1) == pytest.approx(a2 / a1, rel=1e-12)


def test_unruh_temperature_matches_direct_formula():
    a = 1e20  # a large, lab-irrelevant acceleration where T_U isn't absurdly tiny
    expected = HBAR * a / (2 * math.pi * C_LIGHT * K_BOLTZMANN)
    assert thermal.unruh_temperature(a) == pytest.approx(expected, rel=1e-14)


def test_rindler_occupation_vanishes_at_high_frequency_and_diverges_at_low():
    a = 1e20
    high_omega_occupation = thermal.rindler_thermal_occupation(1e12, a)
    low_omega_occupation = thermal.rindler_thermal_occupation(1e-5, a)
    assert 0.0 < high_omega_occupation < 1e-7
    assert low_omega_occupation > 1e3  # Bose-like divergence as omega -> 0


def test_rindler_occupation_does_not_overflow_for_extreme_exponent():
    """Regression test: omega=1e30, acceleration=1e20 gives an exponent
    2*pi*omega*c/a ~ 2e18, which previously raised OverflowError from
    math.expm1 instead of returning the correctly-rounded 0.0 (found while
    writing this test; fixed in zero_point_energy/thermal.py, not by
    weakening this test)."""
    result = thermal.rindler_thermal_occupation(1e30, 1e20)
    assert result == 0.0


def test_rindler_occupation_matches_bose_einstein_form_at_unruh_temperature():
    """|beta_omega|^2 = 1/(e^{hbar*omega/(kB*T_U)} - 1) exactly, given the
    Unruh temperature -- an independent recomputation via T_U rather than
    reusing rindler_thermal_occupation's own exponent form."""
    a = 5e19
    t_u = thermal.unruh_temperature(a)
    omega = 3.0e9
    expected = 1.0 / (math.expm1(HBAR * omega / (K_BOLTZMANN * t_u)))
    assert thermal.rindler_thermal_occupation(omega, a) == pytest.approx(expected, rel=1e-10)


def test_hawking_temperature_scales_inversely_with_mass():
    m1, m2 = SOLAR_MASS, 3 * SOLAR_MASS
    assert thermal.hawking_temperature(m2) / thermal.hawking_temperature(m1) == pytest.approx(
        m1 / m2, rel=1e-12
    )


def test_hawking_temperature_matches_surface_gravity_formula():
    """T_H = hbar*kappa/(2*pi*c*kB) with kappa = c^4/(4*G*M) (D71/D74),
    checked as an independent two-step computation rather than the
    module's single-step hawking_temperature formula."""
    mass = SOLAR_MASS
    kappa = thermal.schwarzschild_surface_gravity(mass)
    expected = HBAR * kappa / (2 * math.pi * C_LIGHT * K_BOLTZMANN)
    assert thermal.hawking_temperature(mass) == pytest.approx(expected, rel=1e-12)


def test_hawking_power_benchmark_and_evaporation_time_scale_correctly():
    m1, m2 = SOLAR_MASS, 2 * SOLAR_MASS
    p1 = thermal.hawking_power_benchmark(m1)
    p2 = thermal.hawking_power_benchmark(m2)
    assert p2 / p1 == pytest.approx((m1 / m2) ** 2, rel=1e-10)  # P ~ M^-2

    t1 = thermal.evaporation_time_benchmark(m1)
    t2 = thermal.evaporation_time_benchmark(m2)
    assert t2 / t1 == pytest.approx((m2 / m1) ** 3, rel=1e-10)  # t_evap ~ M^3


def test_evaporation_time_is_consistent_with_power_benchmark_by_direct_integration():
    """dM/dt = -P/c^2 with P = hbar*c^6/(15360*pi*G^2*M^2) integrates to
    t_evap = (5120*pi*G^2/(hbar*c^4))*M^3 (D72); check this by direct
    symbolic integration rather than trusting the two formulas share an
    algebra mistake in the same direction."""
    mass = SOLAR_MASS
    # integral of M^2 dM from 0 to M0, scaled by the P(M) prefactor's inverse
    prefactor = 15360 * math.pi * G_NEWTON**2 / (HBAR * C_LIGHT**4)
    # dM/dt = -1/(prefactor*M^2) => prefactor*M^2 dM = -dt => t = prefactor*M0^3/3
    t_predicted = prefactor * mass**3 / 3.0
    assert thermal.evaporation_time_benchmark(mass) == pytest.approx(t_predicted, rel=1e-10)


def test_chiral_cft_flux_scales_as_temperature_squared_and_central_charge():
    t1, t2 = 100.0, 400.0
    assert thermal.chiral_cft_thermal_flux(t2) / thermal.chiral_cft_thermal_flux(t1) == pytest.approx(
        (t2 / t1) ** 2, rel=1e-12
    )
    assert thermal.chiral_cft_thermal_flux(100.0, c_cft=3.0) == pytest.approx(
        3.0 * thermal.chiral_cft_thermal_flux(100.0, c_cft=1.0), rel=1e-12
    )


def test_schwinger_critical_field_matches_direct_formula_for_electron():
    m_e = 9.1093837015e-31
    e_charge = 1.602176634e-19
    expected = m_e**2 * C_LIGHT**3 / (e_charge * HBAR)
    assert thermal.schwinger_critical_field(m_e, e_charge) == pytest.approx(expected, rel=1e-13)


def test_schwinger_rate_vanishes_below_and_grows_toward_critical_field():
    """The exponential suppression exp(-pi*m^2*c^3/(hbar*e*E)) underflows
    to exactly 0.0 in float64 well before E reaches 1e-3*E_critical
    (exponent ~ -3142 there) -- that IS the physically correct rate at
    that precision, not a bug, so this test uses field ratios (0.05, 0.5)
    where the rate is still representable, to meaningfully compare weak vs.
    strong rather than compare two identical floating-point zeros."""
    m_e = 9.1093837015e-31
    e_charge = 1.602176634e-19
    e_critical = thermal.schwinger_critical_field(m_e, e_charge)
    rate_weak = thermal.schwinger_pair_rate_leading(0.05 * e_critical, m_e, e_charge)
    rate_strong = thermal.schwinger_pair_rate_leading(0.5 * e_critical, m_e, e_charge)
    assert 0.0 < rate_weak < rate_strong
    assert math.isfinite(rate_weak)
    assert math.isfinite(rate_strong)


def test_schwinger_rate_underflows_to_exactly_zero_far_below_critical_field():
    """Documents the underflow behavior noted above as an explicit,
    intentional check rather than leaving it as surprising behavior."""
    m_e = 9.1093837015e-31
    e_charge = 1.602176634e-19
    e_critical = thermal.schwinger_critical_field(m_e, e_charge)
    rate = thermal.schwinger_pair_rate_leading(1e-3 * e_critical, m_e, e_charge)
    assert rate == 0.0
    assert math.isfinite(rate)


def test_schwinger_rate_matches_direct_formula():
    m_e = 9.1093837015e-31
    e_charge = 1.602176634e-19
    field = 0.3 * thermal.schwinger_critical_field(m_e, e_charge)
    expected = (e_charge * field) ** 2 / (4 * math.pi**3 * HBAR**2 * C_LIGHT) * math.exp(
        -math.pi * m_e**2 * C_LIGHT**3 / (HBAR * e_charge * field)
    )
    assert thermal.schwinger_pair_rate_leading(field, m_e, e_charge) == pytest.approx(expected, rel=1e-12)
