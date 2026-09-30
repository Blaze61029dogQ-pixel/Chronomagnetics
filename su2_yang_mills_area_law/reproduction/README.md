# Reproduction

| File | What it is | Licence |
|---|---|---|
| `SI_YangMills_reproduce_all.py` | **Release copy** of the author's reproduction script. Identical to `original/SI_YangMills_reproduce_all.py` except that line 2 (`# CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT REPRODUCE`) is removed. | MIT |
| `original/SI_YangMills_reproduce_all.py` | The original script, byte-identical to the Google Drive `text/plain` export of the Google Docs document that contains it (UTF-8 BOM, CRLF). Provenance record only. | not MIT (in-file notice) |
| `patches/0001-release-copy-remove-confidentiality-notice.patch` | Unified diff from the original to the release copy. | provenance record |
| `run_reproduction.py` | Wrapper that runs a script unchanged and records command, interpreter, UTC times, wall time, exit status, script SHA-256, package versions, log and JSON report. | MIT |

Re-derive the release copy from the original:

```sh
cd reproduction
patch --binary -s -o - original/SI_YangMills_reproduce_all.py \
      patches/0001-release-copy-remove-confidentiality-notice.patch | sha256sum
# expected: 3b98fd4af076287f223ae1b04c434c1224d9135150739e2c1b0078259300d09e
```

## The script

`SI_YangMills_reproduce_all.py` (1005 lines in the original) runs checks in
ten sections. Its options are `--full` (the papers' grids), `--sections`
(e.g. `S1,S5`) and `--json PATH`. It exits with status 1 if any check FAILs.

| Section | Script's description | Relates to |
|---|---|---|
| S1 | Track 1 / Paper 1 §3: Neumann-flow constant, moments, closed forms, series certificates, tails, grid minima, Theorem 3.8 interval certificate, Theorem 3.9 (runs `levin_N3_certificate.py`) | Paper 1 §3 |
| S2 | Theorem C (Paper 1 §5) | Paper 1 §5, Remark 1.1 |
| S3 | Proposition/Conjecture D (Paper 1 §6) | Paper 1 Prop. 6.1, Conj. 6.2 |
| S4 | DF80 normalisation (Paper 1 Remark 7.1) | Paper 1 Remark 7.1 |
| S5 | Track 2 (Paper 2 §§2–3); includes Paper 1 Remark 2.6's "Section S5" consistency tests | Paper 1 Remark 2.6; Paper 2 (not included) |
| S6–S10 | Paper 2 §§4–5, Tracks 3–5, asymptotic-scaling constants | documents not included |

The mapping of check IDs to manuscript statements is in `../CLAIMS.md`.

## Dependencies

numpy, scipy (`scipy.linalg.expm` in S5) and mpmath, pinned in
`../requirements.txt`. S1 check 1.25 runs `levin_N3_certificate.py` from the
**same directory as the script**, via `subprocess` with a 250 s timeout.

## Missing inputs

| Needed | Why | Effect |
|---|---|---|
| `levin_N3_certificate.py` | Theorem 3.9 (Levin's conjecture, N = 3) certificate; the manuscript describes exact series through order 120 and interval arithmetic on 38 cells of [3.3, 103.53] | check S1/1.25 FAILs, so the run exits 1. Place the original file, unchanged, next to the release script (and next to `original/…` to test the original), record its hash in `../provenance/`, and re-run |
| `cert_series.py`, `cert_tails.py`, `track1_closedforms.py`, `thmC_BE_check.py`, `thmCD_checks.py`, `df80_check.py` | named in Paper 1 Appendix A | not run separately. Sections S1–S4 appear to cover the same computations (an inference from the check descriptions) |
| `verify_track2.py`, `check123.py` | named in the SI PDF and in check 5.11b | not run |

No missing script has been reconstructed or substituted.

## Adding a missing script

1. Copy the original file here **unchanged**.
2. Add its SHA-256 to `../provenance/source_hashes.sha256` and its details
   to `../provenance/FILES.md`.
3. Run `make reproduce` and `make full` from the repository root.
4. Update `../CLAIMS.md`, `../README.md` and `../REPRODUCIBILITY.md` with the
   recorded results.
5. Run `make hashes` and `make check`.
