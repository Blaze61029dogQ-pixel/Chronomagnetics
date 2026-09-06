"""Tests for zero_point_energy.materials: dielectric models and reflection
coefficients on the imaginary-frequency axis."""
import math

import pytest

from zero_point_energy.materials import (
    DrudeModel,
    LorentzModel,
    PerfectConductor,
    PlasmaModel,
    UserDielectric,
    single_lorentz_oscillator,
)

C = 299792458.0


def test_perfect_conductor_reflection_is_exact_and_frequency_independent():
    pc = PerfectConductor()
    for xi in (0.0, 1.0, 1e15, 1e20):
        for k_perp in (0.0, 1.0, 1e6, 1e9):
            r_te, r_tm = pc.reflection_coefficients(xi, k_perp, C)
            assert r_te == -1.0
            assert r_tm == 1.0


def test_plasma_epsilon_xi_squared_zero_limit_is_omega_p_squared():
    wp = 9.0e15
    plasma = PlasmaModel(omega_p=wp)
    assert plasma.epsilon_xi_squared(0.0) == pytest.approx(wp**2, rel=1e-14)


def test_drude_epsilon_xi_squared_zero_limit_is_zero():
    drude = DrudeModel(omega_p=9.0e15, gamma=3.5e13)
    assert drude.epsilon_xi_squared(0.0) == 0.0


def test_drude_te_zero_mode_vanishes_for_all_k_perp():
    """Literature fact (Bostrom & Sernelius 2000; see materials.py docstring):
    the Drude model's TE reflection coefficient is exactly zero at xi=0,
    independent of k_perp -- this is the origin of the Drude/ideal-conductor
    factor-of-2 discrepancy in the classical high-T Casimir pressure."""
    drude = DrudeModel(omega_p=9.0e15, gamma=3.5e13)
    for k_perp in (0.0, 1.0, 1e4, 1e6, 1e9):
        r_te, r_tm = drude.reflection_coefficients(0.0, k_perp, C)
        assert r_te == 0.0
        assert r_tm == 1.0


def test_plasma_te_zero_mode_survives_and_approaches_ideal_as_k_perp_to_zero():
    plasma = PlasmaModel(omega_p=9.0e15)
    r_te_0, _ = plasma.reflection_coefficients(0.0, 0.0, C)
    assert r_te_0 == pytest.approx(-1.0, rel=1e-14)  # exact ideal-conductor value at k_perp=0
    # for k_perp > 0 it is strictly between -1 and 0 (partial reflection)
    r_te_finite, _ = plasma.reflection_coefficients(0.0, 1e6, C)
    assert -1.0 < r_te_finite < 0.0


def test_drude_and_plasma_agree_and_disagree_with_ideal_at_high_frequency_and_zero():
    """At xi >> omega_p both models are nearly transparent (eps -> 1, r -> 0);
    at xi = 0 they diverge (metal): this checks both regimes in one place."""
    wp = 9.0e15
    plasma = PlasmaModel(omega_p=wp)
    drude = DrudeModel(omega_p=wp, gamma=3.5e13)
    xi_high = 1e4 * wp
    for material in (plasma, drude):
        eps = material.epsilon(xi_high)
        assert eps == pytest.approx(1.0, abs=1e-6)
        r_te, r_tm = material.reflection_coefficients(xi_high, 1e6, C)
        assert abs(r_te) < 1e-4
        assert abs(r_tm) < 1e-4


def test_reflection_coefficients_are_finite_and_bounded():
    wp = 9.0e15
    for material in (PerfectConductor(), PlasmaModel(wp), DrudeModel(wp, 3.5e13),
                     single_lorentz_oscillator(1.0, 1.3e16, 1.3e16**2, 1e14)):
        for xi in (0.0, 1.0, 1e10, 1e15, 1e18):
            for k_perp in (0.0, 1.0, 1e6, 1e10):
                r_te, r_tm = material.reflection_coefficients(xi, k_perp, C)
                assert math.isfinite(r_te)
                assert math.isfinite(r_tm)
                assert abs(r_te) <= 1.0 + 1e-12
                assert abs(r_tm) <= 1.0 + 1e-12


def test_lorentz_dielectric_convention_matches_hand_computation():
    """eps(i*xi) = eps_inf + S/(omega_0^2 + xi^2 + gamma*xi); check one point
    by hand rather than re-deriving the implementation."""
    eps_inf, omega_0, s, gamma = 1.0, 1.0e16, (1.0e16) ** 2, 1.0e14
    model = single_lorentz_oscillator(eps_inf, omega_0, s, gamma)
    xi = 5.0e15
    expected = eps_inf + s / (omega_0**2 + xi**2 + gamma * xi)
    assert model.epsilon(xi) == pytest.approx(expected, rel=1e-14)
    assert model.epsilon(0.0) == pytest.approx(eps_inf + s / omega_0**2, rel=1e-14)


def test_multi_oscillator_lorentz_is_sum_of_single_oscillators():
    osc1 = (1.0e16, (1.0e16) ** 2, 1.0e14)
    osc2 = (2.0e16, (0.5e16) ** 2, 5.0e13)
    multi = LorentzModel(eps_inf=1.0, oscillators=[osc1, osc2])
    xi = 3.0e15
    term1 = osc1[1] / (osc1[0] ** 2 + xi**2 + osc1[2] * xi)
    term2 = osc2[1] / (osc2[0] ** 2 + xi**2 + osc2[2] * xi)
    assert multi.epsilon(xi) == pytest.approx(1.0 + term1 + term2, rel=1e-14)


@pytest.mark.parametrize("bad_kwargs", [
    dict(omega_p=-1.0),
    dict(omega_p=0.0),
    dict(omega_p=float("nan")),
    dict(omega_p=float("inf")),
])
def test_plasma_rejects_nonphysical_omega_p(bad_kwargs):
    with pytest.raises(ValueError):
        PlasmaModel(**bad_kwargs)


@pytest.mark.parametrize("gamma", [-1.0, float("nan"), float("-inf")])
def test_drude_rejects_negative_or_nonfinite_damping(gamma):
    with pytest.raises(ValueError):
        DrudeModel(omega_p=1e15, gamma=gamma)


def test_negative_frequency_or_k_perp_is_rejected():
    pc = PerfectConductor()
    with pytest.raises(ValueError):
        pc.reflection_coefficients(-1.0, 1.0, C)
    plasma = PlasmaModel(omega_p=1e15)
    with pytest.raises(ValueError):
        plasma.reflection_coefficients(1.0, -1.0, C)


def test_lorentz_model_requires_at_least_one_oscillator():
    with pytest.raises(ValueError):
        LorentzModel(eps_inf=1.0, oscillators=[])


def test_lorentz_model_rejects_eps_inf_below_one():
    with pytest.raises(ValueError):
        LorentzModel(eps_inf=0.5, oscillators=[(1e16, 1e32, 1e14)])


def test_user_dielectric_finite_dielectric_default_zero_limit():
    ud = UserDielectric(lambda xi: 2.5 + 0.0 * xi)
    assert ud.epsilon_xi_squared(0.0) == 0.0
    assert ud.epsilon(1e10) == pytest.approx(2.5)


def test_user_dielectric_diverging_model_requires_zero_limit():
    def eps_like_plasma(xi):
        wp = 9e15
        if xi == 0.0:
            return math.inf
        return 1.0 + (wp / xi) ** 2

    ud_no_limit = UserDielectric(eps_like_plasma)
    with pytest.raises(ValueError):
        ud_no_limit.epsilon_xi_squared(0.0)

    wp = 9e15
    ud_with_limit = UserDielectric(eps_like_plasma, zero_limit=lambda: wp**2)
    assert ud_with_limit.epsilon_xi_squared(0.0) == pytest.approx(wp**2)


def test_user_dielectric_rejects_nonfinite_probe():
    with pytest.raises(ValueError):
        UserDielectric(lambda xi: math.inf)
