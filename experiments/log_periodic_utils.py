"""Shared, blind spectral-detection utilities for log-periodic experiments.

This module is the single place where FFT frequency-unit conversions and
peak-classification logic live, so that both the synthetic control
(:mod:`experiments.synthetic_log_periodic_control`) and the physical
junction simulation (:mod:`experiments.junction_log_periodic_simulation`)
run through the exact same analysis pipeline. Neither of those two callers
may see the "target" angular frequency until *after* they have already
called :func:`recover_dominant_frequency` -- see each module's own
docstring for why that separation matters.

Frequency-unit convention
--------------------------
``scipy.fft.fftfreq`` returns a *cycle* frequency (cycles per unit of the
sample spacing), not an angular frequency. For a real sinusoid

    x(u) = sin(omega * u)

the cycle frequency of that sinusoid is ``f = omega / (2*pi)``, so the
angular frequency recovered from an FFT bin must be reconstructed as
``omega = 2*pi*f``. Silently comparing a raw FFT bin frequency against an
angular-frequency target (as in the historical version of this experiment,
recovered from ``.github/workflows/blank.yml`` and preserved for reference
history) is a units bug: it compares cycles/unit against radians/unit,
off by a factor of 2*pi.

Period identities in log-time
------------------------------
For ``x(u) = sin(omega*u)``, the period is ``Delta_u = 2*pi/omega``.

For ``x(u) = abs(sin(omega*u))``, the *absolute value* halves the period
via full-wave rectification, so ``Delta_u = pi/omega`` -- the abs-sine
crosses zero (and hence repeats) twice as often as the plain sine. Both
identities are asserted numerically in
``tests/test_log_periodic_detection.py``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks


def angular_frequency_from_cycles(frequency_cycles: float) -> float:
    """omega = 2*pi*f, converting a cycle frequency to an angular frequency."""
    return 2.0 * math.pi * frequency_cycles


def cycles_from_angular_frequency(angular_frequency: float) -> float:
    """f = omega / (2*pi), the inverse of :func:`angular_frequency_from_cycles`."""
    return angular_frequency / (2.0 * math.pi)


def period_for_sine(angular_frequency: float) -> float:
    """Delta_u = 2*pi/omega, the period of sin(omega*u) in its own coordinate."""
    return 2.0 * math.pi / angular_frequency


def period_for_abs_sine(angular_frequency: float) -> float:
    """Delta_u = pi/omega, the period of abs(sin(omega*u)) (half of the plain sine)."""
    return math.pi / angular_frequency


def angular_frequency_for_period_sine(delta_u: float) -> float:
    """Inverse of :func:`period_for_sine`: omega = 2*pi/Delta_u."""
    return 2.0 * math.pi / delta_u


def angular_frequency_for_period_abs_sine(delta_u: float) -> float:
    """Inverse of :func:`period_for_abs_sine`: omega = pi/Delta_u."""
    return math.pi / delta_u


def detrend_linear(u: np.ndarray, signal: np.ndarray) -> np.ndarray:
    """Remove the best-fit line from ``signal`` over coordinate ``u``.

    A slow linear drift in log-time would otherwise leak power into the
    low-frequency bins of the FFT and can bias peak-finding.
    """
    coeffs = np.polyfit(u, signal, deg=1)
    trend = np.polyval(coeffs, u)
    return signal - trend


@dataclass(frozen=True)
class Spectrum:
    frequency_cycles: np.ndarray       # positive-frequency FFT bins, cycles per unit-u
    angular_frequency: np.ndarray      # same bins, converted to omega = 2*pi*f
    power: np.ndarray                  # |FFT|^2 at each positive-frequency bin


def blind_spectrum(u_uniform: np.ndarray, signal: np.ndarray) -> Spectrum:
    """FFT ``signal`` (already resampled onto a uniform ``u_uniform`` grid).

    Returns positive frequencies only, both as raw FFT cycle frequencies and
    as the corresponding angular frequencies (see module docstring for why
    those two are not interchangeable).
    """
    n = len(u_uniform)
    du = u_uniform[1] - u_uniform[0]
    spectrum = fft(signal)
    freqs_cycles = fftfreq(n, d=du)

    half = n // 2
    frequency_cycles = freqs_cycles[:half]
    power = np.abs(spectrum[:half]) ** 2
    angular_frequency = angular_frequency_from_cycles(frequency_cycles)
    return Spectrum(frequency_cycles=frequency_cycles, angular_frequency=angular_frequency, power=power)


@dataclass(frozen=True)
class DominantPeak:
    index: int
    frequency_cycles: float
    angular_frequency: float
    power: float
    spectral_purity: float             # this peak's power / total AC power (0..1)


def recover_dominant_frequency(u_uniform: np.ndarray, signal: np.ndarray) -> DominantPeak:
    """Blindly recover the dominant non-DC spectral peak of ``signal``.

    This function does not take, and must never be given, the target
    frequency it will later be compared against -- it only sees the
    observable's own samples. Comparison against a target frequency happens
    strictly after this call returns, in the caller.
    """
    spectrum = blind_spectrum(u_uniform, signal)
    ac_power = spectrum.power[1:]  # exclude DC bin
    if ac_power.size == 0 or not np.any(ac_power > 0):
        return DominantPeak(index=0, frequency_cycles=0.0, angular_frequency=0.0, power=0.0, spectral_purity=0.0)

    idx = int(np.argmax(ac_power)) + 1
    total_ac_power = float(np.sum(ac_power))
    purity = float(spectrum.power[idx] / total_ac_power) if total_ac_power > 0 else 0.0
    return DominantPeak(
        index=idx,
        frequency_cycles=float(spectrum.frequency_cycles[idx]),
        angular_frequency=float(spectrum.angular_frequency[idx]),
        power=float(spectrum.power[idx]),
        spectral_purity=purity,
    )


DETECTED = "DETECTED"
NOT_DETECTED = "NOT DETECTED"
INCONCLUSIVE = "INCONCLUSIVE"
SYNTHETIC_CONTROL = "SYNTHETIC CONTROL"


def classify_detection(
    recovered_angular_frequency: float,
    target_angular_frequency: float,
    spectral_purity: float,
    *,
    frequency_rel_tol: float = 0.05,
    purity_threshold: float = 0.3,
) -> str:
    """Classify a blind detection result against a target *after* recovery.

    - INCONCLUSIVE: no clear dominant peak exists (spectral_purity below
      purity_threshold) -- the observable does not have enough spectral
      structure to say anything, regardless of where its weak peak sits.
    - DETECTED: a clear dominant peak exists AND it matches the target
      within frequency_rel_tol.
    - NOT DETECTED: a clear dominant peak exists but it does NOT match the
      target -- a genuine, reportable null/falsification result.
    """
    if spectral_purity < purity_threshold:
        return INCONCLUSIVE
    if target_angular_frequency == 0:
        return NOT_DETECTED
    rel_error = abs(recovered_angular_frequency - target_angular_frequency) / abs(target_angular_frequency)
    return DETECTED if rel_error <= frequency_rel_tol else NOT_DETECTED


def resample_uniform(u: np.ndarray, signal: np.ndarray, n: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Interpolate (u, signal) onto a uniform u-grid, required before FFT."""
    if n is None:
        n = len(u)
    u_uniform = np.linspace(u.min(), u.max(), n)
    signal_uniform = np.interp(u_uniform, u, signal)
    return u_uniform, signal_uniform
