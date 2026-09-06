"""Tests for zero_point_energy.dce_solver: numerical Bogoliubov solver for a
parametrically driven quantum harmonic mode."""
import math

import pytest

from zero_point_energy.dce_solver import (
    bogoliubov_coefficients,
    energy_ledger,
    resonant_drive_frequency,
    smooth_ramp_omega,
    windowed_sinusoidal_omega,
)
OMEGA0 = 2 * math.pi * 5.0e9  # 5 GHz mode, representative of a superconducting circuit


def _resonant_pulse(epsilon: float, n_periods: float, detuning: float = 0.0):
    period = 2 * math.pi / OMEGA0
    duration = n_periods * period
    drive = resonant_drive_frequency(OMEGA0, detuning=detuning)
    return windowed_sinusoidal_omega(OMEGA0, epsilon, drive, duration), duration


# --- 1: constant omega(t) -> beta = 0 within numerical tolerance -----------

def test_constant_frequency_gives_zero_beta():
    omega_func = lambda t: OMEGA0
    result = bogoliubov_coefficients(omega_func, 0.0, 1e-8, omega_initial=OMEGA0, omega_final=OMEGA0)
    assert abs(result.beta) < 1e-10
    assert result.particle_number < 1e-20
    assert result.wronskian_error < 1e-8


# --- 2: adiabatically slow modulation -> excitation approaches zero --------

def test_adiabatic_ramp_suppresses_excitation_as_ramp_slows():
    """Standard adiabatic-theorem test (Birrell & Davies-style sudden vs.
    adiabatic frequency change): a smooth, monotonic, non-periodic ramp
    from omega_i to omega_f produces less particle production the more
    slowly it is performed -- a fundamentally different scenario from a
    resonant periodic drive (see smooth_ramp_omega's docstring)."""
    omega_f = 2 * math.pi * 7.0e9
    period = 2 * math.pi / OMEGA0
    ns = []
    for n_periods in (1, 10, 100, 1000):
        ramp_duration = n_periods * period
        omega_func = smooth_ramp_omega(OMEGA0, omega_f, ramp_start=0.0, ramp_duration=ramp_duration)
        result = bogoliubov_coefficients(
            omega_func, -0.1 * ramp_duration, 1.2 * ramp_duration,
            omega_initial=OMEGA0, omega_final=omega_f,
        )
        ns.append(result.particle_number)
    assert ns == sorted(ns, reverse=True)  # monotonically decreasing
    assert ns[-1] < 1e-6 * ns[0]  # four orders of ramp slowdown suppresses N sharply
    assert ns[-1] < 1e-10


# --- 3: weak resonant modulation agrees with perturbative behavior ---------

def test_weak_resonant_modulation_matches_perturbative_growth_rate():
    """Undamped degenerate parametric resonance (D7 Route B in the ZPE
    reference document): squeezing parameter r ~= epsilon*omega0*t/4,
    photon number N ~= sinh^2(r). This is the coherent-growth regime (no
    cavity loss), distinct from dynamical_casimir.pair_production_rate,
    which models the Q-limited *steady-state* rate of a damped/driven
    cavity -- a different physical regime not applicable to this undamped
    comparison (that function is exercised on its own terms in
    tests/test_dynamical_casimir.py-equivalent checks elsewhere)."""
    epsilon = 0.01
    n_periods = 5  # short enough to stay in the perturbative (small-N) regime
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    result = bogoliubov_coefficients(omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0)

    r = epsilon * OMEGA0 * duration / 4.0
    predicted_n = math.sinh(r) ** 2

    assert result.particle_number == pytest.approx(predicted_n, rel=0.5)
    # sanity: both are small numbers in this weak/short regime
    assert result.particle_number < 1.0


# --- 4: canonical (Wronskian) identity |alpha|^2 - |beta|^2 = 1 ------------

def test_canonical_identity_holds_for_undamped_evolution():
    epsilon = 0.05
    n_periods = 30
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    result = bogoliubov_coefficients(omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0)
    assert result.wronskian_error < 1e-8
    assert abs(abs(result.alpha) ** 2 - abs(result.beta) ** 2 - 1.0) < 1e-6 * max(result.particle_number, 1.0)


def test_canonical_identity_not_asserted_for_damped_evolution():
    """Damping breaks unitarity by construction; wronskian_error is still
    reported but is not expected to be small -- this test documents that
    fact rather than treating a large residual there as a failure."""
    epsilon = 0.05
    n_periods = 30
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    result = bogoliubov_coefficients(
        omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0, gamma=0.02 * OMEGA0
    )
    assert result.integration_success
    assert math.isfinite(result.wronskian_error)


# --- 5: time-step/tolerance convergence -------------------------------------

def test_particle_number_converges_under_tighter_tolerance():
    epsilon = 0.05
    n_periods = 30
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    coarse = bogoliubov_coefficients(
        omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0, rtol=1e-7, atol=1e-9
    )
    fine = bogoliubov_coefficients(
        omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0, rtol=1e-12, atol=1e-14
    )
    finer = bogoliubov_coefficients(
        omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0, rtol=1e-13, atol=1e-15
    )
    # tighter tolerance should move the answer less (converging), not more
    assert abs(fine.particle_number - finer.particle_number) < abs(coarse.particle_number - fine.particle_number)
    assert fine.wronskian_error < coarse.wronskian_error


# --- 6: detuning suppresses resonant production -----------------------------

def test_detuning_suppresses_production():
    epsilon = 0.01
    n_periods = 30
    omega_func_res, duration = _resonant_pulse(epsilon, n_periods)
    omega_func_det, _ = _resonant_pulse(epsilon, n_periods, detuning=0.5 * OMEGA0)

    n_resonant = bogoliubov_coefficients(
        omega_func_res, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0
    ).particle_number
    n_detuned = bogoliubov_coefficients(
        omega_func_det, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0
    ).particle_number
    assert n_detuned < 1e-6 * n_resonant


# --- 7: zero modulation amplitude gives zero production ---------------------

def test_zero_modulation_amplitude_gives_zero_production():
    omega_func, duration = _resonant_pulse(epsilon=0.0, n_periods=30)
    result = bogoliubov_coefficients(omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0)
    assert result.particle_number < 1e-20


# --- 8: drive-energy ledger closes numerically ------------------------------

def _omega_dot_windowed_sinusoidal(t, omega0, epsilon, drive, duration):
    if not (0.0 <= t <= duration):
        return 0.0
    window = math.sin(math.pi * t / duration) ** 2
    window_dot = 2 * math.sin(math.pi * t / duration) * math.cos(math.pi * t / duration) * (math.pi / duration)
    return omega0 * epsilon * (window_dot * math.cos(drive * t) - window * drive * math.sin(drive * t))


def test_energy_ledger_closes_for_undamped_evolution():
    epsilon = 0.01
    n_periods = 30
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    drive = resonant_drive_frequency(OMEGA0)

    def omega_dot_func(t):
        return _omega_dot_windowed_sinusoidal(t, OMEGA0, epsilon, drive, duration)

    ledger = energy_ledger(
        omega_func, omega_dot_func, 0.0, duration,
        omega_initial=OMEGA0, omega_final=OMEGA0, n_quadrature_points=20000,
    )
    assert ledger.dissipated_energy == 0.0
    relative_error = ledger.ledger_error / abs(ledger.delta_mode_energy)
    assert relative_error < 1e-6


def test_energy_ledger_closes_for_damped_evolution():
    epsilon = 0.01
    n_periods = 30
    omega_func, duration = _resonant_pulse(epsilon, n_periods)
    drive = resonant_drive_frequency(OMEGA0)
    gamma = 0.02 * OMEGA0

    def omega_dot_func(t):
        return _omega_dot_windowed_sinusoidal(t, OMEGA0, epsilon, drive, duration)

    ledger = energy_ledger(
        omega_func, omega_dot_func, 0.0, duration, gamma=gamma,
        omega_initial=OMEGA0, omega_final=OMEGA0, n_quadrature_points=20000,
    )
    assert ledger.dissipated_energy > 0.0
    relative_error = ledger.ledger_error / abs(ledger.delta_mode_energy)
    assert relative_error < 1e-5


# --- 9: no NaNs or silent solver failures ------------------------------------

def test_no_nans_across_a_parameter_sweep():
    for epsilon in (0.0, 0.001, 0.05, 0.2):
        for n_periods in (1, 10, 50):
            omega_func, duration = _resonant_pulse(epsilon, n_periods)
            result = bogoliubov_coefficients(
                omega_func, 0.0, duration, omega_initial=OMEGA0, omega_final=OMEGA0
            )
            assert result.integration_success
            assert math.isfinite(result.particle_number)
            assert math.isfinite(result.wronskian_error)
            assert math.isfinite(abs(result.alpha))
            assert math.isfinite(abs(result.beta))


def test_non_constant_region_is_rejected_rather_than_silently_wrong():
    omega_func = lambda t: OMEGA0 * (1.0 + 0.5 * math.sin(t))
    with pytest.raises(ValueError):
        bogoliubov_coefficients(omega_func, 0.0, 1.0, omega_initial=OMEGA0, omega_final=OMEGA0)


def test_negative_damping_is_rejected():
    omega_func = lambda t: OMEGA0
    with pytest.raises(ValueError):
        bogoliubov_coefficients(omega_func, 0.0, 1e-8, omega_initial=OMEGA0, omega_final=OMEGA0, gamma=-1.0)


def test_final_time_must_exceed_initial_time():
    omega_func = lambda t: OMEGA0
    with pytest.raises(ValueError):
        bogoliubov_coefficients(omega_func, 1.0, 0.5, omega_initial=OMEGA0, omega_final=OMEGA0)
