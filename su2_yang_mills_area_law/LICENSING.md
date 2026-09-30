# Licensing scope

This repository mixes material under different terms. The MIT License in
[`LICENSE`](LICENSE) (Copyright (c) 2026 James M. Lockwood) covers **only**
the files listed under "MIT-licensed code". Everything else keeps its own
rights, as listed below. MIT licensing does not replace scholarly
attribution: if you use the methods or results, cite the manuscripts and the
works they cite (see "Citation" in [`README.md`](README.md) and
[`CITATIONS.md`](CITATIONS.md)).

## MIT-licensed code

| Path | Notes |
|---|---|
| `reproduction/SI_YangMills_reproduce_all.py` | **Release copy.** Identical to the imported original except that line 2 (a confidentiality notice) is removed. See `reproduction/patches/0001-release-copy-remove-confidentiality-notice.patch` and `provenance/FILES.md`. The author chose to license this copy under MIT. |
| `reproduction/run_reproduction.py` | Run wrapper written for this repository. |
| `tools/verify_repository.py` | Repository integrity checker. |
| `tests/test_repository.py` | Integrity and consistency tests. |
| `Makefile`, `pyproject.toml`, `requirements.txt`, `.gitattributes`, `.gitignore` | Build, environment and repository configuration. |
| `.github/workflows/*.yml` | CI configuration. |

## Not covered by the MIT License

| Path | Status |
|---|---|
| `reproduction/original/SI_YangMills_reproduce_all.py` | Byte-identical import of the author's original script. It carries the in-file notice "CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE" and is kept unchanged as a provenance record. The MIT grant does not extend to it. Use the release copy. |
| `reproduction/patches/*.patch` | Provenance record of the one-line difference between the original and the release copy. |
| `paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf` | Manuscript. Copyright James M. Lockwood, all rights reserved. It carries the notice "CONFIDENTIAL DRAFT — NOT FOR CIRCULATION". |
| `supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf` | Supplementary progress document. Copyright James M. Lockwood, all rights reserved. It carries the notice "CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE". |
| Documentation (`*.md`, `CITATION.cff`, `REFERENCES.bib`, `.github/ISSUE_TEMPLATE/*`, `.github/*.md`) | Copyright James M. Lockwood. Not licensed under MIT unless separately stated. |
| `results/` | Generated outputs of the scripts, provided so that runs can be compared. Not separately licensed. |
| `provenance/`, `MANIFEST.sha256` | Records of hashes and provenance. |

Figures: the manuscripts contain figures and typeset material. These remain
part of the manuscripts and are not covered by the MIT License. No
standalone figure files are included.

Third-party scholarly works cited in the manuscripts, in `CITATIONS.md` or in
`REFERENCES.bib` remain the property of their respective rights holders. Only
bibliographic metadata is reproduced here.

## Third-party software (not bundled)

No third-party source code is copied into this repository. The scripts
import the following packages, which are installed separately and remain
under their own licences:

| Package | Version tested | Licence (from installed package metadata) |
|---|---|---|
| numpy | 2.4.6 | `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` (License-Expression field) |
| scipy | 1.17.1 | BSD licence (classifier `License :: OSI Approved :: BSD License`; licence text begins "Copyright (c) 2001-2002 Enthought, Inc. 2003, SciPy Developers") |
| mpmath | 1.4.1 | `BSD-3-Clause` (License-Expression field) |

The CI workflows reference the GitHub Actions `actions/checkout`,
`actions/setup-python` and `actions/upload-artifact` by tag. They are not
bundled and remain under their own licences.

## Changes to licensing

Any change to these terms will be recorded in this file, in `LICENSE` where
applicable, and in `CHANGELOG.md`.
