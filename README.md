# Chronomagnetics

Author: James Lockwood

> **REDUCED-ORDER ARCHITECTURE FREEZE — NOT EXPERIMENTALLY VALIDATED.**
> Every numerical result in this repository belongs to a reduced-order,
> internally-audited, or transcribed model unless a package explicitly
> states otherwise. No 3-D tensor finite-element model and no experiment
> has been performed for `d067_art_v1`. See each package's Status/Boundary
> section before relying on any number here.

Three independent research constructions, each transcribed into a
runnable, self-checking Python package. Each package's `report.py` prints
a full accounting and hard-checks its computed values against its source
document's own worked numbers, rather than asking the reader to trust an
external claim.

## Packages

- **[`chronometrics/`](chronometrics/README.md)** — a self-contained,
  internally-audited mathematical registry built from one exact triangle
  (144, 138, 116): Brocard phase, exact q-screen leakage defect, frozen
  log-time phase law, locked recurrence-gate/spectral-operator model,
  the dark-to-bright chronometric separation, and a geophysical bridge.
  Explicitly **not** a confirmed physical law — see its README's status
  tags and boundary statement.
- **[`zero_point_energy/`](zero_point_energy/README.md)** — a
  correctness-audited transcription of mainstream, textbook QFT
  vacuum-energy mechanics (Casimir effect, Casimir-Polder, dynamical
  Casimir effect, Unruh/Hawking temperature), auditing the source
  document *"Zero-Point Energy: First Principles, Units, and
  Observables"* (Lockwood, Cyrek, Burkeen & Hansley). Mainstream physics,
  not speculative.
- **[`d067_art_v1/`](d067_art_v1/README.md)** — **D067-ART-v1**, an
  Adaptive Resonance Tracked phononic-piezoelectric light source.
  Documents a program that screened 100 phononic metacrystal families and
  closed on a reduced-order architecture (nested inertial resonator +
  PZT-5A transducer + adaptive resonance tracking) after rejecting a
  passive fixed-frequency design on manufacturing-robustness grounds.
  **Reduced-order architecture freeze — not experimentally validated.**
  The full monograph is in
  [`docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf`](docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf).

## Running the self-checks

```
python3 -m chronometrics.report
python3 -m zero_point_energy.report
python3 -m d067_art_v1.report
```

## License

Source code (all `*.py` files) is licensed under [MIT](LICENSE).
Research/documentation content (README.md files, the monograph PDF, and
the mathematical framework and derivations they describe) is licensed
under [CC BY 4.0](LICENSE-CC-BY-4.0.md).

## Citation

See [`CITATION.cff`](CITATION.cff) for citation metadata covering all
three packages.
