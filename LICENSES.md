# Licensing architecture

This repository is licensed per content type, not under a single uniform
license. `CITATION.cff` lists both `MIT` and `CC-BY-4.0` because both
apply *somewhere* in the repository -- that list is not a choice between
two licenses for a given file ("MIT OR CC-BY-4.0"), it is a statement that
different parts of the repository carry different licenses. This file is
the authoritative scope statement.

## Scope

- **Software source code** in this repository is licensed under the
  **MIT License** ([`LICENSE`](LICENSE)) unless otherwise stated. This
  covers all executable files, including but not limited to every `*.py`
  file under `chronometrics/`, `zero_point_energy/`, `d067_art_v1/`,
  `experiments/`, `tests/`, and the repository-root `validation.py`.

- **Scientific prose, reports, original documentation, and original
  figures** in this repository are licensed under **CC BY 4.0**
  ([`LICENSE-CC-BY-4.0.md`](LICENSE-CC-BY-4.0.md)) unless otherwise
  stated. This covers every `README.md`, `SCIENTIFIC_VALIDATION.md`,
  `PARAMETER_PROVENANCE.md`, `ACKNOWLEDGMENTS.md`, this file, and the
  D067-ART-v1 monograph
  (`docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf`).

- **Third-party material** (e.g. any vendored code, data, or figures
  originating outside this project) retains its own original license,
  wherever such material exists and is marked as such. Nothing in this
  file relicenses third-party content, and no third-party license text in
  this repository has been modified.

## Why per-file, not per-repository

A reader reusing a `.py` module needs MIT's permissive terms without an
attribution-in-derivative-works obligation; a reader quoting or adapting
the write-up needs CC BY 4.0's attribution requirement. Applying a single
license repository-wide would either over-restrict the code or
under-attribute the prose. `CITATION.cff`'s `license` field is kept
consistent with this document -- it is not meant to be read as offering a
choice of license for any single file.
