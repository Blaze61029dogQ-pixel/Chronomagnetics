"""Regression tests for zero_point_energy: analytic identities and limits.

These tests deliberately avoid re-implementing the formulas under test --
they check scaling laws, signs, and cross-relations that must hold for any
correct implementation, plus that the report script itself runs clean.
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from zero_point_energy import casimir, modes, resonators, stress_tensor, thermal
from zero_point_energy import report as zpe_report

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_casimir_pressure_is_attractive():
    assert casimir.plate_pressure(100e-9) < 0


def test_casimir_pressure_scales_as_inverse_fourth_power_of_gap():
    # Standard Casimir result: P(a) ~ -pi^2 hbar c / (240 a^4), so halving the
    # gap must increase the magnitude by exactly 2^4 = 16, independent of the
    # precise prefactor.
    p_near = casimir.plate_pressure(100e-9)
    p_far = casimir.plate_pressure(200e-9)
    assert math.isclose(p_near / p_far, 16.0, rel_tol=1e-3)


def test_proca_is_three_times_scalar_at_an_independent_operating_point():
    # Same D32 identity as report.py, but at different (k_c, mass) values so
    # this isn't just re-running the report's own hard-coded numbers.
    k_c, mass = 2.0e17, 9.1093837015e-31 * 250.0
    scalar_rho = modes.zpe_density_massive_exact(k_c, mass, g=1.0)
    proca_rho = modes.proca_zpe_density_exact(k_c, mass)
    assert math.isclose(proca_rho / scalar_rho, 3.0, rel_tol=1e-12)


def test_massive_asymptotic_converges_to_exact_for_large_cutoff():
    from zero_point_energy.constants import C_LIGHT, HBAR
    electron_mass = 9.1093837015e-31
    a_m = electron_mass * C_LIGHT / HBAR
    k_c_large = 5.0e5 * a_m
    exact = modes.zpe_density_massive_exact(k_c_large, electron_mass)
    asymptotic = modes.zpe_density_massive_asymptotic(k_c_large, electron_mass)
    assert math.isclose(asymptotic, exact, rel_tol=1e-8)


def test_lc_zero_point_identities_at_an_independent_operating_point():
    omega0 = 2 * math.pi * 1.0e9
    capacitance = 5.0e-13
    inductance = 1.0 / (capacitance * omega0**2)
    v_zpf, i_zpf, phi_zpf, q_zpf = resonators.lc_zero_point(omega0, capacitance, inductance)
    assert math.isclose(v_zpf, q_zpf / capacitance, rel_tol=1e-9)
    assert math.isclose(v_zpf, omega0 * phi_zpf, rel_tol=1e-9)
    assert math.isclose(i_zpf, phi_zpf / inductance, rel_tol=1e-9)
    assert math.isclose(i_zpf, omega0 * q_zpf, rel_tol=1e-9)


def test_hawking_temperature_is_inversely_proportional_to_mass():
    m = 1.0e30
    t1 = thermal.hawking_temperature(m)
    t2 = thermal.hawking_temperature(2 * m)
    assert math.isclose(t1 / t2, 2.0, rel_tol=1e-9)


def test_schwinger_critical_field_is_positive_and_the_right_order_of_magnitude():
    e_s = thermal.schwinger_critical_field(9.1093837015e-31, 1.602176634e-19)
    assert e_s > 0
    assert 1e18 < e_s < 1e19


def test_vacuum_equation_of_state_sign():
    assert stress_tensor.vacuum_pressure(1.0) == -1.0
    assert stress_tensor.vacuum_pressure(-3.5) == 3.5


def test_report_main_runs_without_raising():
    zpe_report.main()


def test_report_subprocess_exits_zero():
    result = subprocess.run(
        [sys.executable, "-m", "zero_point_energy.report"],
        capture_output=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr.decode()
