# Scientific validation: zero_point_energy v2

This file records what was actually run and what the numbers actually
were, at the time of the ZPE v2 (Lifshitz / renormalization / DCE /
transmon) branch. Every value below came from executing the corresponding
function in this repository; none was written from memory or hand-waved.
Reproduce any row with the command shown under it, or run the full suite:

```
python3 -m zero_point_energy.report
python3 -m pytest -vv
```

## Benchmark table

| Quantity | Analytic / reference value | Numerical value (this branch) | Relative error | Tolerance | Status |
|---|---|---|---|---|---|
| Casimir parallel plates, E/A (a=1 μm) | -π²ħc/(720a³) = -4.3337525775e-10 J/m² | -4.3337525775e-10 J/m² (Lifshitz T→0, `zero_temperature_free_energy_per_area`) | 5.965e-16 | 1e-10 | PASS |
| Casimir parallel plates, P (a=1 μm) | -π²ħc/(240a⁴) = -1.3001257732e-03 Pa | -1.3001258166e-03 Pa (central-difference of the same Lifshitz F/A) | 3.333e-08 | 1e-6 | PASS |
| Scalar 1D Casimir energy (L=1 mm), zeta route | -πħc/(24L) = -4.1384288691e-24 J | -4.1384288691e-24 J | 0.0 (mpmath zeta vs. the pre-existing hard-coded fraction) | 1e-10 | PASS |
| Scalar 1D Casimir energy (L=1 mm), exponential-cutoff route | same | -4.1384288691e-24 J | 5.006e-14 | 1e-10 | PASS |
| Scalar 1D Casimir energy (L=1 mm), Abel-Plana route | same | -4.1384288691e-24 J | 1.775e-16 | 1e-10 | PASS |
| Lifshitz ideal-conductor high-T classical limit vs. D28 | -ζ(3)kBT/(4πa³) | matches `casimir.high_temperature_pressure_ideal` | ~2e-8 (see test_lifshitz.py) | 1e-5 | PASS |
| Lifshitz Drude high-T classical limit vs. D28 (half the ideal value) | -ζ(3)kBT/(8πa³) | matches `casimir.high_temperature_pressure_drude`; Drude/ideal ratio = 0.500000000003 | ~2e-8 | 1e-5 | PASS |
| DCE constant-frequency Bogoliubov beta | 0 (exact, unitary, no drive) | \|β\| = 3.07e-15, N=9.416e-30 | n/a (absolute) | N < 1e-20 | PASS |
| DCE canonical identity, undamped, resonant drive (ε=0.05, 30 periods) | \|α\|²-\|β\|²-1 = 0 | relative residual 1.80e-12 | 1.80e-12 | 1e-8 | PASS |
| DCE energy ledger closure, undamped | ΔE_mode = drive work | relative error 8.68e-11 (a different ε/duration than the row above; see test_dce_solver.py) | 8.68e-11 | 1e-6 | PASS |
| DCE energy ledger closure, damped (γ=0.02ω₀) | ΔE_mode = drive work − dissipated | relative error ~2.4e-8 (test parameters) | 2.4e-8 | 1e-5 | PASS |
| LC zero-point identity V_zpf = ω₀Φ_zpf = Q_zpf/C | exact | residual 0.0 / -3.3e-24 (float roundoff) | ~1e-27 | 1e-12 | PASS |
| Transmon anharmonicity (E_J/E_C=100), exact vs. asymptotic -E_C | -E_C = -0.2 | exact: -0.219099 | 9.5% (slow, ~1/√(E_J/E_C) convergence -- see below) | n/a (documented trend, not a pass/fail number) | PASS (trend) |
| Transmon charge-basis truncation, n_max=20 vs n_max=30 | converged | max eigenvalue diff 3.55e-15 | 3.55e-15 | 1e-8 | PASS |
| Pre-existing report.py locked checks (15 items) | see zero_point_energy/report.py | all 15 unchanged from the pre-branch baseline | see report.py | as defined in report.py | PASS |

Reproduce the Lifshitz/renormalization/DCE/transmon rows:

```python
import math
from zero_point_energy.casimir import plate_energy_per_area, plate_pressure, scalar_interval_energy
from zero_point_energy.lifshitz import zero_temperature_free_energy_per_area, pressure
from zero_point_energy.materials import PerfectConductor
from zero_point_energy.renormalization import renormalized_casimir_energy_1d_interval
from zero_point_energy.dce_solver import bogoliubov_coefficients, windowed_sinusoidal_omega, resonant_drive_frequency
from zero_point_energy.transmon import diagonalize, energies_vs_truncation
from zero_point_energy.constants import C_LIGHT

a = 1e-6
pc = PerfectConductor()
lif = zero_temperature_free_energy_per_area(a, pc, xi_max=50 * C_LIGHT / a)
print(lif.free_energy_per_area, plate_energy_per_area(a))
```

## Transmon anharmonicity convergence (observed, not assumed)

The asymptotic formula's relative error tracks close to 1/sqrt(E_J/E_C),
not an exponentially fast approach -- discovered while writing
`tests/test_transmon.py`, whose thresholds were then set from this
observed trend rather than an initial (wrong) assumption of fast
convergence:

| E_J/E_C | \|exact − (−E_C)\| / E_C |
|---|---|
| 50 | 14.9% |
| 200 | 6.4% |
| 1000 | 2.65% |
| 5000 | 1.15% |

## Lifshitz plasma-to-ideal-conductor convergence (observed)

The relative error between a `PlasmaModel` and `PerfectConductor` T→0
energy (a=1 μm) scales empirically close to linearly in 1/ω_p over the
tested range (each 100× increase in ω_p cuts the error by a consistent
factor near 100, confirmed across two independent decades in
`tests/test_lifshitz.py`):

| ω_p (rad/s) | relative error vs. ideal conductor |
|---|---|
| 1e18 | 1.20e-3 |
| 1e21 | 1.20e-6 |
| 1e23 | 1.20e-8 |
| 1e25 | 1.20e-10 |

## Formula-to-source traceability

| Implementation | Physical result | Equation/convention | Primary reference | Secondary/review reference | Validation test | Status |
|---|---|---|---|---|---|---|
| `casimir.py` (pre-existing) | Ideal parallel-plate Casimir energy/pressure | E/A=-π²ħc/(720a³), P=-π²ħc/(240a⁴) | Casimir 1948 | Bordag, Mohideen & Mostepanenko 2001 | `tests/test_casimir.py`, `zero_point_energy/report.py` | PASS |
| `materials.py` | Plasma dielectric function | ε(iξ)=1+ω_p²/ξ² | -- (standard Drude/plasma electrodynamics) | Bordag et al. 2001, Klimchitskaya et al. 2009 | `tests/test_materials.py` | PASS |
| `materials.py` | Drude dielectric function | ε(iξ)=1+ω_p²/[ξ(ξ+γ)] | -- (standard Drude electrodynamics) | Klimchitskaya et al. 2009, Brevik et al. 2006 | `tests/test_materials.py` | PASS |
| `materials.py` | Drude-vs-plasma TE zero mode | ε(iξ)ξ² → 0 (Drude) vs. → ω_p² (plasma) as ξ→0 | -- (derived here from the model definitions) | Klimchitskaya et al. 2009 (Sec. V), Brevik et al. 2006 | `tests/test_lifshitz.py`, `tests/test_materials.py` | PASS |
| `materials.py` | Lorentz oscillator model, S_j = ω_pj² convention | ε(iξ)=ε_∞+Σ S_j/(ω_j²+ξ²+γ_jξ) | -- (standard oscillator-strength continuation) | Bordag et al. 2001 (Sec. 2.3), Klimchitskaya et al. 2009 (Sec. II.C) | `tests/test_materials.py` | PASS |
| `lifshitz.py` | Finite-temperature planar Lifshitz free energy | Matsubara TE/TM representation, n=0 half weight | Lifshitz 1956 | Bordag et al. 2001 | `tests/test_lifshitz.py` | PASS |
| `renormalization.py` | Regulator-independent 1D Casimir energy | 4 independent regularization routes | -- (standard mode-counting/zeta methods) | Riemann 1859 (zeta), Elizalde et al. 1994 (regularization) | `tests/test_renormalization.py` | PASS |
| `dce_solver.py` | Bogoliubov particle production, parametric oscillator | N=\|β\|², canonical identity \|α\|²-\|β\|²=1 | -- (standard mode-matching, original code) | Dodonov 2010; experimental: Wilson et al. 2011 | `tests/test_dce_solver.py` | PASS |
| `transmon.py` | Cooper-pair-box/transmon Hamiltonian, exact diagonalization | H=4E_C(n-n_g)²-E_J cos(φ) | Koch et al. 2007 | -- | `tests/test_transmon.py` | PASS |
| `transmon.py` | Large-E_J/E_C asymptotic energies | E_m≈-E_J+√(8E_JE_C)(m+½)-(E_C/12)(6m²+6m+3) | Koch et al. 2007 (regime); derived here via quartic perturbation theory | -- | `tests/test_transmon.py` | PASS |

## Known limitations

- The Lifshitz `pressure()` helper differentiates the free energy
  numerically (central difference); it is not a separately re-derived
  analytic pressure formula per material, and its accuracy (validated to
  ~1e-6 relative against the perfect-conductor T→0 benchmark above) is
  set by the finite-difference step, not the underlying quadrature.
- The Drude-vs-plasma TE zero-mode prescription is a genuinely unresolved
  modeling choice in the literature (Klimchitskaya et al. 2009, Sec. V;
  Brevik et al. 2006); this package implements both and reports which was
  used, taking no side.
- `dce_solver.py`'s Bogoliubov extraction requires an actual constant-
  frequency asymptotic region on each end (`require_constant_regions=True`
  by default); it does not define alpha/beta for a frequency profile that
  is still changing at the matching time.
- The transmon asymptotic formula converges to the exact anharmonicity
  slowly (see table above); it should not be treated as accurate much
  below E_J/E_C ~ 100 or so, and even at E_J/E_C=5000 it is only accurate
  to ~1%.
- `REFERENCES.bib`'s Klimchitskaya et al. 2009, Brevik et al. 2006, and
  Elizalde et al. 1994 entries were not independently re-verified against
  a live catalog/DOI resolver in this session (no network access to one);
  each entry's note says so explicitly rather than presenting the
  citation as independently confirmed.
- `experiments/junction_log_periodic_simulation.py`'s own falsification
  criteria currently report FAIL for its frequency-match and spectral-
  purity criteria at the parameters checked into the repository (see that
  file's own output) -- left as-is, since it is an explicitly falsifiable
  Chronometrics hypothesis test, not a zero_point_energy invariant.
