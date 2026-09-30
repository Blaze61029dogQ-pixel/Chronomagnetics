# Release checklist

State as of 2026-09-30. An item is ticked only if it was done and verified.
Do not create a release, or describe the materials as release-ready, while
any unticked item remains.

- [ ] Confidentiality notices intentionally removed or replaced **by
      rebuilding the PDFs from their sources**. Not done: no LaTeX sources
      for Paper 1 or the SI document were available. The originals keep
      their notices.
- [x] Confidentiality line removed from the **script** release copy only, at
      the author's direction, as a documented one-line patch
      (`reproduction/patches/`). The original is kept byte-identical.
- [ ] Final release PDF hashes recorded in `provenance/release_hashes.sha256`.
      No release PDFs exist yet.
- [x] Original artifact hashes recorded (`provenance/source_hashes.sha256`)
      and pinned in `tests/test_repository.py`.
- [ ] Quick reproduction passes. It runs, but **exits 1**: 112 PASS, 1 FAIL
      (S1/1.25, `levin_N3_certificate.py` missing), 2 INFO.
- [x] Full reproduction status recorded (`results/full/`, `REPRODUCIBILITY.md`):
      121 PASS, 1 FAIL (S1/1.25), 2 INFO, exit 1, 105.8 s.
- [ ] Theorem 3.9 certificate (`levin_N3_certificate.py`) added unchanged and
      passing.
- [ ] Paper 2 (companion manuscript) added, or its absence accepted for the
      release.
- [x] `CLAIMS.md` synchronised with the current Paper 1 draft and the
      script's check IDs.
- [x] `README.md` synchronised with the recorded results.
- [ ] Citations checked against primary records (Crossref, publisher,
      arXiv). Only search-corroborated so far; direct access was refused by
      the network policy. See `CITATIONS.md` for the known discrepancies
      (Dorlas–Savoie journal version; Kanaya–Kaya title hyphen; Remark 1.1
      "≈ 0.37507" versus the computed 0.3750606…).
- [x] Licence decision recorded: MIT for code (`LICENSE`), scope in
      `LICENSING.md`.
- [ ] Repository visibility explicitly chosen by the author for the final
      release. The hosting repository `Chronomagnetics` is currently
      **public**, and the originals were uploaded there at the author's
      direction.
- [ ] Release tag checked: the name matches the document's own version or
      date, and the tag is annotated.
