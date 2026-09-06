# Chronomagnetics

Author: James Lockwood

Two independent research constructions, each transcribed into a runnable,
self-checking Python package:

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
  Observables"* (Lockwood, Cyrek, Burkeen & Hansley).

Each package's `report.py` prints a full accounting and hard-checks its
computed values against the source documents' own worked numbers:

```
python3 -m chronometrics.report
python3 -m zero_point_energy.report
```

## License

Source code (all `*.py` files) is licensed under [MIT](LICENSE).
Research/documentation content (README.md files and the mathematical
framework and derivations they describe) is licensed under
[CC BY 4.0](LICENSE-CC-BY-4.0.md).

See [`CITATION.cff`](CITATION.cff) for citation metadata.
