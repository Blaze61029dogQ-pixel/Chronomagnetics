"""Tests for zero_point_energy.resonators: LC and Josephson zero-point
amplitudes."""
import math

import pytest

from zero_point_energy import resonators
from zero_point_energy.constants import HBAR


def test_lc_zero_point_identities_independent_of_module_formulas():
    """Recompute V_zpf, I_zpf from Z=sqrt(L/C) directly and cross-check
    against the module's own (differently-parameterized) output."""
    omega0 = 2 * math.pi * 6.0e9
    capacitance = 2e-13
    inductance = 1.0 / (capacitance * omega0**2)
    impedance = math.sqrt(inductance / capacitance)

    v_zpf, i_zpf, phi_zpf, q_zpf = resonators.lc_zero_point(omega0, capacitance, inductance)

    assert v_zpf == pytest.approx(math.sqrt(HBAR * omega0 / (2 * capacitance)), rel=1e-13)
    assert i_zpf == pytest.approx(math.sqrt(HBAR * omega0 / (2 * inductance)), rel=1e-13)
    assert phi_zpf == pytest.approx(math.sqrt(HBAR * impedance / 2), rel=1e-13)
    assert q_zpf == pytest.approx(math.sqrt(HBAR / (2 * impedance)), rel=1e-13)

    # cross-identities, D59
    assert v_zpf == pytest.approx(q_zpf / capacitance, rel=1e-12)
    assert v_zpf == pytest.approx(omega0 * phi_zpf, rel=1e-12)
    assert i_zpf == pytest.approx(phi_zpf / inductance, rel=1e-12)
    assert i_zpf == pytest.approx(omega0 * q_zpf, rel=1e-12)


def test_lc_zero_point_scales_with_capacitance_and_inductance():
    omega0 = 2 * math.pi * 5.0e9
    c1, l1 = 1e-13, 1 / (1e-13 * omega0**2)
    c2 = 4 * c1
    l2 = 1.0 / (c2 * omega0**2)
    v1, i1, _p1, _q1 = resonators.lc_zero_point(omega0, c1, l1)
    v2, i2, _p2, _q2 = resonators.lc_zero_point(omega0, c2, l2)
    # V_zpf ~ 1/sqrt(C): quadrupling C halves V_zpf
    assert v2 == pytest.approx(v1 / 2, rel=1e-12)


def test_josephson_plasma_frequency_matches_harmonic_oscillator_identity():
    e_j = HBAR * 2 * math.pi * 15e9
    e_c = HBAR * 2 * math.pi * 0.3e9
    omega_p = resonators.josephson_plasma_frequency(e_j, e_c)
    assert omega_p == pytest.approx(math.sqrt(8 * e_j * e_c) / HBAR, rel=1e-13)


def test_josephson_zero_point_values_and_scaling():
    e_j = HBAR * 2 * math.pi * 15e9
    e_c = HBAR * 2 * math.pi * 0.3e9
    phi_zpf, n_zpf = resonators.josephson_zero_point(e_j, e_c)
    assert phi_zpf == pytest.approx((2 * e_c / e_j) ** 0.25, rel=1e-13)
    assert n_zpf == pytest.approx((e_j / (32 * e_c)) ** 0.25, rel=1e-13)
    # deep transmon regime (E_J >> E_C): phi_zpf should be small (phase well localized)
    assert phi_zpf < 1.0
    # phi_zpf shrinks and n_zpf grows as E_J/E_C increases
    phi_zpf_2, n_zpf_2 = resonators.josephson_zero_point(4 * e_j, e_c)
    assert phi_zpf_2 < phi_zpf
    assert n_zpf_2 > n_zpf


def test_josephson_zero_point_matches_transmon_module_convention():
    """resonators.py's phi_zpf/n_zpf must use the same convention as the
    independently-derived asymptotic formula in transmon.py (both quote
    phi_zpf = (2*E_C/E_J)^(1/4))."""
    from zero_point_energy.transmon import asymptotic_energies

    e_c, e_j = 0.2, 20.0  # dimensionless energy units here, consistent within this test
    phi_zpf, _n_zpf = resonators.josephson_zero_point(e_j, e_c)
    assert phi_zpf == pytest.approx((2 * e_c / e_j) ** 0.25, rel=1e-13)
    # sanity: asymptotic_energies uses the same sqrt(8*E_J*E_C) plasma scale
    energies = asymptotic_energies(e_c, e_j, num_levels=2)
    hbar_omega_p_implied = energies[1] - energies[0] + e_c  # undo the m=1 quartic shift's difference from m=0
    assert hbar_omega_p_implied == pytest.approx(math.sqrt(8 * e_j * e_c), rel=1e-10)
