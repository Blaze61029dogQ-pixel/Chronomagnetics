"""Blind log-periodic detection tests (Sections 10-12).

Covers the FFT unit-conversion identities, the sin-vs-abs(sin) period
identities, and the blind/synthetic separation: the physical RCSJ
simulation must never be fed its own comparison target, while the
synthetic control is explicitly allowed to (and is labeled as such).
"""
from __future__ import annotations

import math

import numpy as np

from chronometrics.constants import OMEGA_DELTA
from experiments import log_periodic_utils as lpu
from experiments.junction_log_periodic_simulation import (
    order_parameter,
    run_blind_detection,
    simulate,
)
from experiments.synthetic_log_periodic_control import make_injected_signal


# ---------------------------------------------------------------------------
# Frequency-unit identities (Section 11)
# ---------------------------------------------------------------------------
def test_angular_frequency_from_cycles_is_2pi_times_f():
    f = 3.7
    omega = lpu.angular_frequency_from_cycles(f)
    assert math.isclose(omega, 2 * math.pi * f, rel_tol=1e-12)


def test_cycles_from_angular_frequency_is_the_inverse_conversion():
    omega = 23.4
    f = lpu.cycles_from_angular_frequency(omega)
    assert math.isclose(lpu.angular_frequency_from_cycles(f), omega, rel_tol=1e-12)


def test_period_for_sine_is_2pi_over_omega():
    omega = 5.0
    assert math.isclose(lpu.period_for_sine(omega), 2 * math.pi / omega, rel_tol=1e-12)


def test_period_for_abs_sine_is_pi_over_omega():
    omega = 5.0
    assert math.isclose(lpu.period_for_abs_sine(omega), math.pi / omega, rel_tol=1e-12)


def test_abs_sine_period_is_half_the_plain_sine_period():
    omega = 9.0
    assert math.isclose(lpu.period_for_abs_sine(omega), lpu.period_for_sine(omega) / 2, rel_tol=1e-12)


def test_angular_frequency_for_period_inverses_are_consistent():
    delta_u = 0.73
    omega_sine = lpu.angular_frequency_for_period_sine(delta_u)
    omega_abs = lpu.angular_frequency_for_period_abs_sine(delta_u)
    assert math.isclose(lpu.period_for_sine(omega_sine), delta_u, rel_tol=1e-9)
    assert math.isclose(lpu.period_for_abs_sine(omega_abs), delta_u, rel_tol=1e-9)
    assert math.isclose(omega_sine, 2 * omega_abs, rel_tol=1e-12)


def test_zero_crossing_spacing_matches_abs_sine_period_numerically():
    # Directly measures the period of abs(sin(omega*u)) from its zero
    # crossings and checks it against pi/omega, independent of the FFT path.
    omega = 6.0
    u = np.linspace(0, 20, 200_000)
    signal = np.abs(np.sin(omega * u))
    # abs(sin) touches zero at u = n*pi/omega; find near-zero minima spacing.
    crossings = u[np.where(np.diff(np.sign(np.sin(omega * u))))[0]]
    spacings = np.diff(crossings)
    assert np.allclose(spacings, math.pi / omega, atol=1e-3)


# ---------------------------------------------------------------------------
# Blind detector scenarios (Section 12)
# ---------------------------------------------------------------------------
def _blind_classify(u: np.ndarray, signal: np.ndarray, target_omega: float) -> tuple[str, "lpu.DominantPeak"]:
    u_uniform, sig = lpu.resample_uniform(u, signal)
    detrended = lpu.detrend_linear(u_uniform, sig)
    peak = lpu.recover_dominant_frequency(u_uniform, detrended)
    return lpu.classify_detection(peak.angular_frequency, target_omega, peak.spectral_purity), peak


def test_pure_noise_is_inconclusive():
    rng = np.random.default_rng(42)
    u = np.linspace(0.1, 12, 4096)
    noise = rng.normal(size=u.shape)
    classification, _ = _blind_classify(u, noise, float(OMEGA_DELTA))
    assert classification == lpu.INCONCLUSIVE


def test_single_log_time_sinusoid_is_detected():
    omega = 12.3
    u = np.linspace(0.1, 12, 4096)
    signal = np.sin(omega * u)
    classification, _ = _blind_classify(u, signal, omega)
    assert classification == lpu.DETECTED


def test_absolute_value_sinusoid_detected_only_against_doubled_frequency():
    omega = 8.0
    u = np.linspace(0.1, 12, 4096)
    signal = np.abs(np.sin(omega * u))
    against_omega, _ = _blind_classify(u, signal, omega)
    against_2omega, _ = _blind_classify(u, signal, 2 * omega)
    assert against_omega == lpu.NOT_DETECTED
    assert against_2omega == lpu.DETECTED


def test_known_synthetic_chronometrics_control_is_detected():
    omega = float(OMEGA_DELTA)
    u = np.linspace(0.1, 12, 4096)
    signal = make_injected_signal(u, omega, use_abs=False)
    classification, _ = _blind_classify(u, signal, omega)
    assert classification == lpu.DETECTED


def test_known_wrong_frequency_control_is_not_detected():
    omega_target = float(OMEGA_DELTA)
    omega_wrong = omega_target * 1.9  # not a near-miss; a clearly different frequency
    u = np.linspace(0.1, 12, 4096)
    signal = make_injected_signal(u, omega_wrong, use_abs=False)
    classification, peak = _blind_classify(u, signal, omega_target)
    assert classification == lpu.NOT_DETECTED
    # the detector must recover the WRONG frequency, not silently the target
    assert math.isclose(peak.angular_frequency, omega_wrong, rel_tol=0.05)


def test_rcsj_output_with_no_injected_target_is_reported_honestly():
    """The physical junction simulation never sees omega_LOG until after
    recover_dominant_frequency returns (see junction_log_periodic_simulation
    module docstring). This is a deterministic ODE integration (no RNG), so
    the classification is reproducible; whatever it is, it must be reported
    as-is rather than forced to DETECTED.
    """
    sim = simulate(n_plasma_periods=100.0, n_points=10_000)
    t_plasma = 2 * math.pi / sim.params.omega_p
    r_t = order_parameter(sim.theta)
    result = run_blind_detection(sim.t, r_t, t0=t_plasma * 10.0)
    assert result.classification in (lpu.DETECTED, lpu.NOT_DETECTED, lpu.INCONCLUSIVE)
    # Documented, reproducible outcome of the current reduced-order RCSJ
    # model: it does NOT reproduce the Chronometrics target frequency. If a
    # future change to the physical model makes this DETECTED, that is a
    # genuinely interesting result and this assertion should be revisited
    # deliberately -- not silently loosened.
    assert result.classification == lpu.NOT_DETECTED


def test_frequency_estimate_improves_with_longer_observation_window():
    # FFT frequency resolution is set by the total observation span
    # (~1/span in cycle units), not by sample count at fixed span. A longer
    # window at matched sampling density must not make the estimate worse.
    omega = 10.0
    errors = []
    for u_max in (6.0, 12.0, 24.0):
        n = int(u_max * 400)
        u = np.linspace(0.1, u_max, n)
        signal = np.sin(omega * u)
        classification, peak = _blind_classify(u, signal, omega)
        errors.append(abs(peak.angular_frequency - omega) / omega)
    assert errors[-1] <= errors[0] + 1e-9


def test_synthetic_control_is_labeled_as_such_not_as_emergence():
    from experiments.synthetic_log_periodic_control import run_control

    result = run_control(float(OMEGA_DELTA), omega_inject=float(OMEGA_DELTA), use_abs=False)
    assert result["label"] == lpu.SYNTHETIC_CONTROL
