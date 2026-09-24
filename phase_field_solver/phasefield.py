#!/usr/bin/env python3
"""GCPF 1.0.0: variational Fourier Galerkin solver on a periodic corrugated tube.

See docs/NUMERICAL_METHOD.md for the exact continuum problem, quadrature
limitations, stability conditions, and the validation scope.
CPU only; NumPy + SciPy; no network access or external services.
"""
from __future__ import annotations

import argparse
import dataclasses
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import tempfile
import time
from typing import Callable

import numpy as np
import scipy
from scipy.linalg import cho_factor, cho_solve, eigh, solve

VERSION = "1.0.0"
SCHEMA = "gcpf-checkpoint-v1"
TWO_PI = 2.0 * np.pi


class SolverError(RuntimeError):
    """A rejected numerical problem or computation with an actionable message."""


def scalar(value, name="value"):
    """Read finite floats, integers, decimal strings, or exact rational strings."""
    if isinstance(value, bool):
        raise SolverError(f"{name}: booleans are not numerical parameters")
    try:
        x = float(Fraction(value)) if isinstance(value, str) else float(value)
    except (ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise SolverError(f"{name}: expected a finite number or rational string") from exc
    if not math.isfinite(x):
        raise SolverError(f"{name}: NaN and infinity are forbidden")
    return x


def integer(value, name="value", minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise SolverError(f"{name}: expected an integer")
    if value < minimum:
        raise SolverError(f"{name}: must be at least {minimum}")
    return int(value)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def source_hash():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def exact_float(value):
    x = float(value)
    if not math.isfinite(x):
        raise SolverError("Cannot serialize a nonfinite numerical result")
    return {"binary64_exact_decimal": str(Decimal.from_float(x)),
            "binary64_hex": x.hex()}


def environment():
    return {"python": platform.python_version(), "numpy": np.__version__,
            "scipy": scipy.__version__, "platform": platform.platform(),
            "solver_version": VERSION, "solver_sha256": source_hash(),
            "arithmetic": "IEEE-754 binary64",
            "threads": {k: os.environ.get(k) for k in
                        ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")}}


def write_json(path, obj):
    atomic_bytes(path, (json.dumps(obj, indent=2, allow_nan=False) + "\n").encode())


def atomic_bytes(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_npz(path, **arrays):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            np.savez_compressed(handle, **arrays)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@dataclass(frozen=True)
class Model:
    radius: float = 1.0
    amplitude: float = 0.1
    axial_scale: float = 1.5
    n: int = 2
    m: int = 1
    phase_theta: float = 0.0
    phase_zeta: float = 0.0
    mass2: float = 0.25
    quartic: float = 0.5
    potential_constant: float = 0.0
    potential_amplitude: float = 0.0
    potential_n: int = 2
    potential_m: int = 1
    potential_phase_theta: float = 0.0
    potential_phase_zeta: float = 0.0
    curvature_h2: float = 0.0
    curvature_k: float = 0.0
    lapse_scale: float = 1.0
    lapse_amplitude: float = 0.0
    lapse_n: int = 1
    lapse_m: int = 0
    lapse_phase_theta: float = 0.0
    lapse_phase_zeta: float = 0.0

    def __post_init__(self):
        ints = {"n": 1, "m": 1, "potential_n": 0, "potential_m": 0,
                "lapse_n": 0, "lapse_m": 0}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            cleaned = (integer(value, field.name, ints[field.name])
                       if field.name in ints else scalar(value, field.name))
            object.__setattr__(self, field.name, cleaned)
        if not self.radius > abs(self.amplitude):
            raise SolverError("radius must strictly exceed abs(amplitude)")
        if self.axial_scale <= 0 or self.lapse_scale <= 0:
            raise SolverError("axial_scale and lapse_scale must be positive")
        if abs(self.lapse_amplitude) >= 1:
            raise SolverError("abs(lapse_amplitude) must be less than one")
        if self.quartic < 0:
            raise SolverError("This implementation requires quartic >= 0")


@dataclass(frozen=True)
class Resolution:
    theta_cutoff: int = 4
    zeta_cutoff: int = 4
    theta_points: int = 48
    zeta_points: int = 48
    memory_limit_mib: int = 1024

    def __post_init__(self):
        for field in dataclasses.fields(self):
            minimum = 1 if field.name in ("theta_points", "zeta_points",
                                         "memory_limit_mib") else 0
            object.__setattr__(self, field.name,
                               integer(getattr(self, field.name), field.name, minimum))
        if self.theta_points <= 4 * self.theta_cutoff:
            raise SolverError("theta_points must exceed 4*theta_cutoff")
        if self.zeta_points <= 4 * self.zeta_cutoff:
            raise SolverError("zeta_points must exceed 4*zeta_cutoff")

    @property
    def ndof(self):
        return (2 * self.theta_cutoff + 1) * (2 * self.zeta_cutoff + 1)

    @property
    def ngrid(self):
        return self.theta_points * self.zeta_points


def strict_dataclass(cls, value):
    if not isinstance(value, dict):
        raise SolverError(f"{cls.__name__} configuration must be an object")
    names = {f.name for f in dataclasses.fields(cls)}
    extra = set(value) - names
    if extra:
        raise SolverError(f"Unknown {cls.__name__} keys: {sorted(extra)}")
    return cls(**value)


def geometry(model, theta, zeta):
    """Analytical first/second fundamental forms; theta,zeta may be broadcast arrays."""
    s = np.sin(model.n * theta + model.phase_theta)
    c = np.cos(model.m * zeta + model.phase_zeta)
    ct = np.cos(model.n * theta + model.phase_theta)
    sz = np.sin(model.m * zeta + model.phase_zeta)
    R = model.radius + model.amplitude * s * c
    Rt = model.amplitude * model.n * ct * c
    Rz = -model.amplitude * model.m * s * sz
    Rtt = -model.amplitude * model.n**2 * s * c
    Rzz = -model.amplitude * model.m**2 * s * c
    Rtz = -model.amplitude * model.n * model.m * ct * sz
    a = model.axial_scale
    E, B, G = R*R + Rt*Rt, Rt*Rz, a*a + Rz*Rz
    det = a*a*(R*R + Rt*Rt) + R*R*Rz*Rz
    area = np.sqrt(det)
    btt = a*(R*R + 2*Rt*Rt - R*Rtt)/area
    btz = a*(Rt*Rz - R*Rtz)/area
    bzz = -a*R*Rzz/area
    H = (G*btt - 2*B*btz + E*bzz)/(2*det)
    KG = (btt*bzz - btz*btz)/det
    N = model.lapse_scale * (1 + model.lapse_amplitude *
        np.cos(model.lapse_n*theta + model.lapse_phase_theta) *
        np.cos(model.lapse_m*zeta + model.lapse_phase_zeta))
    U = (model.potential_constant + model.potential_amplitude *
         np.sin(model.potential_n*theta + model.potential_phase_theta) *
         np.cos(model.potential_m*zeta + model.potential_phase_zeta)
         + model.curvature_h2*H*H + model.curvature_k*KG)
    return dict(R=R, Rt=Rt, Rz=Rz, Rtt=Rtt, Rzz=Rzz, Rtz=Rtz,
                E=E, B=B, G=G, det=det, area=area,
                itt=G/det, itz=-B/det, izz=E/det,
                btt=btt, btz=btz, bzz=bzz, H=H, KG=KG,
                N=N, U=U, mass2=model.mass2 + 2*U)


def trig_basis(x, cutoff):
    """Basis [1,sqrt(2)cos(x),sqrt(2)sin(x),...] normalized in angular average."""
    values = [np.ones_like(x)]
    derivatives = [np.zeros_like(x)]
    labels = [("constant", 0)]
    for k in range(1, cutoff+1):
        values.extend([np.sqrt(2)*np.cos(k*x), np.sqrt(2)*np.sin(k*x)])
        derivatives.extend([-k*np.sqrt(2)*np.sin(k*x), k*np.sqrt(2)*np.cos(k*x)])
        labels.extend([("cos", k), ("sin", k)])
    return np.column_stack(values), np.column_stack(derivatives), labels


@dataclass
class Spectrum:
    values: np.ndarray
    vectors: np.ndarray
    residuals: np.ndarray
    mass_orthogonality_error: float
    classification_tolerance: float

    def report(self):
        tol = self.classification_tolerance
        return {"squared_frequencies": [exact_float(v) for v in self.values],
                "frequencies": [exact_float(np.sqrt(v)) if v > tol else None
                                for v in self.values],
                "growth_rates": [exact_float(np.sqrt(-v)) if v < -tol else None
                                 for v in self.values],
                "classification": ["negative" if v < -tol else
                                   "positive" if v > tol else "numerically_unresolved_zero"
                                   for v in self.values],
                "scaled_residuals": [exact_float(v) for v in self.residuals],
                "mass_orthogonality_error": exact_float(self.mass_orthogonality_error),
                "classification_tolerance": exact_float(tol),
                "scope": "assembled finite Galerkin matrix; not certified continuum bounds"}


class SurfaceSolver:
    """Fixed geometry, fixed lapse, real scalar; periodic in theta and zeta."""

    def __init__(self, model=None, resolution=None):
        self.model = model or Model()
        self.resolution = resolution or Resolution()
        m, r = self.model, self.resolution
        nt = max(m.n if m.amplitude else 0,
                 m.potential_n if m.potential_amplitude else 0,
                 m.lapse_n if m.lapse_amplitude else 0)
        nz = max(m.m if m.amplitude else 0,
                 m.potential_m if m.potential_amplitude else 0,
                 m.lapse_m if m.lapse_amplitude else 0)
        if r.theta_points <= 2*nt or r.zeta_points <= 2*nz:
            raise SolverError("Quadrature does not resolve the input coefficient harmonics")
        estimated = 8*(6*r.ngrid*r.ndof + 12*r.ndof**2 + 40*r.ngrid)
        if estimated > r.memory_limit_mib*1024**2:
            raise SolverError(f"Conservative dense workspace estimate {estimated} bytes "
                              "exceeds memory_limit_mib; lower cutoff/grid or raise the limit")
        self.estimated_workspace_bytes = estimated
        self.theta_1d = TWO_PI*np.arange(r.theta_points)/r.theta_points
        self.zeta_1d = TWO_PI*np.arange(r.zeta_points)/r.zeta_points
        self.theta, self.zeta = np.meshgrid(self.theta_1d, self.zeta_1d, indexing="ij")
        self.geom = {key: np.broadcast_to(value, self.theta.shape).ravel().copy()
                     for key, value in geometry(m, self.theta, self.zeta).items()}
        bt, dt, lt = trig_basis(self.theta_1d, r.theta_cutoff)
        bz, dz, lz = trig_basis(self.zeta_1d, r.zeta_cutoff)
        self.B = np.kron(bt, bz)
        self.Dt = np.kron(dt, bz)
        self.Dz = np.kron(bt, dz)
        self.labels = [(t, z) for t in lt for z in lz]
        self.ndof = r.ndof
        self.cell_weight = TWO_PI**2/r.ngrid
        g = self.geom
        self.wm = self.cell_weight*g["area"]/g["N"]
        self.wk = self.cell_weight*g["area"]*g["N"]
        self.M = self.B.T @ (self.wm[:, None]*self.B)
        cross = self.Dt.T @ ((self.wk*g["itz"])[:, None]*self.Dz)
        self.K = self.Dt.T @ ((self.wk*g["itt"])[:, None]*self.Dt)
        self.K += self.Dz.T @ ((self.wk*g["izz"])[:, None]*self.Dz)
        self.K += cross + cross.T
        self.K += self.B.T @ ((self.wk*g["mass2"])[:, None]*self.B)
        self.assembly_asymmetry = {
            "mass": float(np.max(np.abs(self.M-self.M.T))),
            "stiffness": float(np.max(np.abs(self.K-self.K.T)))}
        for a in (self.M, self.K):
            if not np.isfinite(a).all():
                raise SolverError("Nonfinite operator assembly")
            asymmetry = np.linalg.norm(a-a.T, ord=np.inf)
            if asymmetry > 1e-11*max(1.0, np.linalg.norm(a, ord=np.inf)):
                raise SolverError("Operator symmetry check failed before eigensolve")
            a[:] = (a+a.T)/2
        self.mass_factor = cho_factor(self.M, lower=True, check_finite=True)
        self.linear_min = float(eigh(self.K, self.M, eigvals_only=True,
                                    subset_by_index=[0, 0])[0])
        self.linear_max = float(eigh(self.K, self.M, eigvals_only=True,
                                    subset_by_index=[self.ndof-1, self.ndof-1])[0])
        self.fingerprint = digest({"model": dataclasses.asdict(m),
                                   "resolution": dataclasses.asdict(r),
                                   "basis": "real-tensor-trigonometric-v1",
                                   "solver_version": VERSION})

    def vector(self, q, name="coefficients"):
        if np.iscomplexobj(q):
            raise SolverError(f"{name}: complex data are not accepted by the real field solver")
        q = np.asarray(q, dtype=float)
        if q.shape != (self.ndof,) or not np.isfinite(q).all():
            raise SolverError(f"{name}: expected {self.ndof} finite real coefficients")
        return q

    def mass_solve(self, rhs):
        return cho_solve(self.mass_factor, rhs, check_finite=True)

    def field(self, q):
        return (self.B @ self.vector(q)).reshape(self.theta.shape)

    def project(self, field):
        if np.iscomplexobj(field):
            raise SolverError("Projection requires a real scalar field")
        values = np.asarray(field, dtype=float)
        if values.ndim == 0:
            values = np.full(self.resolution.ngrid, values)
        else:
            values = np.broadcast_to(values, self.theta.shape).ravel()
        if not np.isfinite(values).all():
            raise SolverError("Projection input is nonfinite")
        return self.mass_solve(self.B.T @ (self.wm*values))

    def weak_source(self, field):
        if np.iscomplexobj(field):
            raise SolverError("Source requires real values")
        values = np.broadcast_to(np.asarray(field, dtype=float), self.theta.shape).ravel()
        if not np.isfinite(values).all():
            raise SolverError("Source is nonfinite")
        return self.B.T @ (self.wk*values)

    def force(self, q):
        q = self.vector(q)
        phi = self.B @ q
        with np.errstate(over="raise", invalid="raise"):
            return self.K @ q + self.model.quartic*(self.B.T @ (self.wk*phi**3))

    def hessian(self, q):
        phi = self.B @ self.vector(q)
        h = self.K + 3*self.model.quartic*(self.B.T @ ((self.wk*phi**2)[:, None]*self.B))
        return (h+h.T)/2

    def potential_energy(self, q):
        q = self.vector(q)
        phi = self.B @ q
        with np.errstate(over="raise", invalid="raise"):
            return float(q @ self.K @ q/2 + self.model.quartic*np.dot(self.wk, phi**4)/4)

    def energy(self, q, velocity):
        v = self.vector(velocity, "velocity")
        return float(v @ self.M @ v/2 + self.potential_energy(q))

    def dual_norm(self, covector):
        f = self.vector(covector, "covector")
        return float(np.sqrt(max(0.0, f @ self.mass_solve(f))))

    def mass_norm(self, q):
        q = self.vector(q)
        return float(np.sqrt(max(0.0, q @ self.M @ q)))

    def spectrum(self, count=8, background=None):
        count = integer(count, "count", 1)
        if count > self.ndof:
            raise SolverError("Requested more eigenvalues than Galerkin degrees of freedom")
        h = self.K if background is None else self.hessian(background)
        vals, vecs = eigh(h, self.M, subset_by_index=[0, count-1], check_finite=True)
        res = h @ vecs - (self.M @ vecs)*vals[None, :]
        denom = ((np.linalg.norm(h, "fro") + np.abs(vals)*np.linalg.norm(self.M, "fro"))
                 * np.linalg.norm(vecs, axis=0))
        residuals = np.linalg.norm(res, axis=0)/np.maximum(denom, np.finfo(float).tiny)
        orth = np.max(np.abs(vecs.T @ self.M @ vecs-np.eye(count)))
        tol = 128*np.finfo(float).eps*max(1.0, abs(self.linear_min), abs(self.linear_max),
                                        float(np.max(np.abs(vals))))
        return Spectrum(vals, vecs, residuals, float(orth), tol)

    def step_frequency_bound(self, q):
        phi = self.B @ self.vector(q)
        # Bound for nonnegative quartic Hessian added to the generalized linear operator.
        return max(abs(self.linear_min), abs(self.linear_max)) + \
            3*self.model.quartic*float(np.max((self.geom["N"]*phi)**2))

    def geometry_report(self):
        g = self.geom
        r = self.resolution
        return {"area": exact_float(self.cell_weight*np.sum(g["area"])),
                "integral_gaussian_curvature": exact_float(
                    self.cell_weight*np.dot(g["area"], g["KG"])),
                "integral_mean_curvature_squared": exact_float(
                    self.cell_weight*np.dot(g["area"], g["H"]**2)),
                "sampled_minimum_H_squared_minus_K": exact_float(np.min(g["H"]**2-g["KG"])),
                "analytic_radius_lower_bound": exact_float(self.model.radius-abs(self.model.amplitude)),
                "analytic_lapse_lower_bound": exact_float(
                    self.model.lapse_scale*(1-abs(self.model.lapse_amplitude))),
                "sampled_minimum_determinant": exact_float(np.min(g["det"])),
                "ndof": self.ndof, "quadrature_shape": [r.theta_points, r.zeta_points],
                "estimated_workspace_bytes": self.estimated_workspace_bytes,
                "mass_condition_number": exact_float(np.linalg.cond(self.M)),
                "assembly_asymmetry": {k: exact_float(v) for k, v in self.assembly_asymmetry.items()},
                "fingerprint": self.fingerprint}


@dataclass
class State:
    q: np.ndarray
    velocity: np.ndarray
    dt: float
    step: int = 0
    origin_time: float = 0.0
    work: float = 0.0
    dissipated: float = 0.0
    initial_energy: float | None = None

    @property
    def time(self):
        return self.origin_time + self.step*self.dt


def initial_state(op, q, velocity=None, dt=0.005):
    dt = scalar(dt, "dt")
    if dt <= 0:
        raise SolverError("dt must be positive")
    q = op.vector(q).copy()
    velocity = np.zeros(op.ndof) if velocity is None else op.vector(velocity).copy()
    return State(q, velocity, dt, initial_energy=op.energy(q, velocity))


def state_sample(op, state):
    energy = op.energy(state.q, state.velocity)
    return {"step": state.step, "time": state.time, "energy": energy,
            "work": state.work, "dissipated": state.dissipated,
            "balance_defect": energy-state.initial_energy-state.work+state.dissipated,
            "max_abs_field": float(np.max(np.abs(op.B @ state.q))),
            "mass_norm": op.mass_norm(state.q)}


def integrate(op, state, steps, drive=None, damping=0.0, sample_every=10,
              guard=1.8, on_sample=None):
    """Second order Verlet with exact damping half flows.

    drive(t) returns a weak force covector. Time is origin + integer_step*dt.
    State is updated only after a completed finite step. A failed guard leaves
    the last committed state available to the caller for a failure checkpoint.
    """
    steps = integer(steps, "steps", 0)
    sample_every = integer(sample_every, "sample_every", 1)
    damping = scalar(damping, "damping")
    guard = scalar(guard, "guard")
    if damping < 0 or not 0 < guard < 2:
        raise SolverError("Require damping >= 0 and 0 < guard < 2")
    op.vector(state.q); op.vector(state.velocity)
    if scalar(state.dt, "dt") <= 0 or integer(state.step, "step", 0) != state.step:
        raise SolverError("Invalid state")
    for name in ("origin_time", "work", "dissipated"):
        scalar(getattr(state, name), name)
    if state.initial_energy is None:
        state.initial_energy = op.energy(state.q, state.velocity)
    scalar(state.initial_energy, "initial_energy")
    dt = state.dt
    maximum_samples = 2 + steps // sample_every
    history_estimate = 8 * maximum_samples * (4 * op.ndof + 40)
    if op.estimated_workspace_bytes + history_estimate > op.resolution.memory_limit_mib * 1024**2:
        raise SolverError("History plus operator workspace exceeds memory_limit_mib; "
                          "increase sample_every or reduce the requested run length")
    damp_factor = math.exp(-damping*dt/2)
    samples, qs, vs = [], [], []

    def emit():
        sample = state_sample(op, state)
        samples.append(sample); qs.append(state.q.copy()); vs.append(state.velocity.copy())
        if on_sample is not None:
            on_sample(state, sample)

    emit()
    for local in range(steps):
        if dt*math.sqrt(op.step_frequency_bound(state.q)) > guard:
            raise SolverError("Timestep guard exceeded at committed step "
                              f"{state.step}; reduce dt and restart from compatible initial data")
        q0, v0 = state.q.copy(), state.velocity.copy()
        t0, t1 = state.time, state.origin_time+(state.step+1)*dt
        f0 = np.zeros(op.ndof) if drive is None else op.vector(drive(t0), "drive")
        f1 = np.zeros(op.ndof) if drive is None else op.vector(drive(t1), "drive")
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            va = damp_factor*v0
            loss = float((v0 @ op.M @ v0-va @ op.M @ va)/2)
            vh = va + (dt/2)*op.mass_solve(f0-op.force(q0))
            q1 = q0 + dt*vh
            op.vector(q1)
            if dt*math.sqrt(op.step_frequency_bound(q1)) > guard:
                raise SolverError("Timestep guard exceeded in proposed step; last committed "
                                  f"step is {state.step}. Reduce dt for a new run")
            vb = vh + (dt/2)*op.mass_solve(f1-op.force(q1))
            v1 = damp_factor*vb
            loss += float((vb @ op.M @ vb-v1 @ op.M @ v1)/2)
            op.vector(v1)
            work = float(dt*(f0 @ v0+f1 @ v1)/2)
            energy = op.energy(q1, v1)
            if not math.isfinite(energy+work+loss):
                raise SolverError("Nonfinite step; last committed state retained")
        state.q, state.velocity = q1, v1
        state.step += 1
        state.work += work
        state.dissipated += loss
        if state.step % sample_every == 0 or local == steps-1:
            emit()
    return {"samples": samples, "q": np.asarray(qs), "velocity": np.asarray(vs)}


def equilibrium(op, seed, max_iter=100, atol=1e-11, rtol=1e-10):
    """Damped modified Newton minimization; report Hessian classification separately."""
    q = op.vector(seed).copy()
    max_iter = integer(max_iter, "max_iter", 1)
    atol, rtol = scalar(atol, "atol"), scalar(rtol, "rtol")
    if atol <= 0 or rtol < 0:
        raise SolverError("Require atol > 0 and rtol >= 0")
    initial_residual = op.dual_norm(op.force(q))
    tolerance = atol+rtol*initial_residual
    trace = []
    converged = False
    reason = "maximum_iterations"
    for iteration in range(max_iter+1):
        grad = op.force(q)
        residual = op.dual_norm(grad)
        value = op.potential_energy(q)
        trace.append({"iteration": iteration, "energy": value, "dual_residual": residual})
        if residual <= tolerance:
            converged, reason = True, "residual_tolerance"
            break
        if iteration == max_iter:
            break
        hess = op.hessian(q)
        hmin = float(eigh(hess, op.M, eigvals_only=True, subset_by_index=[0, 0])[0])
        shift = max(0.0, 1e-6-hmin)
        direction = solve(hess+shift*op.M, -grad, assume_a="pos")
        slope = float(grad @ direction)
        if not slope < 0 or not np.isfinite(direction).all():
            direction = -op.mass_solve(grad)
            slope = float(grad @ direction)
        step_length = 1.0
        accepted = False
        for _ in range(50):
            candidate = q+step_length*direction
            try:
                candidate_energy = op.potential_energy(candidate)
            except FloatingPointError:
                candidate_energy = math.inf
            if candidate_energy <= value+1e-4*step_length*slope:
                accepted = True
                break
            # Near an energy arithmetic floor, require a strict residual improvement
            # and no resolvable increase of energy rather than stall indefinitely.
            floor = 16*np.finfo(float).eps*max(1.0, abs(value))
            if abs(candidate_energy-value) <= floor:
                if op.dual_norm(op.force(candidate)) < residual*0.5:
                    accepted = True
                    break
            step_length *= 0.5
        trace[-1]["line_step"] = step_length
        trace[-1]["hessian_shift"] = shift
        if not accepted:
            reason = "line_search_failed"
            break
        q = candidate
    spectrum = op.spectrum(min(8, op.ndof), background=q)
    classification = spectrum.report()["classification"][0]
    return {"q": q, "converged": converged, "reason": reason,
            "residual": op.dual_norm(op.force(q)), "tolerance": tolerance,
            "energy": op.potential_energy(q), "trace": trace,
            "hessian_spectrum": spectrum,
            "stationary_classification": classification}


def checkpoint_payload_hash(metadata, q, velocity):
    h = hashlib.sha256(canonical(metadata).encode())
    for value in (q, velocity):
        a = np.asarray(value, dtype="<f8", order="C")
        h.update(str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def save_checkpoint(path, op, state, config):
    op.vector(state.q); op.vector(state.velocity)
    metadata = {"schema": SCHEMA, "solver_version": VERSION, "source_sha256": source_hash(),
                "operator_fingerprint": op.fingerprint, "config": config,
                "dt": state.dt, "step": state.step, "origin_time": state.origin_time,
                "work": state.work, "dissipated": state.dissipated,
                "initial_energy": state.initial_energy}
    state_hash = checkpoint_payload_hash(metadata, state.q, state.velocity)
    atomic_npz(path, q=state.q, velocity=state.velocity,
               metadata=np.array(canonical(metadata)), sha256=np.array(state_hash))


def load_checkpoint(path, expected_solver=None):
    try:
        with np.load(path, allow_pickle=False) as archive:
            if set(archive.files) != {"q", "velocity", "metadata", "sha256"}:
                raise SolverError("Unexpected checkpoint keys")
            q = archive["q"].copy(); velocity = archive["velocity"].copy()
            metadata = json.loads(str(archive["metadata"].item()))
            saved_hash = str(archive["sha256"].item())
    except (OSError, ValueError, KeyError, EOFError) as exc:
        raise SolverError(f"Checkpoint cannot be read: {exc}") from exc
    if metadata.get("schema") != SCHEMA:
        raise SolverError("Checkpoint schema mismatch")
    if metadata.get("source_sha256") != source_hash() or metadata.get("solver_version") != VERSION:
        raise SolverError("Checkpoint requires the exact solver implementation that wrote it")
    if checkpoint_payload_hash(metadata, q, velocity) != saved_hash:
        raise SolverError("Checkpoint integrity digest mismatch")
    config = normalize_config(metadata["config"])
    op = SurfaceSolver(strict_dataclass(Model, config["model"]),
                       strict_dataclass(Resolution, config["resolution"]))
    if metadata["operator_fingerprint"] != op.fingerprint:
        raise SolverError("Checkpoint operator fingerprint mismatch")
    if expected_solver is not None and expected_solver.fingerprint != op.fingerprint:
        raise SolverError("Requested operator differs from checkpoint")
    q = op.vector(q).copy(); velocity = op.vector(velocity).copy()
    dt = scalar(metadata["dt"], "checkpoint dt")
    if dt <= 0:
        raise SolverError("Checkpoint dt must be positive")
    state = State(q, velocity, dt, integer(metadata["step"], "checkpoint step", 0),
                  scalar(metadata["origin_time"]), scalar(metadata["work"]),
                  scalar(metadata["dissipated"]), scalar(metadata["initial_energy"]))
    return op, state, config


DEFAULT_INITIAL = {"kind": "cosine", "amplitude": "1/10", "offset": 0,
                   "theta_mode": 1, "zeta_mode": 1, "velocity_amplitude": 0,
                   "phase_theta": 0, "phase_zeta": 0, "mode_index": 1}
DEFAULT_DRIVE = {"amplitude": 0, "frequency": 1, "theta_mode": 1, "zeta_mode": 1,
                 "phase_time": 0, "phase_theta": 0, "phase_zeta": 0}


def checked_mapping(value, default, label):
    if not isinstance(value, dict):
        raise SolverError(f"{label} must be an object")
    extra = set(value)-set(default)
    if extra:
        raise SolverError(f"Unknown {label} keys: {sorted(extra)}")
    answer = dict(default); answer.update(value)
    for key in answer:
        if key == "kind":
            continue
        if key in ("theta_mode", "zeta_mode", "mode_index"):
            answer[key] = integer(answer[key], key, 0)
        else:
            answer[key] = scalar(answer[key], key)
    return answer


def normalize_config(config):
    if not isinstance(config, dict):
        raise SolverError("Configuration must be an object")
    extra = set(config)-{"model", "resolution", "initial", "drive", "damping"}
    if extra:
        raise SolverError(f"Unknown top-level keys: {sorted(extra)}")
    m = strict_dataclass(Model, config.get("model", {}))
    r = strict_dataclass(Resolution, config.get("resolution", {}))
    initial = checked_mapping(config.get("initial", {}), DEFAULT_INITIAL, "initial")
    drive = checked_mapping(config.get("drive", {}), DEFAULT_DRIVE, "drive")
    if initial["kind"] not in ("constant", "cosine", "eigenmode"):
        raise SolverError("initial.kind must be constant, cosine, or eigenmode")
    if initial["kind"] == "cosine" and (
        initial["theta_mode"] > r.theta_cutoff or initial["zeta_mode"] > r.zeta_cutoff):
        raise SolverError("Initial cosine mode lies outside the retained basis")
    if initial["mode_index"] >= r.ndof and initial["kind"] == "eigenmode":
        raise SolverError("Initial eigenmode index is outside the discrete spectrum")
    if drive["amplitude"] and (2*drive["theta_mode"] >= r.theta_points or
                               2*drive["zeta_mode"] >= r.zeta_points):
        raise SolverError("Drive is not resolved by the quadrature")
    damping = scalar(config.get("damping", 0), "damping")
    if damping < 0:
        raise SolverError("damping must be nonnegative")
    return {"model": dataclasses.asdict(m), "resolution": dataclasses.asdict(r),
            "initial": initial, "drive": drive, "damping": damping}


def read_config(path):
    try:
        raw = {} if path is None else json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SolverError(f"Cannot read configuration: {exc}") from exc
    return normalize_config(raw)


def configured_initial(op, config):
    spec = config["initial"]
    if spec["kind"] == "eigenmode":
        vec = op.spectrum(spec["mode_index"]+1).vectors[:, spec["mode_index"]]
        return spec["amplitude"]*vec, spec["velocity_amplitude"]*vec
    shape = np.ones_like(op.theta)
    if spec["kind"] == "cosine":
        shape = (np.cos(spec["theta_mode"]*op.theta+spec["phase_theta"]) *
                 np.cos(spec["zeta_mode"]*op.zeta+spec["phase_zeta"]))
    return (op.project(spec["offset"]+spec["amplitude"]*shape),
            op.project(spec["velocity_amplitude"]*shape))


def configured_drive(op, config):
    spec = config["drive"]
    if spec["amplitude"] == 0:
        return None
    field = (spec["amplitude"] *
             np.cos(spec["theta_mode"]*op.theta+spec["phase_theta"]) *
             np.cos(spec["zeta_mode"]*op.zeta+spec["phase_zeta"]))
    weak = op.weak_source(field)
    return lambda t: math.cos(spec["frequency"]*t+spec["phase_time"])*weak


def save_history(path, history):
    samples = history["samples"]
    arrays = {key: np.asarray([row[key] for row in samples]) for key in samples[0]}
    arrays.update(q=history["q"], velocity=history["velocity"])
    atomic_npz(path, **arrays)


def report_history(history):
    rows = history["samples"]
    return {"sample_count": len(rows), "initial_step": rows[0]["step"],
            "final_step": rows[-1]["step"],
            "final": {key: value if key == "step" else exact_float(value)
                      for key, value in rows[-1].items()},
            "max_sampled_absolute_balance_defect": exact_float(
                max(abs(row["balance_defect"]) for row in rows)),
            "diagnostic_note": "maxima are over stored samples, not every intermediate state"}


def prepare_output(path, overwrite=False):
    path = Path(path)
    if path.exists() and any(path.iterdir()) and not overwrite:
        raise SolverError(f"{path} is not empty; choose a new --out or use --overwrite")
    path.mkdir(parents=True, exist_ok=True)
    return path


def spectrum_command(config, out, count):
    op = SurfaceSolver(Model(**config["model"]), Resolution(**config["resolution"]))
    spec = op.spectrum(count)
    atomic_npz(out/"spectrum.npz", eigenvalues=spec.values, eigenvectors=spec.vectors,
               mass=op.M, stiffness=op.K,
               labels=np.array([str(label) for label in op.labels]),
               config=np.array(canonical(config)))
    report = {"task": "spectrum", "environment": environment(), "config": config,
              "geometry": op.geometry_report(), "spectrum": spec.report()}
    write_json(out/"report.json", report)
    return report


def evolve_command(config, out, dt, steps, sample_every, resume=None):
    if resume is None:
        op = SurfaceSolver(Model(**config["model"]), Resolution(**config["resolution"]))
        q, v = configured_initial(op, config)
        state = initial_state(op, q, v, dt)
    else:
        op, state, config = load_checkpoint(resume)
    write_json(out/"config.json", config)
    save_checkpoint(out/"checkpoint.npz", op, state, config)
    drive = configured_drive(op, config)

    def sample_callback(state, sample):
        save_checkpoint(out/"checkpoint.npz", op, state, config)

    try:
        hist = integrate(op, state, steps, drive, config["damping"], sample_every,
                         on_sample=sample_callback)
    except (SolverError, FloatingPointError, np.linalg.LinAlgError) as exc:
        save_checkpoint(out/"checkpoint.npz", op, state, config)
        write_json(out/"failure.json", {"error": str(exc), "last_committed_step": state.step,
                                       "environment": environment(), "config": config})
        raise
    save_history(out/"history.npz", hist)
    report = {"task": "evolve", "environment": environment(), "config": config,
              "geometry": op.geometry_report(), "history": report_history(hist),
              "dt": exact_float(state.dt), "checkpoint": "checkpoint.npz",
              "equation": "M qtt + damping*M qt + K q + quartic*B^T(wK*(Bq)^3) = drive(t)"}
    write_json(out/"report.json", report)
    return report


def equilibrium_command(config, out, max_iter):
    if config["drive"]["amplitude"] != 0:
        raise SolverError("Static equilibrium command requires zero configured drive amplitude")
    op = SurfaceSolver(Model(**config["model"]), Resolution(**config["resolution"]))
    seed, _ = configured_initial(op, config)
    result = equilibrium(op, seed, max_iter=max_iter)
    atomic_npz(out/"equilibrium.npz", q=result["q"], field=op.field(result["q"]),
               eigenvalues=result["hessian_spectrum"].values,
               eigenvectors=result["hessian_spectrum"].vectors,
               theta=op.theta_1d, zeta=op.zeta_1d, config=np.array(canonical(config)))
    report = {"task": "equilibrium", "environment": environment(), "config": config,
              "geometry": op.geometry_report(), "converged": result["converged"],
              "reason": result["reason"], "residual": exact_float(result["residual"]),
              "tolerance": exact_float(result["tolerance"]),
              "energy": exact_float(result["energy"]),
              "stationary_classification": result["stationary_classification"],
              "hessian_spectrum": result["hessian_spectrum"].report(),
              "trace": result["trace"],
              "note": "Stationarity does not imply a global minimum; classification uses the discrete Hessian"}
    write_json(out/"report.json", report)
    return report


def convergence_command(config, out, cutoffs, quadratures, count):
    rows, previous = [], None
    for cutoff in cutoffs:
        r = dict(config["resolution"])
        r.update(theta_cutoff=cutoff, zeta_cutoff=cutoff)
        op = SurfaceSolver(Model(**config["model"]), Resolution(**r))
        sp = op.spectrum(count)
        row = {"kind": "basis", "cutoff": cutoff,
               "quadrature": [r["theta_points"], r["zeta_points"]],
               "spectrum": sp.report(),
               "change_from_previous": None if previous is None else
                   [exact_float(x) for x in sp.values-previous]}
        rows.append(row); previous = sp.values
    previous = None
    for points in quadratures:
        r = dict(config["resolution"])
        r.update(theta_points=points, zeta_points=points)
        op = SurfaceSolver(Model(**config["model"]), Resolution(**r))
        sp = op.spectrum(count)
        rows.append({"kind": "quadrature", "points": points,
                     "cutoff": [r["theta_cutoff"], r["zeta_cutoff"]],
                     "spectrum": sp.report(),
                     "change_from_previous": None if previous is None else
                         [exact_float(x) for x in sp.values-previous]})
        previous = sp.values
    report = {"task": "convergence", "environment": environment(), "config": config,
              "runs": rows, "scope": "observed refinement changes; no interval-certified continuum enclosure"}
    write_json(out/"report.json", report)
    return report


def sweep_command(config, out, parameter, values, count):
    allowed = {"amplitude", "mass2", "potential_amplitude", "potential_constant",
               "lapse_amplitude", "curvature_h2", "curvature_k"}
    if parameter not in allowed:
        raise SolverError(f"sweep parameter must be one of {sorted(allowed)}")
    rows = []
    for value in values:
        m = dict(config["model"]); m[parameter] = value
        op = SurfaceSolver(Model(**m), Resolution(**config["resolution"]))
        rows.append({"parameter": exact_float(value), "spectrum": op.spectrum(count).report()})
    report = {"task": "sweep", "parameter": parameter, "environment": environment(),
              "config": config, "runs": rows,
              "note": "Sorted eigenvalues are reported; individual eigenvector branches are not tracked"}
    write_json(out/"report.json", report)
    return report


def csv_ints(value):
    try:
        result = [int(x) for x in value.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected comma-separated integers") from exc
    if not result or any(x < 0 for x in result):
        raise argparse.ArgumentTypeError("Expected nonnegative integer list")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("spectrum", "evolve", "equilibrium", "converge", "sweep"):
        p = sub.add_parser(command)
        p.add_argument("--config", type=Path)
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--overwrite", action="store_true")
        if command in ("spectrum", "converge", "sweep"):
            p.add_argument("--count", type=int, default=8)
        if command == "evolve":
            p.add_argument("--dt", default="1/200")
            p.add_argument("--steps", type=int, default=1000)
            p.add_argument("--sample-every", type=int, default=10)
        elif command == "equilibrium":
            p.add_argument("--max-iter", type=int, default=100)
        elif command == "converge":
            p.add_argument("--cutoffs", type=csv_ints, default=[2, 3, 4])
            p.add_argument("--quadratures", type=csv_ints, default=[32, 48, 64])
        elif command == "sweep":
            p.add_argument("--parameter", required=True)
            p.add_argument("--values", required=True,
                           help="Comma-separated numbers or fractions; use --values=-1,0,1 for negatives")
    p = sub.add_parser("resume")
    p.add_argument("checkpoint", type=Path)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--steps", type=int, default=1000)
    p.add_argument("--sample-every", type=int, default=10)
    p.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    start = time.perf_counter()
    try:
        out = prepare_output(args.out, args.overwrite)
        config = None if args.command == "resume" else read_config(args.config)
        if args.command == "spectrum":
            report = spectrum_command(config, out, args.count)
        elif args.command == "evolve":
            report = evolve_command(config, out, scalar(args.dt, "dt"),
                                    args.steps, args.sample_every)
        elif args.command == "resume":
            report = evolve_command(None, out, None, args.steps, args.sample_every,
                                    resume=args.checkpoint)
        elif args.command == "equilibrium":
            report = equilibrium_command(config, out, args.max_iter)
        elif args.command == "converge":
            report = convergence_command(config, out, args.cutoffs, args.quadratures, args.count)
        else:
            report = sweep_command(config, out, args.parameter,
                                   [scalar(x) for x in args.values.split(",")], args.count)
        success = report.get("converged", True)
        print(json.dumps({"status": "completed" if success else "not_converged",
                          "report": str(out/"report.json"), "elapsed_seconds": time.perf_counter()-start,
                          "solver_version": VERSION}, allow_nan=False))
        return 0 if success else 2
    except (SolverError, FloatingPointError, np.linalg.LinAlgError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
