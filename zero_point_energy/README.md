# Zero-Point Energy: proper mechanics

A runnable transcription of the standard QFT vacuum-energy mechanics
audited in *"Zero-Point Energy: First Principles, Units, and Observables"*
(Revision 5, Lockwood, Cyrek, Burkeen & Hansley, 13 Jul 2026) — mode
counting, the Casimir effect, Casimir-Polder, LC/Josephson zero-point
amplitudes, the dynamical Casimir effect, and Unruh/Hawking temperature.

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

## Status discipline

Every function's docstring names the `D`-item it transcribes and states
its regime of validity (e.g. the massive-field asymptotic series is only
valid for cutoff ≫ mc/ħ; the plasma-model conductivity correction's
coefficient is specific to a nondissipative, zero-temperature model). Sign
conventions are kept explicit rather than implicit: bosons contribute
`+g`, fermions `-g`; the Casimir pressure and Casimir–Polder force are
negative (attractive); the vacuum stress tensor uses signature `(+---)`.

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
