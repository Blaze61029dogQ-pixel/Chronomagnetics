# Recorded runs

Each directory holds one run of the reproduction script made with
`reproduction/run_reproduction.py` on 2026-09-30 (CPython 3.11.15, numpy
2.4.6, scipy 1.17.1, mpmath 1.4.1, Linux x86_64, 4 vCPU):

| Directory | Script | Mode | Checks | PASS | FAIL | INFO | Exit | Wall time |
|---|---|---|---|---|---|---|---|---|
| `quick/` | release copy | quick | 115 | 112 | 1 | 2 | 1 | 38.7 s |
| `full/` | release copy | full | 124 | 121 | 1 | 2 | 1 | 105.8 s |
| `original-export/quick/` | original | quick | 115 | 112 | 1 | 2 | 1 | 33.6 s |
| `original-export/full/` | original | full | 124 | 121 | 1 | 2 | 1 | 103.6 s |

Files in each directory:

- `stdout.log`: verbatim console output.
- `report.json`: the script's JSON report.
- `run_meta.json`: command, interpreter, UTC times, wall time, exit status,
  script SHA-256, package versions.

The single FAIL in every run is check S1/1.25: `levin_N3_certificate.py` is
missing. These are reference outputs. They show what the script printed on
this machine. They are not proofs, and a PASS means only what `CLAIMS.md`
says it means.

Regenerate with `make reproduce` and `make full`. The runs of the original
script use the `--script` option; see `REPRODUCIBILITY.md`.
