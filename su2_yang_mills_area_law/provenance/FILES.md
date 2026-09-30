# Provenance of imported and derived files

Hash records:

- `provenance/source_hashes.sha256`: **originals** exactly as imported. This is
  a historical record and is never rewritten when release copies change.
- `provenance/release_hashes.sha256`: **release artifacts** derived from the
  originals.

## Originals

| Original (as supplied) | Repository path | Bytes | SHA-256 | Role | Imported | Unchanged |
|---|---|---|---|---|---|---|
| `a8969626-Paper1_AreaLaw_SU2_draft.pdf` (supplied file upload) | `paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf` | 418772 | `8c4b17317495ff791c3c8af2d0e5ad131e9115cf0c18ca332d1145dc853af256` | Paper 1 manuscript: "Draft, 28 September 2026"; 15 pages; pdfTeX-1.40.25; PDF CreationDate 2026-09-29T03:00:40Z | 2026-09-29 | Yes. `cmp` against the upload found no difference. Moved from `paper/` to `paper/original/` on 2026-09-30; bytes unchanged |
| Google Drive PDF `SI_YangMills_Tracks1-2_v0.1.pdf` (Drive created 2026-09-28T02:18:58Z; Drive-reported size 397297) | `supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf` | 397297 | `fab5b718e5ff02728e0e8588525e3ca8fefd445fb1ffa82103e4fe05b85f0496` | Supplementary progress document: "SI Yang–Mills Tracks 1–2, draft v0.1, 28 Sept. 2026"; 7 pages; pdfTeX-1.40.25; PDF CreationDate 2026-09-28T02:16:18Z | 2026-09-30 | Yes. Downloaded through the Google Drive API; the byte count equals the Drive-reported size |
| Google Docs document titled "Jupyter" (Drive created 2026-09-28T23:43:33Z, modified 2026-09-28T23:43:40Z), whose text is the script `SI_YangMills_reproduce_all.py` | `reproduction/original/SI_YangMills_reproduce_all.py` | 63509 | `c682c895d51ce0acc09f260d4eede38e98be765c18268d1378e53d4be40dcb88` | Reproduction script covering Paper 1, Paper 2 and further "tracks" (sections S1–S10) | 2026-09-30 | Yes, relative to the export (see note) |

**Note on the script's provenance.** The author's on-disk `.py` file was not
available. What was imported is the Google Drive API `text/plain` export of the
Google Docs document that contains the script's text. The bytes are stored
exactly as exported, including a UTF-8 byte-order mark and CRLF line endings.
`.gitattributes` marks the file `-text` so that git does not normalise it.
Whether this export is byte-identical to the author's original `.py` file is
**UNKNOWN**; its hash could not be compared. Checks on the export:

- it byte-compiles with CPython 3.11.15;
- it contains no typographic quotes, non-breaking spaces or zero-width spaces;
- it runs to completion in both quick and full modes (see `results/`).

## Release artifacts

| Repository path | Derived from | Derivation | Bytes | SHA-256 |
|---|---|---|---|---|
| `reproduction/SI_YangMills_reproduce_all.py` | `reproduction/original/SI_YangMills_reproduce_all.py` | Line 2, `# CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE` plus its CRLF (68 bytes), removed at the author's direction (2026-09-30). No other byte changed: the BOM, CRLF endings and all code are identical. `tests/test_repository.py` checks this byte for byte. | 63441 | `3b98fd4af076287f223ae1b04c434c1224d9135150739e2c1b0078259300d09e` |
| `reproduction/patches/0001-release-copy-remove-confidentiality-notice.patch` | — | Unified diff (`diff -u`) from the original to the release copy. `patch --binary -s -o - reproduction/original/SI_YangMills_reproduce_all.py reproduction/patches/0001-release-copy-remove-confidentiality-notice.patch | sha256sum` (GNU patch 2.7.6) reproduces the release copy's SHA-256 (checked 2026-09-30) | 290 | `33ead725ebb29b24774e25e909e4f44ba799260bcbb2d3b6cdf7c512abb04637` |

**No release PDFs exist.** The instructions were to rebuild notice-free
release PDFs from the manuscript sources. No LaTeX or other source for Paper 1
or the SI document was found (see below), so none was built. The notices were
not removed or covered in any PDF. The original PDFs remain the only PDFs.

## Searched for but not found (as of 2026-09-30)

Searched: this container's filesystem; every branch of
`Blaze61029dogQ-pixel/Chronomagnetics`; the private repository
`Blaze61029dogQ-pixel/None` (contains only a README); the connected Google
Drive (full-text and title searches). Not found:

- LaTeX (or any other) sources for Paper 1 and for the SI document (`.tex`,
  `.bib`, `.bbl`, figures);
- Paper 2 (the companion manuscript cited as [13] in Paper 1), in any format;
- `levin_N3_certificate.py`, which the SI script runs for check S1/1.25
  (Theorem 3.9, N = 3). Its absence makes that check FAIL;
- `cert_series.py`, `cert_tails.py`, `track1_closedforms.py`,
  `thmC_BE_check.py`, `thmCD_checks.py`, `df80_check.py` (named in Paper 1,
  Appendix A). Their computations appear to be covered by sections S1–S4 of
  the SI script. This is an inference from the script's check descriptions,
  not a comparison with those files;
- `verify_track2.py` (named in the SI document). A listing appears in the SI
  PDF's appendix, but that listing was not extracted into a separate file;
- the "Record v1.4", "addendum v1.5" and "Track 5 spec v0.1" documents named in
  the SI script's docstring, and `check123.py` (named in check S5/5.11b).

Nothing was reconstructed from memory or from PDFs.
