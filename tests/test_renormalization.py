"""Tests for zero_point_energy.renormalization: regulator-independence
demonstration via four independent regularization routes on the 1D scalar
Dirichlet-interval benchmark, plus the EM parallel-plate cross-check."""
import pytest

from zero_point_energy.casimir import plate_energy_per_area, plate_pressure, scalar_interval_energy
from zero_point_energy.lifshitz import zero_temperature_free_energy_per_area
from zero_point_energy.materials import PerfectConductor
from zero_point_energy.constants import C_LIGHT
from zero_point_energy.renormalization import (
    abel_plana_remainder,
    exponential_cutoff_remainder,
    mode_sum_minus_continuum_remainder,
    parallel_plate_benchmark,
    renormalized_casimir_energy_1d_interval,
    zeta_regularized_energy,
)

REFERENCE_REMAINDER = -1.0 / 12.0


def test_zeta_regularization_reproduces_minus_one_twelfth():
    result = zeta_regularized_energy()
    assert result.remainder == pytest.approx(REFERENCE_REMAINDER, abs=1e-15)


def test_abel_plana_reproduces_minus_one_twelfth_directly_at_zero_regulator():
    """The Abel-Plana route needs no divergent subtraction even at a=0."""
    result = abel_plana_remainder(0.0)
    assert result.remainder == pytest.approx(REFERENCE_REMAINDER, abs=1e-8)


def test_exponential_cutoff_converges_to_minus_one_twelfth_as_regulator_shrinks():
    errors = []
    for a in (1e-2, 1e-3, 1e-4, 1e-5):
        result = exponential_cutoff_remainder(a)
        errors.append(result.absolute_error)
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < 1e-11


def test_exponential_cutoff_error_scales_quadratically_with_regulator():
    """sum_n n e^{-na} = 1/a^2 - 1/12 + O(a^2): each 10x reduction in the
    regulator should cut the remainder's error by ~100x."""
    errs = [exponential_cutoff_remainder(a).absolute_error for a in (1e-2, 1e-3, 1e-4)]
    ratio_1 = errs[0] / errs[1]
    ratio_2 = errs[1] / errs[2]
    assert 90 < ratio_1 < 110
    assert 90 < ratio_2 < 110


def test_mode_sum_minus_continuum_matches_exponential_cutoff_route():
    """Two different code paths (closed-form algebra vs independent
    discrete-sum-minus-quadrature-integral) must agree at the same regulator."""
    a = 1e-3
    r1 = exponential_cutoff_remainder(a)
    r2 = mode_sum_minus_continuum_remainder(a)
    assert r1.remainder == pytest.approx(r2.remainder, rel=1e-12)


def test_exponential_cutoff_does_not_lose_precision_at_small_regulator():
    """At a=1e-8, the divergent piece 1/a^2 ~ 1e16 while the finite
    remainder is ~0.083 -- a naive IEEE-double subtraction here would be
    dominated by roundoff (1e16 has ~1e-16 relative == O(1) absolute
    uncertainty at that scale, swamping the target 0.083). The mpmath
    50-digit implementation must still recover the correct remainder."""
    result = exponential_cutoff_remainder(1e-8, dps=50)
    assert result.absolute_error < 1e-14


def test_all_four_routes_agree_on_the_renormalized_1d_casimir_energy():
    length = 1e-3
    reference = scalar_interval_energy(length)
    for method in ("exponential", "mode_sum", "zeta", "abel_plana"):
        value = renormalized_casimir_energy_1d_interval(length, method=method)
        assert value == pytest.approx(reference, rel=1e-10)


def test_unknown_method_is_rejected():
    with pytest.raises(ValueError):
        renormalized_casimir_energy_1d_interval(1e-3, method="not_a_method")


def test_nonpositive_regulator_and_length_are_rejected():
    with pytest.raises(ValueError):
        exponential_cutoff_remainder(0.0)
    with pytest.raises(ValueError):
        exponential_cutoff_remainder(-1.0)
    with pytest.raises(ValueError):
        renormalized_casimir_energy_1d_interval(0.0)


# --- Electromagnetic 3D benchmark and cross-check against lifshitz.py ------

def test_parallel_plate_benchmark_matches_casimir_module():
    a = 250e-9
    e_over_a, p = parallel_plate_benchmark(a)
    assert e_over_a == plate_energy_per_area(a)
    assert p == plate_pressure(a)


def test_parallel_plate_benchmark_matches_independent_lifshitz_calculation():
    """Regulator independence, demonstrated by an entirely different
    numerical method: the 3D Matsubara/Fresnel Lifshitz sum (lifshitz.py)
    at T->0 for a perfect conductor must reproduce the same finite
    parallel-plate energy as the 1D-mode-counting-derived closed form."""
    a = 1e-6
    e_over_a, _p = parallel_plate_benchmark(a)
    lifshitz_result = zero_temperature_free_energy_per_area(
        a, PerfectConductor(), xi_max=50 * C_LIGHT / a
    )
    assert lifshitz_result.free_energy_per_area == pytest.approx(e_over_a, rel=1e-10)
