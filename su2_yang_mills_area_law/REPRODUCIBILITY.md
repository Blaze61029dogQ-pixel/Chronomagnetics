# Reproducibility

This file gives the exact commands, environment and recorded outcomes. A
command that ran is not the same as a scientific claim being established.
See `CLAIMS.md` for what each check does and does not support.

## Supported environment

- CPython **3.11** or later. Recorded runs used CPython 3.11.15 on Linux
  x86_64 (glibc 2.39, 4 vCPU).
- numpy 2.4.6, scipy 1.17.1 and mpmath 1.4.1, pinned in `requirements.txt`.
  These come from the imports of `reproduction/SI_YangMills_reproduce_all.py`
  (`numpy`, `scipy.linalg.expm`, `mpmath`). The script's docstring says
  "Python 3.9+, numpy, scipy, mpmath". Only the versions above were tested.
- GNU coreutils `sha256sum` (9.4 tested); on macOS use `shasum -a 256 -c`.
- GNU `patch` (2.7.6 tested) only to re-derive the release copy.

Full record: `provenance/environment.txt`.

## Clean-machine set-up

```sh
git clone <repository URL>
cd <repository>/su2_yang_mills_area_law     # or the repository root, if standalone
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

`make setup` does the same. The `Makefile` uses `.venv/bin/python` when it
exists, and otherwise `python3`.

## 1. Integrity checks and tests (`make check`)

| Step | Command | Pass condition |
|---|---|---|
| Byte-compile | `python3 -m compileall -q tools tests reproduction` | exit 0 |
| Integrity checker | `python3 tools/verify_repository.py` | `PASS: <n> manifest entries, 0 problem(s)`, exit 0 |
| Tests | `python3 -m unittest discover -s tests -v` | `OK`, exit 0 |
| Manifest | `sha256sum -c --quiet MANIFEST.sha256` | no output, exit 0 |

The checker and tests verify that:

- the manifest matches every file;
- the three originals match their historical SHA-256 values;
- the release script equals the original minus line 2, byte for byte;
- the recorded runs are consistent and correspond to the committed scripts;
- the release copy's check records equal the original's;
- the documentation links resolve;
- no absolute local paths or credential-like strings occur;
- `LICENSE`, `CITATION.cff` and `pyproject.toml` agree on MIT;
- the script's CLI and JSON report work (sections S4, S10).

## 2. Quick reproduction (`make reproduce`)

```sh
python3 reproduction/run_reproduction.py
```

This runs `python3 reproduction/SI_YangMills_reproduce_all.py --json results/quick/report.json`
and writes `results/quick/{stdout.log,report.json,run_meta.json}`.

**Recorded (2026-09-30):** 115 checks: 112 PASS, 1 FAIL, 2 INFO. Exit
status 1. Wall time 38.7 s. The FAIL is S1/1.25 ("Thm 3.9 certificate file
present next to this script", value "levin_N3_certificate.py missing").

`make reproduce` itself was also run, in a scratch copy of the repository so
that the recorded files were not overwritten. The wrapper exited 1 after
32.3 s, `make` exited 2, and the check records were identical to
`results/quick/report.json`.

## 3. Full reproduction (`make full`)

```sh
python3 reproduction/run_reproduction.py --full
```

This runs the script with `--full`, which uses the grids and sizes of the
papers, and writes `results/full/`.

**Recorded (2026-09-30):** 124 checks: 121 PASS, 1 FAIL, 2 INFO. Exit
status 1. Wall time 105.8 s. The only FAIL is S1/1.25, as above. Per-section
times from the log: S1 7.0 s, S2 0.4 s, S3 34.8 s, S4 0.0 s, S5 21.8 s, S6
10.0 s, S7 0.2 s, S8 6.7 s, S9 24.7 s, S10 0.0 s.

`make full` in the scratch copy: the wrapper exited 1 after 103.7 s, `make`
exited 2, and the check records were identical to `results/full/report.json`.

## 4. Original script (provenance comparison)

```sh
python3 reproduction/run_reproduction.py --script reproduction/original/SI_YangMills_reproduce_all.py --outdir results/original-export/quick
python3 reproduction/run_reproduction.py --script reproduction/original/SI_YangMills_reproduce_all.py --full --outdir results/original-export/full
```

**Recorded (2026-09-30):** the same counts and exit status as the release
copy (quick 33.6 s, full 103.6 s). The check records (status, value,
expected) are identical to the release copy's in both modes. The logs differ
only in timing lines.

## 5. Individual sections

```sh
python3 reproduction/SI_YangMills_reproduce_all.py --sections S1 --full --json s1.json   # Lemma 3.4, Thm 3.8 certificates
python3 reproduction/SI_YangMills_reproduce_all.py --sections S2,S3,S4                  # Theorem C, Prop. 6.1 / Conj. 6.2, Remark 7.1
```

Sections S5–S10 cover Paper 2 and further tracks whose documents are not in
this repository (see `CLAIMS.md`).

## Return codes and interpretation

- **0**: every check PASSed (INFO lines are informational).
- **1**: at least one check FAILed. The `SUMMARY` line and the list of FAIL
  lines follow in the output.
- **124** (wrapper only): `--timeout` expired.
- `make reproduce` and `make full` pass the wrapper's status through. On a
  non-zero status `make` prints "Error 1" and exits with status 2.

A PASS means the computation reproduced its target within the tolerance the
script sets. For tier `CERT` checks, the arithmetic is exact rational or
outward-rounded interval arithmetic, and the check is a component of a
computer-assisted proof. For `EXACT`, `NUM`, `MC` and `REG` checks, a PASS is
a consistency check or a regression only.

## Precision and determinism

- Exact rational arithmetic (`fractions.Fraction`) for the series
  certificates (S1/1.7–1.16).
- `mpmath` at 20–60 decimal digits, set per section (`mp.dps`), and
  `mpmath.iv` interval arithmetic at 40 digits for S1/1.22.
- IEEE-754 double precision (numpy) for lattice and Monte Carlo checks. Some
  Gram matrices in check 7.10 are formed in float32.
- Fixed seeds: `np.random.default_rng` with seeds 6, 7, 11, 29 and 80, per
  section.
- Determinism: on this machine, two independent runs (release copy and
  original) gave identical check records in both modes. Bit-for-bit
  equality of outputs on other platforms or library versions has **not**
  been tested. The Monte Carlo and double-precision checks may differ in
  the last digits.

## Outputs

`results/<run>/stdout.log` is the combined stdout and stderr, verbatim.
Machine-specific absolute paths would be replaced by `<REPO>`,
`<PYTHON_PREFIX>` or `<PYTHON_BASE_PREFIX>`, and each replacement recorded in
`run_meta.json`. None occurred in the recorded runs.
`results/<run>/report.json` is the script's own JSON report.
`results/<run>/run_meta.json` records the command, interpreter, UTC
start/end, wall time, exit status, script SHA-256, platform and package
versions.

## SHA-256 verification

```sh
sha256sum -c MANIFEST.sha256
grep -v '^#' provenance/source_hashes.sha256  | sha256sum -c   # originals
grep -v '^#' provenance/release_hashes.sha256 | sha256sum -c   # release artifacts
```

## Not executed / not available

- `levin_N3_certificate.py` (Theorem 3.9): missing, so check S1/1.25 FAILs.
- Paper 1 Appendix A scripts `cert_series.py`, `cert_tails.py`,
  `track1_closedforms.py`, `thmC_BE_check.py`, `thmCD_checks.py`,
  `df80_check.py`: not present, so they were not run separately.
- Rebuilding notice-free PDFs: no manuscript sources are available.

## Platform caveats

`.gitattributes` normalises text files to LF, **except** the two copies of
the SI script. They are marked `-text` to keep their BOM and CRLF bytes, and
hence their recorded hashes. PDFs are binary.
