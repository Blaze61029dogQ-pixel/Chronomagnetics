"""Numerical dynamical Casimir engine: Bogoliubov particle production from a
parametrically driven quantum harmonic mode (source: Dodonov, Phys. Scr. 82,
038105 (2010); see REFERENCES.bib). Complements, and does not replace, the
weak-pump/perturbative formulas already in zero_point_energy.dynamical_casimir.

MODEL

A single field mode obeys the classical equation of motion

    q_ddot(t) + omega(t)^2 * q(t) = 0        (undamped, mass = 1 convention)

with the DAMPED extension

    q_ddot(t) + 2*gamma*q_dot(t) + omega(t)^2 * q(t) = 0

as a clearly-labeled effective/open-system addition (gamma > 0 breaks
unitarity by construction -- see CANONICAL IDENTITY below).

The complex classical solution q(t) that starts as the positive-frequency
vacuum mode function of the *initial* constant frequency omega_i,

    q(t0)     = 1 / sqrt(2*omega_i)
    q_dot(t0) = -i * omega_i / sqrt(2*omega_i)

is evolved forward. In the *final* constant-frequency region (omega(t) =
omega_f for t >= some t_f <= final_time), the same solution is re-expressed
in the final-frequency plane-wave basis,

    q(t) = [alpha * exp(-i*omega_f*t) + beta * exp(+i*omega_f*t)] / sqrt(2*omega_f),

which defines the Bogoliubov coefficients alpha, beta by direct linear
matching of q(final_time), q_dot(final_time) against this ansatz (Birrell &
Davies-style mode matching, e.g. as used throughout the DCE literature
reviewed in Dodonov 2010). REQUIRING an actual final constant-frequency
region (checked by `require_constant_regions`) is what makes alpha, beta
meaningful: they are undefined while omega(t) is still changing.

PARTICLE NUMBER: N = |beta|^2 (mean photon number produced in the mode,
starting from vacuum).

CANONICAL IDENTITY: for the undamped (gamma=0) case the evolution is
unitary/symplectic and |alpha|^2 - |beta|^2 = 1 exactly; this module
verifies it to numerical (solver) tolerance and reports the *relative*
residual (normalized by max(|alpha|^2+|beta|^2, 1), since under strong
parametric gain the absolute residual scales with the solver's rtol times
the -- possibly huge -- mode occupation itself) as `wronskian_error`. This
identity is NOT expected to hold once damping is enabled (energy leaves
the mode) -- `wronskian_error` is still reported in that case but is not
asserted anywhere to be small.

ENERGY LEDGER (see also zero_point_energy/dce_solver.py's
`energy_ledger`): using the same normalization, the classical mode energy

    E(t) = (1/2)*|q_dot(t)|^2 + (1/2)*omega(t)^2*|q(t)|^2

equals exactly (1/2)*hbar*omega_i at t0 (the initial vacuum's zero-point
energy) and exactly (N + 1/2)*hbar*omega_f in the final constant region
(derived directly from the alpha/beta ansatz above; the derivation is
straightforward algebra reproduced in this module's tests). Its rate of
change is

    dE/dt = omega(t)*omega_dot(t)*|q(t)|^2 - 2*gamma*|q_dot(t)|^2

(the first term is the power delivered by the explicit time-dependence of
the Hamiltonian -- i.e. the external drive; the second is dissipation).
Integrating this along the trajectory and comparing to E(final_time) -
E(t0) is the "ledger closes" check.

REPEATED, EXPLICIT STATEMENT (per zero_point_energy/README.md and the
source ZPE reference document's D57): dynamical Casimir photon production
is powered entirely by the external modulation of omega(t); it is NOT
stationary-vacuum energy extraction. No function here returns a nonzero N
without an explicit, accounted-for `omega_dot` driving it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
from scipy.integrate import solve_ivp

from .constants import HBAR

# numpy >= 2.0 renamed trapz -> trapezoid; requirements.txt only pins
# numpy>=1.26, so support both without forcing a numpy floor bump.
_trapezoid = getattr(np, "trapezoid", None) or np.trapz


def windowed_sinusoidal_omega(
    omega0: float,
    epsilon: float,
    drive_frequency: float,
    duration: float,
    phase: float = 0.0,
) -> Callable[[float], float]:
    """omega(t) = omega0*[1 + epsilon*window(t)*cos(drive_frequency*t + phase)].

    window(t) = sin^2(pi*t/duration) for 0 <= t <= duration, else 0: this
    gives omega(t) -> omega0 smoothly (continuously differentiable) outside
    [0, duration], so "before" (t<=0) and "after" (t>=duration) are both
    genuine constant-omega0 regions as required for Bogoliubov matching.
    `epsilon` is the dimensionless modulation depth; `drive_frequency`
    (rad/s) is typically set near 2*omega0 for parametric resonance
    (D7/D62 in the ZPE reference document; Dodonov 2010).
    """
    if omega0 <= 0:
        raise ValueError(f"omega0 must be > 0, got {omega0!r}")
    if duration <= 0:
        raise ValueError(f"duration must be > 0, got {duration!r}")
    if not math.isfinite(epsilon):
        raise ValueError(f"epsilon must be finite, got {epsilon!r}")

    def omega(t: float) -> float:
        if 0.0 <= t <= duration:
            window = math.sin(math.pi * t / duration) ** 2
        else:
            window = 0.0
        return omega0 * (1.0 + epsilon * window * math.cos(drive_frequency * t + phase))

    return omega


def resonant_drive_frequency(omega0: float, detuning: float = 0.0) -> float:
    """Parametric-resonance drive frequency Omega = 2*omega0 + detuning."""
    return 2.0 * omega0 + detuning


def smooth_ramp_omega(
    omega_initial: float,
    omega_final: float,
    ramp_start: float,
    ramp_duration: float,
) -> Callable[[float], float]:
    """A smooth (Hann/raised-cosine), monotonic, non-periodic ramp from
    omega_initial to omega_final over [ramp_start, ramp_start+ramp_duration],
    constant before and after.

    This is the adiabatic-theorem test case (Birrell & Davies-style sudden
    vs. adiabatic frequency change), distinct from `windowed_sinusoidal_omega`'s
    resonant periodic drive: a slow RAMP suppresses particle production as
    ramp_duration grows (adiabatic theorem), whereas a slow *envelope* on a
    resonantly-tuned periodic drive does not -- resonant parametric driving
    amplifies exponentially with total interaction time regardless of how
    gently it is switched on. Use this function for adiabatic-limit tests
    and `windowed_sinusoidal_omega` for resonance/detuning tests.
    """
    if omega_initial <= 0 or omega_final <= 0:
        raise ValueError("omega_initial and omega_final must be > 0")
    if ramp_duration <= 0:
        raise ValueError(f"ramp_duration must be > 0, got {ramp_duration!r}")

    def omega(t: float) -> float:
        if t <= ramp_start:
            return omega_initial
        if t >= ramp_start + ramp_duration:
            return omega_final
        s = (t - ramp_start) / ramp_duration
        smoothstep = 0.5 * (1.0 - math.cos(math.pi * s))  # 0->1, zero derivative at both ends
        return omega_initial + (omega_final - omega_initial) * smoothstep

    return omega


@dataclass
class DCEResult:
    """Bogoliubov coefficients, particle number, and diagnostics."""

    alpha: complex
    beta: complex
    particle_number: float  # |beta|^2
    wronskian_error: float  # relative: | |alpha|^2 - |beta|^2 - 1 | / max(|alpha|^2+|beta|^2, 1)
    omega_initial: float
    omega_final: float
    initial_time: float
    final_time: float
    integration_success: bool
    max_step_error_estimate: float
    excitation_energy: float  # hbar * omega_final * particle_number, J
    trajectory: Optional[dict] = field(default=None, repr=False)


def _pack_initial_state(omega_initial: float) -> np.ndarray:
    q0 = 1.0 / math.sqrt(2.0 * omega_initial)
    qdot0 = -1j * omega_initial * q0
    return np.array([q0.real, q0.imag, qdot0.real, qdot0.imag], dtype=float)


def _unpack(y: np.ndarray):
    q = y[0] + 1j * y[1]
    qdot = y[2] + 1j * y[3]
    return q, qdot


def _rhs(t: float, y: np.ndarray, omega_func: Callable[[float], float], gamma: float) -> np.ndarray:
    q, qdot = _unpack(y)
    omega_t = omega_func(t)
    qddot = -(omega_t**2) * q - 2.0 * gamma * qdot
    return np.array([qdot.real, qdot.imag, qddot.real, qddot.imag], dtype=float)


def bogoliubov_coefficients(
    omega_func: Callable[[float], float],
    initial_time: float,
    final_time: float,
    omega_initial: Optional[float] = None,
    omega_final: Optional[float] = None,
    gamma: float = 0.0,
    require_constant_regions: bool = True,
    constant_region_check_points: int = 5,
    constant_region_tol: float = 1e-9,
    rtol: float = 1e-11,
    atol: float = 1e-13,
    method: str = "DOP853",
    return_trajectory: bool = False,
    n_trajectory_points: int = 500,
) -> DCEResult:
    """Solve q_ddot + 2*gamma*q_dot + omega(t)^2*q = 0 from vacuum-normalized
    positive-frequency initial data and extract the Bogoliubov coefficients
    at `final_time`.

    `omega_func(t)` must be (numerically) constant on some neighborhood of
    both `initial_time` and `final_time`; `require_constant_regions=True`
    (default) checks this explicitly by sampling `omega_func` at several
    points and raising ValueError if it is not, since alpha/beta are only
    well-defined mode-matching quantities in genuine constant-frequency
    asymptotic regions (see module docstring). gamma >= 0 is the optional
    damping rate (rad/s); gamma=0 (default) is the exact unitary case.
    """
    if final_time <= initial_time:
        raise ValueError("final_time must be > initial_time")
    if gamma < 0:
        raise ValueError(f"gamma must be >= 0, got {gamma!r}")

    if omega_initial is None:
        omega_initial = omega_func(initial_time)
    if omega_final is None:
        omega_final = omega_func(final_time)
    if omega_initial <= 0 or omega_final <= 0:
        raise ValueError("omega_initial and omega_final must be > 0")

    if require_constant_regions:
        span = final_time - initial_time
        probe_dt = 1e-6 * span
        for label, t_center, omega_ref in (
            ("initial", initial_time, omega_initial),
            ("final", final_time, omega_final),
        ):
            for k in range(1, constant_region_check_points + 1):
                sample = omega_func(t_center + (-1) ** k * k * probe_dt)
                if abs(sample - omega_ref) > constant_region_tol * omega_ref:
                    raise ValueError(
                        f"omega_func is not constant near the {label} time "
                        f"{t_center!r} (sampled {sample!r} vs reference {omega_ref!r}); "
                        "Bogoliubov coefficients require genuine constant-frequency "
                        "asymptotic regions. Pass require_constant_regions=False to "
                        "override at your own risk."
                    )

    y0 = _pack_initial_state(omega_initial)
    t_eval = np.linspace(initial_time, final_time, n_trajectory_points) if return_trajectory else None

    solution = solve_ivp(
        _rhs,
        (initial_time, final_time),
        y0,
        args=(omega_func, gamma),
        method=method,
        rtol=rtol,
        atol=atol,
        dense_output=False,
        t_eval=t_eval,
    )
    if not solution.success:
        raise RuntimeError(f"DCE integration failed: {solution.message}")

    q_final, qdot_final = _unpack(solution.y[:, -1])
    wf = omega_final
    sqrt_2wf = math.sqrt(2.0 * wf)
    a_coef = 0.5 * (q_final * sqrt_2wf + 1j * qdot_final * math.sqrt(2.0 / wf))
    b_coef = 0.5 * (q_final * sqrt_2wf - 1j * qdot_final * math.sqrt(2.0 / wf))
    alpha = a_coef * np.exp(1j * wf * final_time)
    beta = b_coef * np.exp(-1j * wf * final_time)

    particle_number = float(abs(beta) ** 2)
    # Reported as a *relative* residual, |alpha|^2 - |beta|^2 - 1| divided
    # by max(|alpha|^2 + |beta|^2, 1): under strong exponential parametric
    # gain (|alpha|, |beta| >> 1) the absolute residual scales with the
    # solver's rtol times the (huge) magnitudes themselves, so an absolute
    # threshold would misreport an accurate solution as having "broken"
    # unitarity. At small N (|alpha|~1, |beta|~0) this reduces to the plain
    # absolute residual, matching the near-vacuum regime exactly.
    wronskian_norm = max(abs(alpha) ** 2 + abs(beta) ** 2, 1.0)
    wronskian_error = abs(abs(alpha) ** 2 - abs(beta) ** 2 - 1.0) / wronskian_norm
    excitation_energy = HBAR * omega_final * particle_number

    trajectory = None
    if return_trajectory:
        trajectory = {
            "t": solution.t,
            "q": solution.y[0] + 1j * solution.y[1],
            "qdot": solution.y[2] + 1j * solution.y[3],
        }

    return DCEResult(
        alpha=complex(alpha),
        beta=complex(beta),
        particle_number=particle_number,
        wronskian_error=wronskian_error,
        omega_initial=omega_initial,
        omega_final=omega_final,
        initial_time=initial_time,
        final_time=final_time,
        integration_success=solution.success,
        max_step_error_estimate=float(rtol),  # solve_ivp does not expose a single global error bound; rtol/atol are the requested tolerances
        excitation_energy=excitation_energy,
        trajectory=trajectory,
    )


@dataclass
class EnergyLedgerResult:
    """Explicit DCE energy accounting: drive work in, dissipation out,
    change in mode energy -- must close (see module docstring derivation)."""

    initial_mode_energy: float  # (1/2)*hbar*omega_initial
    final_mode_energy: float  # (N+1/2)*hbar*omega_final (undamped) or less (damped)
    delta_mode_energy: float
    drive_work: float  # integral of hbar*omega*omega_dot*|q|^2 dt
    dissipated_energy: float  # integral of hbar*2*gamma*|qdot|^2 dt (0 if gamma=0)
    ledger_error: float  # |delta_mode_energy - (drive_work - dissipated_energy)|


def energy_ledger(
    omega_func: Callable[[float], float],
    omega_dot_func: Callable[[float], float],
    initial_time: float,
    final_time: float,
    gamma: float = 0.0,
    n_quadrature_points: int = 20000,
    **bogoliubov_kwargs,
) -> EnergyLedgerResult:
    """Verify that the DCE mode energy's change equals drive work minus
    dissipation, by independently trapezoidal-integrating dE/dt along the
    trajectory and comparing to the endpoint difference.

    `omega_dot_func(t)` must be the analytic derivative of `omega_func`
    (not computed by finite differences here, to keep this an independent
    check against `bogoliubov_coefficients`'s own trajectory rather than a
    self-consistency tautology).
    """
    result = bogoliubov_coefficients(
        omega_func, initial_time, final_time, gamma=gamma,
        return_trajectory=True, n_trajectory_points=n_quadrature_points,
        **bogoliubov_kwargs,
    )
    traj = result.trajectory
    t = traj["t"]
    q = traj["q"]
    qdot = traj["qdot"]
    omega_t = np.array([omega_func(ti) for ti in t])
    omega_dot_t = np.array([omega_dot_func(ti) for ti in t])

    power = HBAR * omega_t * omega_dot_t * np.abs(q) ** 2
    dissipation_rate = HBAR * 2.0 * gamma * np.abs(qdot) ** 2

    drive_work = float(_trapezoid(power, t))
    dissipated_energy = float(_trapezoid(dissipation_rate, t))

    e_initial = 0.5 * HBAR * result.omega_initial
    e_final = 0.5 * HBAR * omega_t[-1] * (1.0 + 2.0 * result.particle_number) if gamma == 0.0 else None
    if e_final is None:
        # Damped case: read the final mode energy directly off the trajectory
        # rather than the undamped (N+1/2) closed form, which assumed
        # unitary evolution.
        e_final = 0.5 * (abs(qdot[-1]) ** 2 + omega_t[-1] ** 2 * abs(q[-1]) ** 2) * HBAR

    delta_e = e_final - e_initial
    ledger_error = abs(delta_e - (drive_work - dissipated_energy))

    return EnergyLedgerResult(
        initial_mode_energy=e_initial,
        final_mode_energy=e_final,
        delta_mode_energy=delta_e,
        drive_work=drive_work,
        dissipated_energy=dissipated_energy,
        ledger_error=ledger_error,
    )
