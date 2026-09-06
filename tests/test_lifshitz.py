"""Tests for zero_point_energy.lifshitz: finite-temperature planar Lifshitz
free energy and pressure.

Tolerances are set from the observed numerical behavior of the underlying
scipy.integrate.quad calls (see zero_point_energy/lifshitz.py and
SCIENTIFIC_VALIDATION.md for the exact numbers this suite reproduces), not
chosen to make failing assertions pass.
"""
import math

import pytest

from zero_point_energy.casimir import (
    high_temperature_pressure_drude,
    high_temperature_pressure_ideal,
    plate_energy_per_area,
    plate_pressure,
)
from zero_point_energy.constants import C_LIGHT, HBAR, K_BOLTZMANN
from zero_point_energy.lifshitz import (
    finite_temperature_free_energy_per_area,
    matsubara_frequencies,
    pressure,
    zero_temperature_free_energy_per_area,
)
from zero_point_energy.materials import DrudeModel, PerfectConductor, PlasmaModel


# --- A/B: ideal-conductor T -> 0 energy and pressure -----------------------

def test_ideal_conductor_zero_temperature_energy_matches_casimir_1948():
    """A: E/A -> -pi^2 hbar c/(720 a^3) (Casimir 1948)."""
    a = 1e-6
    pc = PerfectConductor()
    res = zero_temperature_free_energy_per_area(a, pc, xi_max=50 * C_LIGHT / a)
    analytic = plate_energy_per_area(a)
    assert res.free_energy_per_area == pytest.approx(analytic, rel=1e-10)


def test_ideal_conductor_zero_temperature_pressure_matches_casimir_1948():
    """B: P -> -pi^2 hbar c/(240 a^4) (Casimir 1948)."""
    a = 1e-6
    pc = PerfectConductor()
    p_numeric = pressure(
        zero_temperature_free_energy_per_area, a, material1=pc, xi_max=50 * C_LIGHT / a
    )
    analytic = plate_pressure(a)
    assert p_numeric == pytest.approx(analytic, rel=1e-6)


def test_ideal_conductor_te_equals_tm_at_zero_temperature():
    """A perfect conductor is polarization-symmetric: TE and TM parts must
    be numerically identical (not just same sign)."""
    a = 1e-6
    pc = PerfectConductor()
    res = zero_temperature_free_energy_per_area(a, pc, xi_max=50 * C_LIGHT / a)
    assert res.te_part == pytest.approx(res.tm_part, rel=1e-10)


# --- C: classical high-temperature ideal-conductor limit -------------------

def test_high_temperature_ideal_conductor_limit():
    """C: at a*kB*T/(hbar*c) >> 1, P -> -zeta(3) kB T/(4 pi a^3) (D28)."""
    a = 20e-6
    T = 300.0
    pc = PerfectConductor()
    p_numeric = pressure(
        finite_temperature_free_energy_per_area, a, material1=pc, temperature=T, quad_epsrel=1e-9
    )
    analytic = high_temperature_pressure_ideal(a, T, K_BOLTZMANN)
    assert p_numeric == pytest.approx(analytic, rel=1e-5)


def test_drude_high_temperature_limit_is_half_ideal_conductor():
    """C (Drude variant, D28): the Drude TE-zero-mode absence halves the
    classical high-T pressure relative to the ideal-conductor/plasma value."""
    a = 20e-6
    T = 300.0
    drude = DrudeModel(omega_p=1.0e20, gamma=1.0e10)  # omega_p -> "ideal metal" limit
    p_numeric = pressure(
        finite_temperature_free_energy_per_area, a, material1=drude, temperature=T, quad_epsrel=1e-9
    )
    analytic = high_temperature_pressure_drude(a, T, K_BOLTZMANN)
    assert p_numeric == pytest.approx(analytic, rel=1e-5)


# --- D: symmetry under exchange of plate 1 and plate 2 ----------------------

def test_symmetric_under_exchange_of_materials():
    a = 300e-9
    T = 300.0
    pc = PerfectConductor()
    drude = DrudeModel(omega_p=1.37e16, gamma=5.3e13)
    res_12 = finite_temperature_free_energy_per_area(a, T, pc, drude, quad_epsrel=1e-8)
    res_21 = finite_temperature_free_energy_per_area(a, T, drude, pc, quad_epsrel=1e-8)
    assert res_12.free_energy_per_area == pytest.approx(res_21.free_energy_per_area, rel=1e-12)
    assert res_12.te_part == pytest.approx(res_21.te_part, rel=1e-12)
    assert res_12.tm_part == pytest.approx(res_21.tm_part, rel=1e-12)


# --- E: free energy -> 0 as separation -> infinity --------------------------

def test_free_energy_vanishes_at_large_separation():
    pc = PerfectConductor()
    res_near = zero_temperature_free_energy_per_area(1e-6, pc, xi_max=50 * C_LIGHT / 1e-6)
    res_far = zero_temperature_free_energy_per_area(1e-3, pc, xi_max=50 * C_LIGHT / 1e-3)
    assert abs(res_far.free_energy_per_area) < abs(res_near.free_energy_per_area) * 1e-8


# --- F: dimensional / power-law scaling -------------------------------------

def test_zero_temperature_energy_scales_as_inverse_cube():
    """E/A ~ a^-3 (Casimir 1948): doubling a should divide |E/A| by 8."""
    pc = PerfectConductor()
    a1 = 1e-6
    a2 = 2e-6
    e1 = zero_temperature_free_energy_per_area(a1, pc, xi_max=50 * C_LIGHT / a1).free_energy_per_area
    e2 = zero_temperature_free_energy_per_area(a2, pc, xi_max=50 * C_LIGHT / a2).free_energy_per_area
    assert (e1 / e2) == pytest.approx(8.0, rel=1e-6)


def test_matsubara_frequencies_are_linear_in_n():
    T = 300.0
    xis = matsubara_frequencies(T, 5)
    expected_step = 2 * math.pi * K_BOLTZMANN * T / HBAR
    assert xis[0] == 0.0
    for n, xi_n in enumerate(xis):
        assert xi_n == pytest.approx(expected_step * n, rel=1e-14)


# --- G: TE and TM contributions remain finite -------------------------------

def test_te_and_tm_parts_are_finite_for_various_materials():
    a = 500e-9
    T = 300.0
    for material in (PerfectConductor(), PlasmaModel(1.37e16), DrudeModel(1.37e16, 5.3e13)):
        res = finite_temperature_free_energy_per_area(a, T, material, quad_epsrel=1e-8)
        assert math.isfinite(res.te_part)
        assert math.isfinite(res.tm_part)
        assert res.te_part <= 0.0  # attractive free energy contributions
        assert res.tm_part <= 0.0


# --- H: explicit zero-mode tests --------------------------------------------

def test_zero_mode_reflection_matches_material_prescription():
    """H: the n=0 Matsubara term's reflection coefficients must match each
    material's documented zero-mode prescription (see materials.py)."""
    drude = DrudeModel(omega_p=1.37e16, gamma=5.3e13)
    plasma = PlasmaModel(omega_p=1.37e16)
    pc = PerfectConductor()
    for k_perp in (0.0, 1e5, 1e7):
        assert drude.reflection_coefficients(0.0, k_perp, C_LIGHT)[0] == 0.0
        assert pc.reflection_coefficients(0.0, k_perp, C_LIGHT)[0] == -1.0
    # Leading-order deviation from -1 as k_perp -> 0 is 2*k_perp*c/omega_p
    # (from r_TE=(k_perp-kappa)/(k_perp+kappa), kappa ~ omega_p/c for
    # k_perp << omega_p/c); pick k_perp small enough that this analytic
    # bound is comfortably below the assertion's absolute tolerance.
    k_perp = 1e-3
    expected_deviation = 2 * k_perp * C_LIGHT / plasma.omega_p
    assert expected_deviation < 1e-9
    r_te_plasma_small_k, _ = plasma.reflection_coefficients(0.0, k_perp, C_LIGHT)
    assert r_te_plasma_small_k == pytest.approx(-1.0, abs=1e-9)


def test_drude_and_plasma_differ_only_through_zero_mode_at_high_temperature():
    """H/I: at fixed (a, T) with equal omega_p, Drude and plasma differ, and
    the discrepancy is attributable to the TE zero mode (D28 factor of 2 in
    the classical limit already checked above; here just confirm they are
    numerically distinguishable at all, i.e. the model choice matters)."""
    a = 20e-6
    T = 300.0
    wp = 1.37e16
    drude = DrudeModel(omega_p=wp, gamma=5.3e13)
    plasma = PlasmaModel(omega_p=wp)
    f_drude = finite_temperature_free_energy_per_area(a, T, drude, quad_epsrel=1e-8).free_energy_per_area
    f_plasma = finite_temperature_free_energy_per_area(a, T, plasma, quad_epsrel=1e-8).free_energy_per_area
    # Compare via the ratio explicitly rather than pytest.approx's default
    # absolute tolerance (1e-12), which would spuriously call these two
    # ~1e-13 J/m^2 values "equal" regardless of their relative difference.
    assert abs(f_drude / f_plasma - 1.0) > 0.1


# --- I: Drude/plasma limiting behavior toward the ideal conductor ----------

def test_plasma_approaches_ideal_conductor_as_omega_p_grows():
    """The finite-plasma-frequency correction to the ideal-conductor energy
    vanishes as omega_p grows (a finite plasma frequency makes the plates
    more transparent than an ideal conductor). Empirically, over the
    omega_p range tested here the relative error scales approximately
    linearly in 1/omega_p (each 100x increase in omega_p cuts the error by
    a consistent factor close to 100, confirmed to hold across two
    independent decades below); this is reported as an observed numerical
    fact, not a claimed first-principles derivation."""
    a = 1e-6
    pc = PerfectConductor()
    e_ideal = zero_temperature_free_energy_per_area(
        a, pc, xi_max=50 * C_LIGHT / a, epsrel=1e-10
    ).free_energy_per_area
    errors = []
    for wp in (1e18, 1e21, 1e23, 1e25):
        plasma = PlasmaModel(omega_p=wp)
        e_plasma = zero_temperature_free_energy_per_area(
            a, plasma, xi_max=50 * C_LIGHT / a, epsrel=1e-10
        ).free_energy_per_area
        errors.append(abs(e_plasma - e_ideal) / abs(e_ideal))
    # monotonic convergence to the ideal-conductor value as omega_p grows
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < 1e-9
    # 1e21 -> 1e23 and 1e23 -> 1e25 are both clean 100x steps in omega_p;
    # check the error falls by a consistent factor across them (empirically
    # ~100, i.e. ~linear in 1/omega_p over this range).
    ratio_1 = errors[1] / errors[2]
    ratio_2 = errors[2] / errors[3]
    assert 50 < ratio_1 < 200
    assert 50 < ratio_2 < 200
    assert ratio_1 == pytest.approx(ratio_2, rel=0.1)


# --- J: numerical convergence under tighter tolerances ----------------------

def test_zero_temperature_energy_converges_under_tighter_quad_tolerance():
    a = 1e-6
    pc = PerfectConductor()
    coarse = zero_temperature_free_energy_per_area(
        a, pc, xi_max=50 * C_LIGHT / a, epsrel=1e-6
    ).free_energy_per_area
    tight = zero_temperature_free_energy_per_area(
        a, pc, xi_max=50 * C_LIGHT / a, epsrel=1e-11
    ).free_energy_per_area
    analytic = plate_energy_per_area(a)
    assert abs(tight - analytic) <= abs(coarse - analytic) + 1e-25


def test_finite_temperature_sum_reports_convergence_diagnostics():
    a = 200e-9
    T = 300.0
    pc = PerfectConductor()
    res = finite_temperature_free_energy_per_area(a, T, pc, quad_epsrel=1e-9)
    assert res.converged is True
    assert res.n_matsubara_terms > 1
    assert math.isfinite(res.max_quadrature_error)


def test_finite_temperature_sum_signals_nonconvergence_when_starved():
    """A tiny n_max should be reported as not converged rather than silently
    returning a truncated, uncorrected sum as if it were final."""
    a = 100e-9  # small gap -> Matsubara ladder needs many terms at 300 K
    T = 300.0
    pc = PerfectConductor()
    res = finite_temperature_free_energy_per_area(a, T, pc, n_max=2, quad_epsrel=1e-8)
    assert res.converged is False
    assert res.n_matsubara_terms == 3


# --- Basic input validation --------------------------------------------------

def test_rejects_nonpositive_separation():
    pc = PerfectConductor()
    with pytest.raises(ValueError):
        zero_temperature_free_energy_per_area(0.0, pc)
    with pytest.raises(ValueError):
        zero_temperature_free_energy_per_area(-1e-6, pc)


def test_pressure_rejects_nonpositive_relative_step():
    """Found during the Phase-15 audit: relative_step=0 would otherwise
    divide by zero in the central-difference step h=relative_step*a."""
    pc = PerfectConductor()
    with pytest.raises(ValueError):
        pressure(zero_temperature_free_energy_per_area, 1e-6, relative_step=0.0, material1=pc)
    with pytest.raises(ValueError):
        pressure(zero_temperature_free_energy_per_area, 1e-6, relative_step=-1e-4, material1=pc)


def test_rejects_nonpositive_temperature_for_finite_temperature_call():
    pc = PerfectConductor()
    with pytest.raises(ValueError):
        finite_temperature_free_energy_per_area(1e-6, 0.0, pc)
    with pytest.raises(ValueError):
        finite_temperature_free_energy_per_area(1e-6, -300.0, pc)
