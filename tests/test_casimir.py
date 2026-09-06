"""Tests for zero_point_energy.casimir, independent of its own internal
formulas where practical (cross-checked against lifshitz.py and modes.py
elsewhere; here mostly internal consistency, signs, scaling, and limits)."""
import math

import pytest

from zero_point_energy import casimir
from zero_point_energy.constants import C_LIGHT, HBAR, K_BOLTZMANN


def test_plate_pressure_is_the_derivative_of_plate_energy():
    """P = -d(E/A)/da, checked via central finite difference against the
    module's own closed-form pressure (a genuinely different computation
    path: differentiation vs. an independently-typed algebraic formula)."""
    a = 3.3e-7
    h = 1e-4 * a
    numeric = -(casimir.plate_energy_per_area(a + h) - casimir.plate_energy_per_area(a - h)) / (2 * h)
    assert numeric == pytest.approx(casimir.plate_pressure(a), rel=1e-6)


def test_plate_pressure_scales_as_inverse_fourth_power():
    a1, a2 = 1e-7, 3e-7
    ratio = casimir.plate_pressure(a1) / casimir.plate_pressure(a2)
    assert ratio == pytest.approx((a2 / a1) ** 4, rel=1e-12)


def test_plate_pressure_and_energy_are_negative_attractive():
    a = 1e-6
    assert casimir.plate_energy_per_area(a) < 0.0
    assert casimir.plate_pressure(a) < 0.0


def test_stress_tensor_diagonal_matches_brown_maclay_pattern():
    """diag(T) = coeff*(-1,1,1,-3); T_zz must equal plate_pressure exactly,
    and T00 must equal -coeff (attractive vacuum energy density sign)."""
    a = 4.2e-7
    t00, txx, tyy, tzz = casimir.stress_tensor_diagonal(a)
    coeff = math.pi**2 * HBAR * C_LIGHT / (720 * a**4)
    assert t00 == pytest.approx(-coeff, rel=1e-14)
    assert txx == pytest.approx(coeff, rel=1e-14)
    assert tyy == pytest.approx(coeff, rel=1e-14)
    assert tzz == pytest.approx(-3 * coeff, rel=1e-14)
    assert tzz == pytest.approx(casimir.plate_pressure(a), rel=1e-14)


def test_plasma_model_pressure_ratio_reduces_to_unity_at_zero_penetration_depth():
    assert casimir.plasma_model_pressure_ratio(1e-7, delta0=0.0) == pytest.approx(1.0)


def test_plasma_model_pressure_ratio_reduces_magnitude_for_finite_conductivity():
    """Finite conductivity should reduce the pressure magnitude below the
    ideal value (ratio < 1) for realistic delta0/a << 1."""
    a = 200e-9
    delta0 = 20e-9  # skin depth an order of magnitude below the gap
    ratio = casimir.plasma_model_pressure_ratio(a, delta0)
    assert 0.0 < ratio < 1.0


def test_sphere_plate_pfa_scales_with_radius_and_gap():
    a = 1e-7
    f1 = casimir.sphere_plate_force_pfa(radius=1e-5, a=a)
    f2 = casimir.sphere_plate_force_pfa(radius=2e-5, a=a)
    assert f2 == pytest.approx(2.0 * f1, rel=1e-12)  # linear in R
    assert f1 < 0.0  # attractive


def test_geometry_scaling_energy_matches_direct_formula_and_scales_as_inverse_length():
    """D12 Route A: E = -C_geom*hbar*c/L for a single-length-scale cavity.
    This is a 3D cavity's total energy (length-to-the-minus-one), a
    genuinely different observable from the 2D parallel-plate E/A (which
    scales as L^-3) -- not expected to numerically coincide with it even
    at the same C_geom value."""
    length = 5e-7
    c_geom = 0.5
    expected = -c_geom * HBAR * C_LIGHT / length
    assert casimir.geometry_scaling_energy(length, c_geom) == pytest.approx(expected, rel=1e-14)
    assert casimir.geometry_scaling_energy(2 * length, c_geom) == pytest.approx(
        0.5 * casimir.geometry_scaling_energy(length, c_geom), rel=1e-12
    )


def test_geometry_scaling_energy_density_matches_direct_formula_and_scales_as_inverse_fourth_power():
    """D12 Route A: E/V = -C'_geom*hbar*c/L^4 for a 3D cavity's energy
    density -- dimensionally distinct from plate_energy_per_area (E/A)."""
    length = 5e-7
    c_prime = math.pi**2 / 720
    expected = -c_prime * HBAR * C_LIGHT / length**4
    assert casimir.geometry_scaling_energy_density(length, c_prime) == pytest.approx(expected, rel=1e-14)
    assert casimir.geometry_scaling_energy_density(2 * length, c_prime) == pytest.approx(
        casimir.geometry_scaling_energy_density(length, c_prime) / 16.0, rel=1e-12
    )


def test_scalar_interval_and_ring_are_both_negative_and_scale_as_inverse_length():
    length1, length2 = 1e-3, 2e-3
    for fn in (casimir.scalar_interval_energy, casimir.scalar_ring_energy):
        assert fn(length1) < 0.0
        assert fn(length1) / fn(length2) == pytest.approx(length2 / length1, rel=1e-12)


def test_boyer_sphere_energy_is_positive_and_scales_as_inverse_radius():
    r1, r2 = 1e-6, 3e-6
    e1 = casimir.boyer_sphere_energy(r1)
    e2 = casimir.boyer_sphere_energy(r2)
    assert e1 > 0.0  # outward stress, opposite sign to the plate case
    assert e1 / e2 == pytest.approx(r2 / r1, rel=1e-12)


def test_high_temperature_limits_scale_linearly_with_temperature_and_inverse_cube_with_gap():
    a = 5e-6
    t1, t2 = 100.0, 300.0
    for fn in (casimir.high_temperature_pressure_ideal, casimir.high_temperature_pressure_drude):
        p1 = fn(a, t1, K_BOLTZMANN)
        p2 = fn(a, t2, K_BOLTZMANN)
        assert p2 / p1 == pytest.approx(t2 / t1, rel=1e-12)
    p_ideal = casimir.high_temperature_pressure_ideal(a, t1, K_BOLTZMANN)
    p_drude = casimir.high_temperature_pressure_drude(a, t1, K_BOLTZMANN)
    assert p_drude == pytest.approx(0.5 * p_ideal, rel=1e-12)


def test_high_temperature_pressures_are_finite_and_negative():
    a = 1e-6
    assert casimir.high_temperature_pressure_ideal(a, 300.0, K_BOLTZMANN) < 0.0
    assert casimir.high_temperature_pressure_drude(a, 300.0, K_BOLTZMANN) < 0.0
