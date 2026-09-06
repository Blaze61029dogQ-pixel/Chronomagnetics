#!/usr/bin/env python3
"""SYNTHETIC CONTROL: verify the blind log-periodic detection pipeline itself.

This script deliberately INJECTS a known log-periodic signal into a
synthetic observable and then runs it through the exact same blind
detection pipeline (:mod:`experiments.log_periodic_utils`) used on the
physical RCSJ junction simulation in
:mod:`experiments.junction_log_periodic_simulation`.

Purpose: this is a methods check, not a physics result. It answers "if a
log-periodic signal at the Chronometrics target frequency really were
present in an observable, would this detection pipeline find it?" -- not
"is such a signal physically present." Every result from this script is
reported and must be labeled SYNTHETIC CONTROL, never as an independent
confirmation of emergence.

Run with:

    python3 -m experiments.synthetic_log_periodic_control
"""
from __future__ import annotations

import numpy as np

from chronometrics.constants import OMEGA_DELTA
from experiments.log_periodic_utils import (
    DETECTED,
    NOT_DETECTED,
    SYNTHETIC_CONTROL,
    classify_detection,
    detrend_linear,
    recover_dominant_frequency,
    resample_uniform,
)


def make_injected_signal(
    u: np.ndarray,
    omega_target: float,
    *,
    use_abs: bool = True,
    noise_amplitude: float = 0.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Construct a synthetic observable with a KNOWN injected frequency.

    This is the one place in the whole log-periodic experiment suite where
    injecting the target frequency directly into the analyzed observable is
    legitimate -- because this file's entire purpose is to be the synthetic
    positive control, not a claim about junction physics.
    """
    signal = np.sin(omega_target * u)
    if use_abs:
        signal = np.abs(signal)
    if noise_amplitude:
        if rng is None:
            rng = np.random.default_rng(0)
        signal = signal + rng.normal(scale=noise_amplitude, size=u.shape)
    return signal


def run_control(
    omega_target: float,
    *,
    omega_inject: float,
    u_span: tuple[float, float] = (0.1, 12.0),
    n_points: int = 4096,
    use_abs: bool = True,
    noise_amplitude: float = 0.0,
    label: str = "",
) -> dict:
    """Inject a known signal and run it through the blind detection pipeline.

    IMPORTANT (see experiments/log_periodic_utils.py module docstring): for
    sin(omega*u) the FFT fundamental sits at omega itself, but for
    abs(sin(omega*u)) the absolute value halves the period (full-wave
    rectification), so the FFT fundamental sits at 2*omega, not omega. The
    "expected recovered frequency" below accounts for that -- it is NOT a
    tolerance fudge, it is the documented abs-sine period identity.
    """
    u = np.linspace(*u_span, n_points)
    signal = make_injected_signal(u, omega_inject, use_abs=use_abs, noise_amplitude=noise_amplitude)
    u_uniform, signal_uniform = resample_uniform(u, signal, n_points)
    detrended = detrend_linear(u_uniform, signal_uniform)
    peak = recover_dominant_frequency(u_uniform, detrended)

    expected_recovered = 2.0 * omega_target if use_abs else omega_target
    classification = classify_detection(peak.angular_frequency, expected_recovered, peak.spectral_purity)

    print(f"-- {label or 'synthetic control'} --")
    print(f"   injected angular frequency        : {omega_inject:.10f}")
    print(f"   target angular frequency          : {omega_target:.10f}")
    if use_abs:
        print(f"   expected FFT peak (abs-sine, 2x)  : {expected_recovered:.10f}")
    print(f"   recovered angular frequency       : {peak.angular_frequency:.10f}")
    print(f"   recovered cycle frequency         : {peak.frequency_cycles:.10f}")
    print(f"   spectral purity                   : {peak.spectral_purity:.4f}")
    print(f"   classification (informative)      : {classification}")
    print(f"   result label                      : {SYNTHETIC_CONTROL}")
    print()
    return {
        "peak": peak,
        "classification": classification,
        "label": SYNTHETIC_CONTROL,
    }


def main() -> None:
    print("=" * 78)
    print("SYNTHETIC LOG-PERIODIC CONTROL -- methods check, NOT a physics result")
    print("=" * 78)
    print(f"Chronometrics target omega_LOG = {OMEGA_DELTA} (from chronometrics.constants)")
    print()

    correct_sine = run_control(
        float(OMEGA_DELTA), omega_inject=float(OMEGA_DELTA), use_abs=False,
        label="positive control: plain sin(omega*u), correct frequency injected",
    )
    if correct_sine["classification"] != DETECTED:
        print("[WARN] positive control failed to recover its own injected frequency; "
              "the detection pipeline itself may be broken.")

    correct_abs = run_control(
        float(OMEGA_DELTA), omega_inject=float(OMEGA_DELTA), use_abs=True,
        label="positive control: abs(sin(omega*u)) -- FFT peak at 2*omega",
    )
    if correct_abs["classification"] != DETECTED:
        print("[WARN] abs-sine positive control failed to recover the expected 2*omega peak; "
              "the abs-sine period identity or the detection pipeline may be broken.")

    wrong = run_control(
        float(OMEGA_DELTA), omega_inject=float(OMEGA_DELTA) * 1.7, use_abs=False,
        label="negative control: wrong frequency injected",
    )
    if wrong["classification"] != NOT_DETECTED:
        print("[WARN] negative control did not correctly reject the wrong frequency.")

    run_control(
        float(OMEGA_DELTA), omega_inject=float(OMEGA_DELTA), use_abs=False,
        noise_amplitude=0.3,
        label="positive control with additive noise",
    )

    print("=" * 78)
    print("These are SYNTHETIC CONTROLS: the injected signal is fabricated by this")
    print("script. They validate the detection pipeline only. They must never be")
    print("described as evidence of log-periodic emergence from junction dynamics --")
    print("see experiments/junction_log_periodic_simulation.py for that (blind) test.")


if __name__ == "__main__":
    main()
