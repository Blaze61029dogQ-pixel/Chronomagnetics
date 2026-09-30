# Changelog

## Unreleased

### 2026-09-30

Added:
- `supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf`: supplementary
  progress document (Google Drive), byte-identical.
- `reproduction/original/SI_YangMills_reproduce_all.py`: the author's
  reproduction script, byte-identical to the Google Docs text/plain export.
- `reproduction/SI_YangMills_reproduce_all.py`: release copy with the
  confidentiality line (line 2) removed, at the author's direction. Documented
  in `reproduction/patches/0001-release-copy-remove-confidentiality-notice.patch`.
- `reproduction/run_reproduction.py`: run wrapper recording command,
  environment, timing, exit status and output.
- `results/`: quick and full runs of the release copy and of the original.
  Every run gives one FAIL, S1/1.25, because `levin_N3_certificate.py` is
  missing.
- `CITATIONS.md` and `REFERENCES.bib`: Paper 1 bibliography with
  verification status (search-corroborated only), attribution notes, and
  BibTeX for Paper 1, Paper 2 and the repository.
- `provenance/release_hashes.sha256`, and per-directory READMEs.
- Tests for the historical hashes, the release-copy derivation, the
  consistency of the recorded runs, licence metadata, and the script's CLI.

Changed:
- Licensing: code is MIT-licensed (`LICENSE`, Copyright (c) 2026 James M.
  Lockwood). The scope is in `LICENSING.md` (renamed from `RIGHTS.md`).
  Manuscripts, the SI document, the original script and the documentation
  are not MIT-licensed. This replaces the earlier all-rights-reserved notice.
- `paper/Paper1_AreaLaw_SU2_2026-09-28.pdf` moved to `paper/original/`, bytes
  unchanged, to keep originals separate from future release copies.
- `CITATION.cff`: repository title, version label `draft-2026-09-28`,
  repository URL, MIT, preferred citation of Paper 1, references to Paper 2
  and the SI document. The earlier `date-released` was removed because no
  release has been made.
- `requirements.txt` and `pyproject.toml`: numpy 2.4.6, scipy 1.17.1,
  mpmath 1.4.1.
- `Makefile`: `reproduce` and `full` now run the script.
- `tools/verify_repository.py`: checks every original and release hash;
  scans JSON, log, patch and BibTeX files for hygiene.
- `README.md`, `CLAIMS.md`, `REPRODUCIBILITY.md`,
  `.github/RELEASE_CHECKLIST.md`: updated to the recorded state (bibliography search-corroborated only;
  Theorem 3.9 certificate missing; no release).

Not done (inputs missing):
- Release PDFs without confidentiality notices (no manuscript sources).
- Theorem 3.9 certificate (`levin_N3_certificate.py`).
- Paper 2.
- Bibliographic verification against primary records (network access to
  Crossref, doi.org and arXiv refused).

### 2026-09-29

- Initial repository import: Paper 1 PDF (byte-identical), documentation,
  provenance records, SHA-256 manifest, integrity checker and tests, CI
  configuration, issue and PR templates, release checklist.
