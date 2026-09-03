# Chronomagnetics

> **REDUCED-ORDER ARCHITECTURE FREEZE — NOT EXPERIMENTALLY VALIDATED.**
> Every numerical result in this repository belongs to a reduced-order
> or transcribed model unless a package explicitly states otherwise. No
> 3-D tensor finite-element model and no experiment have been performed
> for `d067_art_v1`. See each package's Status/Boundary section before
> relying on any number here.

A collection of self-contained, runnable computational studies. Each
package transcribes and self-checks a source document's own worked
numbers rather than asking the reader to trust an external claim.

## Packages

- [`chronometrics/`](chronometrics/) — the chronomagnetics chronometric
  registry (Brocard phase, q-screen constant, recurrence-gate/spectral
  operator, dark-to-bright separation, and a geophysical bridge). This is
  a closed internal chronometric object, not a confirmed physical law.
- [`zero_point_energy/`](zero_point_energy/) — mainstream, textbook-level
  QFT vacuum-energy mechanics (Casimir, Casimir-Polder, dynamical Casimir,
  Unruh/Hawking), audited against a source document but not speculative.
- [`d067_art_v1/`](d067_art_v1/) — **D067-ART-v1**, an Adaptive Resonance
  Tracked phononic-piezoelectric light source. Documents a program that
  screened 100 phononic metacrystal families and closed on a reduced-order
  architecture (nested inertial resonator + PZT-5A transducer + adaptive
  resonance tracking) after rejecting a passive fixed-frequency design on
  manufacturing-robustness grounds. **Reduced-order architecture freeze —
  not experimentally validated.** The full monograph is in
  [`docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf`](docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf).

## Running the self-checks

Each package's `report.py` verifies its own transcribed/derived numbers
against the source document's worked values:

```
python3 -m chronometrics.report
python3 -m zero_point_energy.report
python3 -m d067_art_v1.report
```

## Citation

See [`CITATION.cff`](CITATION.cff) for how to cite the D067-ART-v1
monograph (James Lockwood, September 2026).
