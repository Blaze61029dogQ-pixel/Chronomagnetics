"""Regression tests for d067_art_v1: cross-relations and limiting behavior."""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from d067_art_v1 import electromechanical as em
from d067_art_v1 import photonics
from d067_art_v1 import report as d067_report
from d067_art_v1.constants import C_LIGHT, H_PLANCK, K_CD

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_quality_factor_is_frequency_over_bandwidth():
    assert math.isclose(em.quality_factor(100.0, 10.0), 10.0, rel_tol=1e-12)


def test_voltage_from_power_round_trips_through_load_power():
    power, resistance = 1.0e-4, 5000.0
    voltage = em.voltage_from_power(power, resistance)
    assert math.isclose(em.load_power(complex(voltage), resistance), power, rel_tol=1e-9)


def test_robustness_ratio_is_worst_over_nominal():
    assert em.robustness_ratio(1.0, 4.0) == 0.25
    assert em.robustness_ratio(4.0, 4.0) == 1.0


def test_scaled_power_is_quadratic_in_acceleration_ratio():
    nominal = 1.0e-5
    assert math.isclose(em.scaled_power(nominal, 2.0), nominal * 4.0, rel_tol=1e-12)
    assert math.isclose(em.scaled_power(nominal, 0.5), nominal * 0.25, rel_tol=1e-12)


def test_scaled_voltage_is_linear_in_acceleration_ratio():
    nominal = 1.0
    assert math.isclose(em.scaled_voltage(nominal, 3.0), 3.0, rel_tol=1e-12)


def test_coupling_theta_physical_closure_round_trip():
    kappa_eff_sq, k_eff, capacitance = 1.2e-3, 5.0e5, 1.6e-7
    theta = em.coupling_theta_from_physical_closure(kappa_eff_sq, k_eff, capacitance)
    k_eff_recovered = em.effective_stiffness_from_theta(theta, kappa_eff_sq, capacitance)
    assert math.isclose(k_eff_recovered, k_eff, rel_tol=1e-9)


def test_photon_energy_matches_planck_einstein_relation():
    wavelength = 500e-9
    assert math.isclose(
        photonics.photon_energy(wavelength), H_PLANCK * C_LIGHT / wavelength, rel_tol=1e-12
    )


def test_photon_rate_is_power_divided_by_photon_energy():
    power, wavelength = 1.0e-4, 500e-9
    expected = power / (H_PLANCK * C_LIGHT / wavelength)
    assert math.isclose(photonics.photon_rate(power, wavelength), expected, rel_tol=1e-12)


def test_idealized_lumens_are_linear_in_power_with_slope_k_cd():
    p1, p2 = 1.0e-5, 3.0e-5
    l1 = photonics.idealized_photopic_lumens(p1)
    l2 = photonics.idealized_photopic_lumens(p2)
    assert math.isclose(l2 / l1, p2 / p1, rel_tol=1e-12)
    assert math.isclose(l1 / p1, K_CD, rel_tol=1e-12)


def test_report_main_runs_without_raising():
    d067_report.main()


def test_report_subprocess_exits_zero():
    result = subprocess.run(
        [sys.executable, "-m", "d067_art_v1.report"],
        capture_output=True, cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr.decode()
