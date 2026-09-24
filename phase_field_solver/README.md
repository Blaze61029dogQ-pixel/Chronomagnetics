# Geometry Coupled Phase Field Solver

## Version 1.0.0 — runnable CPU release

This package implements a specialized, variational Fourier Galerkin solver for a real scalar field on a prescribed periodic corrugated tube, with a static positive lapse, an external scalar potential, optional curvature dependent coefficients, and a quartic self interaction. It includes linear spectra, nonlinear time evolution, forced and damped evolution, stationary equilibria, refinement studies, parameter sweeps, and restartable checkpoints.

**The implementation was executed and passed all 30 verification tests.** Eight example jobs completed, including a nonlinear wave, a nonuniform equilibrium, a driven restart, and two independent forms of spatial refinement. The exact recorded results are in VALIDATION.md and results/. The full expanded theory document is included in docs/THEORY_MONOGRAPH.md.

The computational scope is a fixed 2+1 dimensional background. The code does not solve Einstein equations, spinor equations, a moving membrane, or a bulk three dimensional field. The executed tests verify the implementation within that scope; they are not physical validation or interval certified continuum error bounds.

## Start here

Extract the ZIP, then open a terminal inside the extracted Phase_Field_Solver folder. These are ordinary Python scripts; no notebook, GPU, CUDA, driver changes, or external service is required.

A compatible Python installation with NumPy and SciPy is required. The recorded environment was Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0 on Linux. Native Windows execution uses the same scripts, but was not separately executed here.

In Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-tested.txt
.\.venv\Scripts\python.exe verify_solver.py --out my_verification.json
.\.venv\Scripts\python.exe phasefield.py spectrum --config examples/corrugated.json --out my_spectrum
```

Using the environment's Python executable directly avoids any PowerShell activation policy change. If your Python launcher uses a different installed compatible version, select that interpreter instead. The requirements-tested file fixes the two numerical library versions used for this release; requirements.txt provides wider compatibility ranges that have not all been tested.

On Linux or WSL:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-tested.txt
.venv/bin/python verify_solver.py --out my_verification.json
.venv/bin/python phasefield.py spectrum --config examples/corrugated.json --out my_spectrum
```

The remaining examples use python to mean the Python executable of that environment. On Windows, substitute .\.venv\Scripts\python.exe when needed. Each command writes its results to the directory named by --out. Choose an empty directory for each run; an existing nonempty directory requires explicit --overwrite. Prefer a new directory to keep earlier run evidence.

## Commands you can run immediately

Compute nine squared frequencies and mass normalized eigenvectors:

```bash
python phasefield.py spectrum --config examples/corrugated.json --count 9 --out my_spectrum
```

Evolve a nonlinear wave for 1,000 steps with timestep 1/200 and store every tenth step:

```bash
python phasefield.py evolve --config examples/corrugated.json --dt 1/200 --steps 1000 --sample-every 10 --out my_wave
```

Find a nonuniform broken symmetry stationary state:

```bash
python phasefield.py equilibrium --config examples/broken_equilibrium.json --out my_equilibrium
```

Evolve with forcing and damping, then continue the same trajectory:

```bash
python phasefield.py evolve --config examples/driven.json --dt 1/200 --steps 400 --sample-every 20 --out my_driven
python phasefield.py resume my_driven/checkpoint.npz --steps 200 --sample-every 20 --out my_resumed
```

Study basis cutoff and quadrature refinement separately:

```bash
python phasefield.py converge --config examples/corrugated.json --cutoffs 2,3,4,5 --quadratures 32,48,64 --count 8 --out my_refinement
```

Sweep the amplitude of the external potential:

```bash
python phasefield.py sweep --config examples/potential.json --parameter potential_amplitude --values 0,1/40,1/20,1/10,1/5 --count 6 --out my_sweep
```

To reproduce all eight packaged examples with one command:

```bash
python run_examples.py --out my_runs
```

The runner also writes a fresh verification receipt and stops at the first failed command. It will not overwrite an existing output directory. The packaged results were generated with the same example settings.

For all options:

```bash
python phasefield.py --help
python phasefield.py evolve --help
```

## What each result means

| Command | Files | Interpretation |
|---|---|---|
| spectrum | report.json, spectrum.npz | Linearization about zero; eigenvalues are squared coordinate time frequencies, with multiplicities retained |
| evolve | report.json, history.npz, checkpoint.npz, config.json | Nonlinear trajectory, sampled energy and work diagnostics, and latest committed checkpoint |
| equilibrium | report.json, equilibrium.npz | A stationary point found from the supplied seed, its residual, and its discrete Hessian spectrum |
| converge | report.json | Separate changes under basis and quadrature refinement |
| sweep | report.json | Sorted eigenvalues at each parameter value; individual branches are not tracked |
| resume | Same as evolve | Additional steps with the checkpoint's source, operator, timestep, and configuration |

A negative squared frequency represents a linear instability. The report retains it and reports a real growth rate. Values within a numerical zero tolerance are explicitly unresolved. A small algebraic eigensolver residual verifies the finite matrix problem; it does not measure spatial truncation error.

A successful equilibrium residual check does not imply a minimum. Inspect stationary_classification as well as converged. A positive smallest discrete Hessian eigenvalue supports a local minimum in the retained finite dimensional space; it does not establish a global minimum or exclude unstable directions outside that space. An exactly zero seed can stay at an unstable zero stationary point.

The source configuration is a physical source on the right side of the positive time evolution equation in docs/NUMERICAL_METHOD.md. Internally it is converted to a weak force covector. The sign of a source added to a covariant equation must be reconciled with that convention.

## Initial data and normalization

For initial.kind = cosine, the physical field is

$$
\phi(0,\theta,\zeta)=\mathrm{offset}
+\mathrm{amplitude}\cos(l\theta+\alpha)\cos(p\zeta+\beta).
$$

The initial velocity is the same cosine profile times velocity_amplitude. For constant data, the profile is one. These fields are projected with the mass weighted inner product.

For eigenmode data, amplitude and velocity_amplitude multiply an M normalized eigenvector. They are modal coefficients, not a prescribed peak field amplitude. mode_index is zero based in the sorted spectrum. offset and the cosine phase/mode settings are not used for this initial kind. Eigenvectors within a degenerate eigenspace need not have a reproducible orientation.

The spectrum command uses the linearization about zero even when quartic is nonzero. To study a nonzero stationary background, use the Hessian spectrum produced by equilibrium, or call op.spectrum(count, background=q) in Python.

## Read and reconstruct saved data

```python
import json
import numpy as np
from phasefield import Model, Resolution, SurfaceSolver

with open("results/nonlinear_wave/config.json", encoding="utf-8") as handle:
    config = json.load(handle)

op = SurfaceSolver(Model(**config["model"]), Resolution(**config["resolution"]))
with np.load("results/nonlinear_wave/history.npz", allow_pickle=False) as data:
    time = data["time"].copy()
    q_final = data["q"][-1].copy()
    velocity_final = data["velocity"][-1].copy()
    energy = data["energy"].copy()
    defect = data["balance_defect"].copy()

field_final = op.field(q_final)
assert field_final.shape == (op.resolution.theta_points, op.resolution.zeta_points)
print("Final energy:", float(energy[-1]).hex())
```

history.npz stores one row per recorded sample, not every integration step. q and velocity are coefficients in the real tensor basis documented in the method guide. theta is the first field array axis and zeta the second. Periodic endpoint samples are omitted. In a resumed history, the first row is the checkpoint state and the reported work, dissipation, and energy defect remain cumulative from the original initial state.

NPZ files contain ordinary numeric or Unicode arrays and are read with allow_pickle=False. JSON numbers use a representation that round trips to the same Python binary64 value. Key diagnostics additionally include the exact decimal expansion and hexadecimal representation of the stored binary64 value. Those extra digits describe the stored number; they do not claim extra numerical accuracy.

## Python API example

```python
import numpy as np
from phasefield import Model, Resolution, SurfaceSolver, initial_state, integrate

op = SurfaceSolver(
    Model(amplitude="1/10", mass2="1/4", quartic="1/2"),
    Resolution(theta_cutoff=4, zeta_cutoff=4, theta_points=48, zeta_points=48),
)
q0 = op.project(0.2 * np.cos(op.theta) * np.cos(op.zeta))
state = initial_state(op, q0, dt=1/200)
history = integrate(op, state, steps=1000, sample_every=10)
field = op.field(state.q)
```

An API drive callback receives the coordinate time and must return a real vector of length op.ndof representing the weak force. Use op.weak_source(sampled_physical_source) to construct that vector. Use op.project only for projection of fields or velocities. These two operations have different meanings and weights.

## Compute cost and practical settings

This release deliberately assembles dense variational matrices. With cutoffs Ktheta and Kzeta, there are D = (2 Ktheta + 1)(2 Kzeta + 1) real degrees of freedom and Q = Qtheta Qzeta quadrature points. Basis storage is O(QD), assembly is O(QD²), dense factorizations and generalized eigenvalue solves have O(D³) work, and one explicit evolution step has O(QD + D²) work. Requesting a small number of eigenvalues does not make this a sparse or matrix free solver.

Default cutoffs are 4 in both directions, giving 81 real degrees of freedom. The default grid has 48 by 48 points. The code checks an estimated memory budget before operator construction and accounts separately for sampled trajectory storage. That estimate is a guard, not an operating system memory cap. Native libraries and allocation peaks can use additional memory.

Use one BLAS thread for small reproducible verification jobs when convenient. In PowerShell set $env:OPENBLAS_NUM_THREADS="1"; in a POSIX shell set OPENBLAS_NUM_THREADS=1 before launching Python. This is optional; the solver does not change your drivers or system configuration.

Increase quadrature and basis separately before interpreting a result as spatially converged. Decrease timestep separately before interpreting a nonlinear trajectory as temporally converged. The built in timestep guard detects an excessive local stiffness scale, but it is not a substitute for an accuracy study or a global nonlinear stability proof.

## Package contents

| Path | Purpose |
|---|---|
| phasefield.py | Solver, configuration validation, spectra, time integration, equilibria, checkpointing, command line |
| verify_solver.py | 30 executable checks with independent exact limits and recorded numerical metrics |
| run_examples.py | Reproduction runner that stops on an error |
| requirements-tested.txt | NumPy and SciPy versions actually used |
| requirements.txt | Broader declared dependency ranges |
| examples/ | Six editable JSON configurations |
| results/verification.json | Executed test receipt with environment and solver source hash |
| results/*/ | Eight executed example result sets |
| docs/NUMERICAL_METHOD.md | Continuum model, derivation, discrete equations, algorithms, and error interpretation |
| docs/CONFIGURATION.md | Complete generated configuration defaults and parameter interpretation |
| docs/THEORY_MONOGRAPH.md | Full expanded theoretical document supplied with the project |
| VALIDATION.md | Readable record of executed checks and example diagnostics |
| MANIFEST.sha256 | SHA256 hashes of release files, excluding the manifest itself |

The theory monograph includes a broader research program and earlier verification material. The supported executable contract for this release is phasefield.py plus NUMERICAL_METHOD.md. Statements or proposed extensions in the monograph are not a claim that every sector is implemented.

## Limits of this release

All computations use binary64, with no arbitrary precision or interval arithmetic. Geometry and lapse are prescribed and static. The field is real. Boundary conditions are periodic in both coordinates, with no open ends, axis regularity condition, absorbing boundary, or topology change. Negative quartic couplings are rejected. Time integration uses a fixed timestep; it has no automatic timestep or basis adaptation. Equilibrium search is local and does not enumerate every branch.

The axial period is a quotient of a straight tube by translation. It is not an ordinary embedded doughnut shaped torus in Euclidean three space. Curvature is computed from the local corrugated tube embedding; the intrinsic metric descends to the periodic quotient.

Checkpoint restart requires an unchanged solver source hash, solver version, operator fingerprint, and compatible numerical data. Byte identical split versus continuous execution was checked in the recorded environment. Cross platform byte identity is not promised. A checksum detects accidental change; it is not authentication of an untrusted file.

No performance claim against another solver, physical measurement match, continuum certification, gravitational backreaction, or experimental feasibility claim follows from these test results.
