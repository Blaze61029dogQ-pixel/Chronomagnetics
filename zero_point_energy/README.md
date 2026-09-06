# Zero-Point Energy: proper mechanics

A runnable transcription of the standard QFT vacuum-energy mechanics
audited in *"Zero-Point Energy: First Principles, Units, and Observables"*
(Revision 5, Lockwood, Cyrek, Burkeen & Hansley, 13 Jul 2026) — mode
counting, the Casimir effect, Casimir-Polder, LC/Josephson zero-point
amplitudes, the dynamical Casimir effect, and Unruh/Hawking temperature —
plus (v2) a numerical validation and parameter-study engine built on top of
that reference layer: finite-temperature Lifshitz theory with real material
models, regulator-independence demonstrations, a numerical Bogoliubov
solver for the dynamical Casimir effect, and a transmon eigensolver. See
`REFERENCES.bib` for bibliographic provenance and `../SCIENTIFIC_VALIDATION.md`
for the full benchmark table.

Unlike the rest of this repository, **this package transcribes mainstream,
textbook-level QFT** (Casimir 1948, Lifshitz 1956, Unruh 1976, Hawking
1975, …), not a speculative construction of this project's own. It exists
as a correctness-audited reference: every quoted formula traces to a
specific `D`-item in the source document, and `report.py` hard-checks the
document's own worked numbers.

## Layout

- `constants.py` — SI constants (ħ, c, e, h, kB exact by the post-2019 SI;
  ε₀ and G measured, carrying their own uncertainty).
- `modes.py` — density of states, spectral energy density, and hard-cutoff
  ZPE density for massless and massive fields (D1–D4, D8–D9, D14–D15,
  D31–D33). The massive case includes both the **exact** closed-form
  integral and the large-cutoff **asymptotic** series — the source
  document is explicit that the series must not be integrated back through
  the infrared (D3 note); use the exact form there.
- `casimir.py` — parallel-plate energy/pressure, the renormalized stress
  tensor, sphere-plate PFA, finite-conductivity correction, high-T limits,
  the Boyer sphere, and the 1D interval/ring scalar (D5, D12, D16, D18,
  D20, D25–D29, D40).
- `casimir_polder.py` — retarded atom-surface potential and force (D56).
- `units.py` — the natural-unit ↔ SI energy-density conversion (D13/S6).
- `resonators.py` — LC-oscillator and Josephson-junction zero-point
  amplitudes (D59, D61).
- `dynamical_casimir.py` — driven-boundary photon pair production (D7,
  D57, D62); the source document stresses this is boundary-driven, not
  extraction from a stationary vacuum.
- `stress_tensor.py` — the vacuum equation of state `p = -rho` and
  `T^mu_nu = rho * g^mu_nu` (D6/D10).
- `thermal.py` — Unruh temperature, Hawking temperature and evaporation
  time, chiral-CFT thermal flux, and the Schwinger pair-production rate
  (D37, D71–D75).
- `report.py` — hard-checks this transcription against the source
  document's own worked numbers (Casimir pressure at 100 nm, the GeV⁴↔J/m³
  conversion, the LC zero-point identities, …) plus independent real-world
  sanity checks (solar-mass Hawking temperature and evaporation time,
  electron Schwinger field). Run with:

  ```
  python3 -m zero_point_energy.report
  ```

### v2 additions (Lifshitz, renormalization, DCE, transmon)

- `materials.py` — dielectric response ε(iξ) on the imaginary (Matsubara)
  frequency axis: `PerfectConductor`, `PlasmaModel`, `DrudeModel`,
  `LorentzModel` (single- or multi-oscillator), and `UserDielectric` for a
  validated user-supplied callable. Every model implements
  `epsilon_xi_squared(xi)` — ε(iξ)·ξ² via its own analytic ξ→0 limit —
  because ε(0) is genuinely infinite for any conducting model and
  `epsilon(xi)*xi**2` would be an inf·0 indeterminate form there.
- `lifshitz.py` — the finite-temperature planar Lifshitz free energy per
  unit area (Matsubara sum, n=0 at the documented half weight, TE/TM
  Fresnel coefficients from `materials.py`), plus a separately-taken T→0
  limit (`zero_temperature_free_energy_per_area`) rather than a
  finite-T evaluation at a tiny T. Uses a dimensionless x=2·κ₀·a
  substitution and `log1p` for numerical stability.
- `renormalization.py` — demonstrates regulator independence on the
  massless-scalar 1D Dirichlet-interval benchmark (E_C=-πħc/(24L)) via four
  independent routes (exponential cutoff, mode-sum-minus-continuum, zeta
  regularization, Abel-Plana), using mpmath at 50 digits where a
  regulator-dependent divergent piece must be subtracted from a finite
  remainder.
- `dce_solver.py` — numerically integrates a parametrically driven quantum
  harmonic mode and extracts Bogoliubov α, β by mode-matching against a
  required constant-frequency asymptotic region, verifying the canonical
  identity |α|²−|β|²=1 and an explicit energy ledger (drive work in,
  dissipation out). Complements, and does not replace, the
  weak-pump/perturbative formulas already in `dynamical_casimir.py`.
- `transmon.py` — exact numerical diagonalization of the truncated
  charge-basis Cooper-pair-box/transmon Hamiltonian, plus the large-E_J/E_C
  asymptotic approximation as a labeled comparison, not a replacement.

#### Finite-temperature Lifshitz theory

`lifshitz.finite_temperature_free_energy_per_area(a, T, material1,
material2=None)` implements Lifshitz (1956)'s free energy between two
(possibly dissimilar) planar half-spaces:

```
F/A = (kB*T/2*pi) * sum'_n integral_0^inf k_perp dk_perp
          [ln(1 - r_TE1*r_TE2*e^(-2*kappa_0*a)) + ln(1 - r_TM1*r_TM2*e^(-2*kappa_0*a))]
```

with Matsubara frequencies ξ_n=2πn·kB·T/ħ. `zero_temperature_free_energy_per_area`
takes T→0 analytically (the Matsubara sum becomes an integral over ξ) rather
than evaluating the sum at a very small T, and reproduces Casimir (1948)'s
ideal-conductor E/A to ~6e-16 relative error.

#### Imaginary-frequency material response

`materials.py`'s dielectric models are evaluated at ξ≥0 (never at a real,
oscillating frequency) — this is the representation the Lifshitz formula
is naturally written in, avoiding any resonance poles on the contour.

#### TE/TM reflection coefficients

`lifshitz.reflection_te`/`reflection_tm` (or `material.reflection_coefficients`)
implement the standard nonmagnetic Fresnel forms (Bordag, Mohideen &
Mostepanenko 2001):

```
kappa_0 = sqrt(k_perp^2 + xi^2/c^2)          kappa = sqrt(k_perp^2 + eps(i*xi)*xi^2/c^2)
r_TM = (eps*kappa_0 - kappa)/(eps*kappa_0 + kappa)     r_TE = (kappa_0 - kappa)/(kappa_0 + kappa)
```

#### Matsubara zero mode

The n=0 term is always treated explicitly, never epsilon-regularized away.
Its value depends on lim_{ξ→0} ε(iξ)·ξ², which differs by model:

| Model | ε(iξ)·ξ² as ξ→0 | r_TE(ξ=0) |
|---|---|---|
| Perfect conductor | (bypassed — r_TE=-1, r_TM=+1 identically) | -1 |
| Plasma | ω_p² (finite, nonzero) | ≠0, → -1 as k_perp→0 |
| Drude | 0 | 0, for every k_perp |

#### Drude versus plasma

This is a genuinely unresolved prescription choice in the literature, not
settled here: the Drude model's vanishing TE zero mode halves the classical
high-temperature Casimir pressure relative to the ideal-conductor/plasma
value (F/A → -ζ(3)kBT/(8πa³) vs. -ζ(3)kBT/(4πa³); D28 in the source
document; verified numerically in `tests/test_lifshitz.py` to ~2e-8
relative error against both closed forms). See Klimchitskaya, Mohideen &
Mostepanenko (2009), Sec. V, and Brevik, Ellingsen & Milton (2006) for a
neutral survey of the experimental and theoretical arguments; both
prescriptions are implemented and a calculation's `LifshitzResult` records
which materials (and hence which prescription) were used.

#### Numerical convergence and regulator independence

The Lifshitz k_perp integral uses a dimensionless x=2κ₀a substitution with
`scipy.integrate.quad`; the Matsubara sum terminates on an explicit
consecutive-small-term criterion (never a fixed, undocumented cutoff) and
reports `converged`, `n_matsubara_terms`, and `max_quadrature_error`.
`renormalization.py` shows the same finite Casimir energy emerging from
four unrelated regularization routes, and `tests/test_renormalization.py`
verifies the exponential-cutoff route's error shrinks quadratically as its
regulator is removed, using mpmath specifically to avoid the
two-nearly-equal-numbers cancellation problem at small regulator values
(see that module's PRECISION NOTE).

#### DCE Bogoliubov solver

`dce_solver.bogoliubov_coefficients` solves q̈+2γq̇+ω(t)²q=0 from
vacuum-normalized positive-frequency initial data and matches the result
against the final constant-frequency plane-wave basis. `windowed_sinusoidal_omega`
(a resonant periodic drive with a smooth envelope) and `smooth_ramp_omega`
(a slow, non-periodic frequency ramp) are *not* interchangeable: only the
latter demonstrates the adiabatic theorem (excitation suppressed as the
ramp slows); a long *resonant* drive amplifies exponentially regardless of
how gently it switches on.

#### DCE energy source

`dce_solver.energy_ledger` independently integrates dE/dt = ħωω̇|q|² −
ħ·2γ|q̇|² along the trajectory and checks it against the endpoint energy
change (closes to ~1e-8–1e-11 relative error in testing). As throughout
this package: **dynamical Casimir photon production is powered by the
external drive; it is not stationary-vacuum energy extraction** (D34, D57
in the source document; restated explicitly in `dce_solver.py`'s own
docstring).

#### Transmon solver

`transmon.diagonalize` exactly diagonalizes the truncated charge-basis
Hamiltonian (Koch et al. 2007); `transmon.asymptotic_energies` is a
separately-derived large-E_J/E_C comparison (not the solver). Reproduces
two textbook transmon signatures: anharmonicity → -E_C (though the
convergence is empirically slow, ~1/√(E_J/E_C), not exponential — see
`SCIENTIFIC_VALIDATION.md`) and exponentially suppressed charge dispersion.
Not coupled to any `chronometrics` assumption (see Architecture, below).

#### Validation commands

```
python3 -m zero_point_energy.report      # 15 locked checks against the source document
python3 -m pytest -vv                    # full suite (report.py checks + all module tests)
```

## Status discipline

Every function's docstring names the `D`-item it transcribes and states
its regime of validity (e.g. the massive-field asymptotic series is only
valid for cutoff ≫ mc/ħ; the plasma-model conductivity correction's
coefficient is specific to a nondissipative, zero-temperature model). Sign
conventions are kept explicit rather than implicit: bosons contribute
`+g`, fermions `-g`; the Casimir pressure and Casimir–Polder force are
negative (attractive); the vacuum stress tensor uses signature `(+---)`.

## Architecture: the epistemic firewall

This repository keeps three sectors strictly separated:

- **`zero_point_energy/`** (this package) — standard QFT, Casimir/Lifshitz
  theory, circuit QED, and numerical mathematical physics. Every
  nontrivial formula traces to a cited, mainstream source (see
  `REFERENCES.bib` and `SCIENTIFIC_VALIDATION.md`'s traceability table).
- **`chronometrics/`** — this project's own speculative hypotheses (log-time
  phase laws, the chronomagnetic-contortion construction, etc.), explicitly
  disclaimed in its own README as "not physics."
- **`experiments/`** — numerical hypothesis tests and cross-sector
  investigations (e.g. `junction_log_periodic_simulation.py`, which uses a
  `chronometrics`-motivated but explicitly-labeled placeholder "chronomagnetic
  rate" and reports its own falsification criteria honestly, pass or fail).

**No file under `zero_point_energy/` imports from, or bakes in an
assumption from, `chronometrics/` or `experiments/`** — checked by
inspection for this branch (`materials.py`, `lifshitz.py`,
`renormalization.py`, `dce_solver.py`, and `transmon.py` import only from
`zero_point_energy.constants` and each other, plus `numpy`/`scipy`/`mpmath`).
If a future addition wants to couple the two layers, the speculative layer
may *consume* outputs from `zero_point_energy/` (e.g. a Chronometrics model
citing a validated Casimir number); `zero_point_energy/` must never import
`chronometrics/` or redefine a mainstream result to match a Chronometrics
expectation.

## Boundary statement

This package computes standard, experimentally-tested QFT vacuum-energy
effects (the Casimir force has been measured to percent-level precision;
Hawking/Unruh temperature and the dynamical Casimir effect are
theoretically established and, for the latter, observed in superconducting
circuits). It does **not** endorse using zero-point energy as a source of
extractable power, a mechanism for gravity or inertia, or a stationary
vacuum-fluctuation "engine": the source document itself devotes D34, D57,
and D77 to why passivity forbids net work from an undriven vacuum, why the
dynamical Casimir effect is powered entirely by its drive, and why the
historical zero-point-field gravity/inertia proposals (Puthoff; Haisch–
Rueda–Puthoff) were shown incorrect by Carlip (1993) and Levin (2009).
