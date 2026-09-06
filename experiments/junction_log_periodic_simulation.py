#!/usr/bin/env python3
"""BLIND TEST: does log-periodic structure emerge from RCSJ junction dynamics?

Objective: DERIVE (not fit) whether the physical observable of a 4-junction
resistively-and-capacitively-shunted-junction (RCSJ) network exhibits
log-periodic modulation at the Chronometrics-predicted angular frequency
``omega_LOG = 2*pi / ln(lambda_Delta)`` (``chronometrics.constants.OMEGA_DELTA``).

This is a FALSIFIABLE test with three possible outcomes, not two:

- DETECTED     -- a clear dominant spectral peak in log-time matches
                  omega_LOG within tolerance.
- NOT DETECTED -- a clear dominant spectral peak exists but does not match
                  omega_LOG. This is a genuine, reportable negative result.
- INCONCLUSIVE -- no clear dominant peak exists at all (the observable's
                  spectrum lacks the structure needed to say anything).

Why this file is separate from experiments/synthetic_log_periodic_control.py
------------------------------------------------------------------------------
An earlier version of this experiment (recovered from the repository's
invalid ``.github/workflows/blank.yml``, where it had been mistakenly
stored as a GitHub Actions workflow file) computed a *prescribed*
observable ``kappa_cm(t) = |sin(omega_LOG * ln(t/t0))|`` -- i.e. it baked
``omega_LOG`` directly into the "physical" signal it then claimed to
detect ``omega_LOG`` in. That is circular: recovering an injected
frequency from a signal you constructed using that frequency is not
evidence of emergence from junction dynamics.

This file fixes that by construction: the pipeline below is

    RCSJ junction equations
    -> simulated phase/velocity trajectories theta_i(t), theta_dot_i(t)
    -> physical observable (Kuramoto-style phase-coherence order parameter
       r(t) = |mean_i exp(i*theta_i(t))|, plus the mean gate phase)
    -> log-time coordinate u = ln((t+t_c)/t0), t0 a PHYSICAL timescale
       (a multiple of the plasma period) with no dependence on lambda_Delta
    -> linear detrending
    -> blind FFT spectrum (experiments.log_periodic_utils.recover_dominant_frequency,
       which never receives omega_LOG)
    -> recovered peak
    -> ONLY NOW is the recovered peak compared against omega_LOG.

Nowhere before the final comparison does ``lambda_Delta``, ``omega_LOG``, or
any Chronometrics phase function appear in the RCSJ equations or in the
observable construction.

Run with:

    python3 -m experiments.junction_log_periodic_simulation
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from chronometrics.constants import LAMBDA_DELTA, LN_LAMBDA_DELTA, OMEGA_DELTA
from experiments.log_periodic_utils import (
    DETECTED,
    INCONCLUSIVE,
    NOT_DETECTED,
    DominantPeak,
    classify_detection,
    detrend_linear,
    recover_dominant_frequency,
    resample_uniform,
)

# ---------------------------------------------------------------------------
# SECTION 1: Junction network specification (NO free parameters tuned to any
# log-periodic target -- these are the same K_4-complete-graph coupling
# weights used throughout this project's junction-network studies).
# ---------------------------------------------------------------------------
_COUPLING_WEIGHTS = np.array([58, 59, 46, 55, 58, 39], dtype=np.float64)


def build_laplacian(weights: np.ndarray = _COUPLING_WEIGHTS) -> np.ndarray:
    """4-node complete-graph weighted Laplacian from 6 edge weights."""
    W = np.zeros((4, 4))
    W[0, 1] = W[1, 0] = weights[0]
    W[0, 2] = W[2, 0] = weights[1]
    W[0, 3] = W[3, 0] = weights[2]
    W[1, 2] = W[2, 1] = weights[3]
    W[1, 3] = W[3, 1] = weights[4]
    W[2, 3] = W[3, 2] = weights[5]
    return np.diag(W.sum(axis=1)) - W


# ---------------------------------------------------------------------------
# SECTION 2: Physical parameters (typical superconducting Josephson-junction
# values; independent of any Chronometrics quantity).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class JunctionParams:
    phi_0: float = 2.067833848e-15   # Wb, flux quantum
    capacitance: float = 1.0e-12     # F
    resistance: float = 100.0        # Ohm
    critical_current: float = 10.0e-6   # A
    coupling_current: float = 1.0e-6    # A (weak inter-junction coupling)
    i_dc_fraction: float = 0.5           # I_dc = fraction * I_c
    i_ac_fraction: float = 0.1           # I_ac = fraction * I_c
    drive_fraction: float = 0.5          # Omega_drive = fraction * omega_p

    @property
    def gamma(self) -> float:
        """Damping rate Gamma = 1/(R*C)."""
        return 1.0 / (self.resistance * self.capacitance)

    @property
    def omega_p_sq(self) -> float:
        """Plasma angular frequency squared, omega_p^2 = 2*pi*I_c/(Phi_0*C)."""
        return (2 * np.pi * self.critical_current) / (self.phi_0 * self.capacitance)

    @property
    def omega_p(self) -> float:
        return float(np.sqrt(self.omega_p_sq))

    @property
    def epsilon(self) -> float:
        """Inter-junction coupling strength, epsilon = 2*pi*I_k/(Phi_0*C)."""
        return (2 * np.pi * self.coupling_current) / (self.phi_0 * self.capacitance)

    @property
    def i_dc(self) -> float:
        return self.i_dc_fraction * self.critical_current

    @property
    def i_ac(self) -> float:
        return self.i_ac_fraction * self.critical_current

    @property
    def drive_omega(self) -> float:
        return self.drive_fraction * self.omega_p


# ---------------------------------------------------------------------------
# SECTION 3: RCSJ dynamics (coupled ODEs) -- no Chronometrics quantities
# appear anywhere in this right-hand side.
# ---------------------------------------------------------------------------
def rcsj_network_rhs(t: float, y: np.ndarray, L: np.ndarray, p: JunctionParams) -> np.ndarray:
    """Coupled RCSJ equations for an N-junction network.

    State vector y = [theta_1..theta_N, theta_dot_1..theta_dot_N].
    theta_ddot_i = -Gamma*theta_dot_i - omega_p^2*sin(theta_i)
                   - epsilon*sum_j L_ij*sin(theta_i - theta_j) + S_i(t)
    """
    n = L.shape[0]
    theta = y[:n]
    theta_dot = y[n:]

    drive = (2 * np.pi / (p.phi_0 * p.capacitance)) * (p.i_dc + p.i_ac * np.cos(p.drive_omega * t))
    drive = np.full(n, drive)

    coupling = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                coupling[i] += L[i, j] * np.sin(theta[i] - theta[j])

    theta_ddot = -p.gamma * theta_dot - p.omega_p_sq * np.sin(theta) - p.epsilon * coupling + drive
    return np.concatenate([theta_dot, theta_ddot])


@dataclass(frozen=True)
class JunctionSimulation:
    t: np.ndarray
    theta: np.ndarray        # shape (N, len(t))
    theta_dot: np.ndarray    # shape (N, len(t))
    params: JunctionParams


def simulate(
    n_plasma_periods: float = 100.0,
    n_points: int = 10_000,
    params: JunctionParams | None = None,
    laplacian: np.ndarray | None = None,
    theta_init: np.ndarray | None = None,
) -> JunctionSimulation:
    """Integrate the RCSJ network and return raw phase/velocity trajectories.

    ``n_plasma_periods`` and ``n_points`` control run length/resolution only
    -- neither depends on lambda_Delta or omega_LOG.
    """
    p = params or JunctionParams()
    L = build_laplacian() if laplacian is None else laplacian
    n = L.shape[0]

    t_plasma = 2 * np.pi / p.omega_p
    t_max = t_plasma * n_plasma_periods
    t_eval = np.linspace(0, t_max, n_points)

    y0 = np.concatenate([
        theta_init if theta_init is not None else np.array([0.01, 0.02, -0.01, 0.00][:n]),
        np.zeros(n),
    ])

    sol = solve_ivp(
        rcsj_network_rhs, (0, t_max), y0, t_eval=t_eval, args=(L, p),
        method="LSODA", rtol=1e-8, atol=1e-10,
    )
    if not sol.success:
        raise RuntimeError(f"RCSJ integration failed: {sol.message}")

    return JunctionSimulation(t=sol.t, theta=sol.y[:n, :], theta_dot=sol.y[n:, :], params=p)


# ---------------------------------------------------------------------------
# SECTION 4: Physical observable -- a genuine function of the simulated
# phases only. No Chronometrics quantity is used to construct this signal.
# ---------------------------------------------------------------------------
def order_parameter(theta: np.ndarray) -> np.ndarray:
    """Kuramoto-style phase-coherence order parameter r(t) = |mean_i exp(i*theta_i(t))|.

    This is a standard observable for coupled-oscillator networks -- it
    measures phase synchronization, bounded in [0, 1], and depends only on
    the simulated junction phases.
    """
    return np.abs(np.mean(np.exp(1j * theta), axis=0))


def mean_gate_phase(theta: np.ndarray) -> np.ndarray:
    """theta_gate(t) = mean_i theta_i(t), an alternative physical observable."""
    return np.mean(theta, axis=0)


# ---------------------------------------------------------------------------
# SECTION 5: Blind log-time analysis and classification.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BlindDetectionResult:
    peak: DominantPeak
    classification: str
    target_angular_frequency: float
    relative_mismatch: float


def run_blind_detection(
    t: np.ndarray,
    observable: np.ndarray,
    t0: float,
    t_c: float = 1e-12,
    target_angular_frequency: float = float(OMEGA_DELTA),
) -> BlindDetectionResult:
    """Log-time transform, detrend, and blindly recover the dominant peak.

    ``target_angular_frequency`` is used ONLY in the final classification
    step, after ``recover_dominant_frequency`` (which never receives it) has
    already produced its peak -- see the module docstring.
    """
    u = np.log((t + t_c) / t0)
    u_uniform, signal_uniform = resample_uniform(u, observable)
    detrended = detrend_linear(u_uniform, signal_uniform)

    peak = recover_dominant_frequency(u_uniform, detrended)  # BLIND: no target passed in

    classification = classify_detection(peak.angular_frequency, target_angular_frequency, peak.spectral_purity)
    rel_mismatch = (
        abs(peak.angular_frequency - target_angular_frequency) / abs(target_angular_frequency)
        if target_angular_frequency
        else float("nan")
    )
    return BlindDetectionResult(
        peak=peak,
        classification=classification,
        target_angular_frequency=target_angular_frequency,
        relative_mismatch=rel_mismatch,
    )


def main() -> None:
    print("=" * 78)
    print("BLIND TEST: junction network -> log-periodic modulation?")
    print("=" * 78)
    print()
    print(f"Chronometrics target: lambda_Delta = {LAMBDA_DELTA} = {float(LAMBDA_DELTA):.10f}")
    print(f"                       ln(lambda_Delta) = {float(LN_LAMBDA_DELTA):.10f}")
    print(f"                       omega_LOG = 2*pi/ln(lambda_Delta) = {float(OMEGA_DELTA):.10f}")
    print("(This target is used ONLY for the final comparison below, never fed")
    print(" into the RCSJ equations or the observable construction.)")
    print()

    sim = simulate()
    t_plasma = 2 * np.pi / sim.params.omega_p
    t0 = t_plasma * 10.0  # a physical timescale; unrelated to lambda_Delta

    r_t = order_parameter(sim.theta)
    gate_phase = mean_gate_phase(sim.theta)

    print(f"Simulated {len(sim.t)} samples over {sim.t[-1] / t_plasma:.1f} plasma periods.")
    print(f"Order parameter r(t) range: [{r_t.min():.6f}, {r_t.max():.6f}]")
    print(f"Mean gate phase range     : [{gate_phase.min():.6f}, {gate_phase.max():.6f}] rad")
    print()

    result = run_blind_detection(sim.t, r_t, t0)

    print("-- Blind detection result (physical observable: order parameter) --")
    print(f"   recovered angular frequency : {result.peak.angular_frequency:.10f}")
    print(f"   recovered cycle frequency   : {result.peak.frequency_cycles:.10f}")
    print(f"   target angular frequency    : {result.target_angular_frequency:.10f}")
    print(f"   relative mismatch           : {result.relative_mismatch:.4%}")
    print(f"   spectral purity             : {result.peak.spectral_purity:.4f}")
    print(f"   CLASSIFICATION              : {result.classification}")
    print()

    if result.classification == DETECTED:
        print("Log-periodic modulation at the Chronometrics target frequency was")
        print("recovered blindly from RCSJ junction dynamics.")
    elif result.classification == NOT_DETECTED:
        print("A dominant spectral peak exists but does NOT match the Chronometrics")
        print("target frequency. This is a genuine null result: junction dynamics, as")
        print("modeled here, do not produce the predicted log-periodic modulation.")
    elif result.classification == INCONCLUSIVE:
        print("No clear dominant spectral peak was found (spectral purity too low).")
        print("This test is INCONCLUSIVE, not a detection.")
    else:
        raise RuntimeError(f"unrecognized classification: {result.classification!r}")

    print()
    print("This result is reported as-is. It is not tuned, filtered, or adjusted")
    print("to match the target -- see experiments/synthetic_log_periodic_control.py")
    print("for the (separate, clearly labeled) methods-validation control.")


if __name__ == "__main__":
    main()
