# Area Law for 4D SU(2) Lattice Yang–Mills at β_W < 2/3

**James M. Lockwood**, Spectrality Institute

This repository holds the manuscript *Area law for four-dimensional SU(2)
lattice Yang–Mills theory at β_W < 2/3, and the limits of single-site mixing
criteria* (draft of 28 September 2026, "Paper 1"), a supplementary progress
document, and the author's reproduction script. It also records the runs of
that script, the provenance of every file, and citation metadata.

> **Status (2026-09-30): not release-ready.**
>
> - **Confidentiality notices are still in the originals.** The Paper 1 PDF
>   carries "CONFIDENTIAL DRAFT — NOT FOR CIRCULATION". The SI PDF and the
>   original script carry "CONFIDENTIAL — DO NOT SHARE · DO NOT COPY · DO NOT
>   REPRODUCE". They are included byte-identical at the author's direction.
>   No manuscript sources were available, so notice-free release PDFs could
>   not be rebuilt. The notices were not removed or covered.
> - **One certificate is missing.** `levin_N3_certificate.py` (Theorem 3.9,
>   N = 3) was not available. The reproduction script reports check S1/1.25
>   as FAIL and exits with status 1 in both quick and full modes.
> - **Paper 2** (the companion manuscript) is not in this repository.
>
> See [`.github/RELEASE_CHECKLIST.md`](.github/RELEASE_CHECKLIST.md).

## Overview

Paper 1 studies four-dimensional SU(2) lattice Yang–Mills theory with Wilson
action exp((β_W/2) Σ_p Re Tr U_p) at **fixed lattice spacing**. Its main
result is Wilson's area law for all β_W < 2/3. The proof has three
ingredients:

1. the **Durhuus–Fröhlich slab reduction** to three-dimensional O(4)
   σ-models in arbitrary SO(4) environments;
2. a **Wasserstein form of Dobrushin's uniqueness condition** (Section 2.2,
   Proposition 2.5), proved in a self-contained way;
3. a bound on the **Wasserstein Lipschitz constant of the von Mises–Fisher
   (vMF) family on S³**, which takes the optimal value 1/4 for fields of norm
   at most 4 (Theorem B). It is proved with a harmonic Neumann flow and
   reduced to two Bessel-function inequalities (Lemma 3.4), which are
   certified in exact rational arithmetic.

In the slab O(4) system the fields have norm at most 6K < 4, so the Dobrushin
row sum is at most 6K/4 < 1 for K = β_W < 2/3 (Section 4). The manuscript
also shows that 2/3, the O(4) mean-field point, is the exact limit of
single-site chordal-Wasserstein criteria for these models (Theorem C).

## Main results

The statements below paraphrase the manuscript. The PDF is authoritative.
Labels follow the manuscript.

**Theorem A (area law).** Let Λ be a periodic box in ℤ⁴ of side L and let
β_W < 2/3. There are C₁, C₂ > 0, depending only on β_W, such that
|⟨½ Tr U_ℓ⟩| ≤ C₁ e^{−C₂ area(ℓ)} for every rectangular loop ℓ with sides at
most L/2, uniformly in L.

**Theorem B (Wasserstein Lipschitz constant of vMF laws).** Let
μ_η ∝ e^{η·n} dσ(n) on S³, with the chordal metric. For |η₀|, |η₁| ≤ 4,
W₁(μ_{η₀}, μ_{η₁}) ≤ ¼ |η₀ − η₁|. The constant ¼ is attained as η₀, η₁ → 0.

**Theorem C (limits of single-site criteria).** Consider the slab O(4)
models with coupling K = β_W and arbitrary SO(4) environments:

- (i) Bakry–Émery holds uniformly iff K < 1/6;
- (ii) every single-site total-variation Dobrushin criterion fails for
  K ≥ K_TV = 0.39629095688…, the root of 6 L₁(K) = I₁(K);
- (iii) single-site chordal-W₁ criteria hold for K < 2/3 and fail for
  K ≥ 2/3;
- (iv) the slab-criterion hypothesis fails for K > 4 G_{ℤ³}(0) = 1.0109….
  Numerically it fails already for K > K_c = 0.9360(1) (ref. [11]).

**Levin's conjecture.** Theorem 3.8 proves it for N = 4 at all fields, using
Corollary 3.6 for |g| ≤ 4 and an interval-arithmetic certificate on
[4, 262.45]. The manuscript states that Theorem 3.9 proves it for N = 3, using exact series for
r ≤ 7/2 and an interval certificate on [3.3, 103.53]. That certificate is not in this repository and was not
reproduced (check S1/1.25). Corollary 3.7 gives
uniqueness for sup_a Σ_b ‖J_ab‖_op < 4. Remark 3.10 notes that the method as
it stands cannot settle N ≥ 5.

**Further statements.** Proposition 6.1 gives mean-absolute-deviation bounds
and the unconditional TV range β_W < 1/3. Conjecture 6.2 (unproved) would
extend that range to β_W < π/8. Remark 7.1 concerns a normalisation in
Durhuus–Fröhlich (1980).

**Relation to earlier work, in the manuscript's words.** β_W < 2/3 is "the
full range asserted without proof by Durhuus and Fröhlich in 1980". The
largest range previously established with a complete argument is
β_W < 1/6 (Cao–Nissim–Sheffield 2025). The ranges derivable from Levin's and
Royer's constants (≈ 0.298 and ≈ 0.375) are described as "not found
recorded" ("We have not found either combination recorded"). That is a
literature-search statement, which this repository has not independently
verified. The repository makes no stronger priority claim, and a
passing numerical check is not evidence of novelty.

## Scope: lattice results versus the continuum problem

**What the manuscripts address:** fixed lattice spacing; strong coupling
(β_W < 2/3 for the area law, while the manuscript notes that the SU(2)
crossover is near β_W ≈ 2.2); Wilson's area law for rectangular loops;
single-site uniqueness and mixing criteria for O(N) models with N = 3, 4.

**What they do not address, and this repository does not claim:**
construction of a continuum four-dimensional Yang–Mills theory; the
continuum limit or any bound uniform in the lattice spacing; a continuum
mass gap; the Clay Millennium Prize problem "Yang–Mills existence and mass
gap", which remains unresolved. Paper 1 states: "All results are at fixed
lattice spacing and strong coupling; nothing here concerns the continuum
limit." Paper 2's title and the SI document mention a "transfer-matrix gap"
or "mass gap" for β_W < 2/9. That is a fixed-lattice-spacing statement,
which the SI document labels "(Open)", and it says: "Nothing here bears on
the Clay statement."

The computations support only the statements to which the manuscript assigns
them. Only the exact and interval certificates named in the manuscript are
parts of proofs. All other checks are consistency checks or evidence. See
[`CLAIMS.md`](CLAIMS.md).

## Repository contents

| Path | Contents |
|---|---|
| `paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf` | Paper 1, byte-identical to the supplied file (contains the confidentiality notice). See [`paper/README.md`](paper/README.md). |
| `supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf` | Supplementary progress document v0.1 (28 September 2026), byte-identical to the Drive file (contains the confidentiality notice). See [`supplementary/README.md`](supplementary/README.md). |
| `reproduction/SI_YangMills_reproduce_all.py` | **Release copy** of the reproduction script (MIT). Identical to the original except that the notice on line 2 is removed. |
| `reproduction/original/SI_YangMills_reproduce_all.py` | The original script, byte-identical to the imported Google Docs export. Not MIT. |
| `reproduction/patches/` | The one-line patch from original to release copy. |
| `reproduction/run_reproduction.py` | Wrapper that runs the script unchanged and records command, environment, timing, exit status and output. |
| `results/` | Recorded runs (quick and full, for the release copy and the original). See [`results/README.md`](results/README.md). |
| `CLAIMS.md` | Map from statements to evidence and script check IDs. |
| `CITATIONS.md`, `REFERENCES.bib`, `CITATION.cff` | Citation metadata, verification status, attribution. |
| `REPRODUCIBILITY.md` | Step-by-step reproduction instructions and recorded results. |
| `LICENSE`, `LICENSING.md` | MIT License text and its scope. |
| `provenance/` | File provenance, original and release hashes, environment. |
| `tools/verify_repository.py`, `tests/` | Integrity checker and tests. |
| `MANIFEST.sha256` | SHA-256 of every file (except the manifest). |

## Reproduction

Requirements: CPython ≥ 3.11 and the pinned packages in `requirements.txt`
(numpy 2.4.6, scipy 1.17.1, mpmath 1.4.1).

```sh
make setup          # python3 -m venv .venv && pip install -r requirements.txt
make check          # integrity checks + tests (exit 0 expected)
make reproduce      # quick run -> ci-output/quick/  (currently fails: S1/1.25)
make full           # full run  -> ci-output/full/   (currently fails: S1/1.25)
```

Equivalent direct commands, from the repository root:

```sh
python3 reproduction/run_reproduction.py --outdir ci-output/quick          # quick
python3 reproduction/run_reproduction.py --full --outdir ci-output/full    # the papers' grids
python3 reproduction/SI_YangMills_reproduce_all.py --sections S1,S4 --full
```

`make reproduce`, `make full` and the commands above write only to the
ignored `ci-output/` directory. Running the wrapper **without** `--outdir`
overwrites the committed reference records in `results/`. Their timings then
change, so run `make hashes` before `make check` if you intend to replace
the records. Any other new file in the repository (for example a `--json`
output) also makes the manifest check fail until it is removed or `make
hashes` is run.

The script's options are `--full`, `--sections S1,…,S10` and `--json PATH`.
It exits with status 1 if any check FAILs. The wrapper passes that status
through, and `make` then stops with "Error 1" and exits with status 2.

### Recorded results (2026-09-30, CPython 3.11.15, Linux x86_64, 4 vCPU)

| Run | Checks | PASS | FAIL | INFO | Exit | Wall time |
|---|---|---|---|---|---|---|
| quick, release copy | 115 | 112 | 1 | 2 | 1 | 38.7 s |
| full, release copy | 124 | 121 | 1 | 2 | 1 | 105.8 s |
| quick, original | 115 | 112 | 1 | 2 | 1 | 33.6 s |
| full, original | 124 | 121 | 1 | 2 | 1 | 103.6 s |

The only FAIL is S1/1.25, "levin_N3_certificate.py missing". The release
copy and the original produce identical check records (status, value,
expected) in both modes.

## Certificate computations

| Manuscript statement | Checks | Arithmetic | Recorded status |
|---|---|---|---|
| Lemma 3.4 (Bessel inequalities for r ≤ 4) | S1/1.7–1.13, 1.15, 1.16 | exact rationals (`fractions.Fraction`) with rational majorant tails | PASS (full mode: coefficients to k = 189, tail ≤ 9.111e-99) |
| Theorem 3.8, N = 4, r ∈ [4, 262.45] | S1/1.22 | outward-rounded interval arithmetic (`mpmath.iv`) | PASS: 58 cells, max cell ≤ 0.062363, tail ≤ 0.045694, below 1/16 = 0.0625 |
| Theorem 3.9, N = 3 | S1/1.25 | exact series and interval arithmetic, per the manuscript | **FAIL: certificate file missing; not reproduced** |

All other checks, including the grid minima of Remark 3.5, Theorem C and the
Section 2 consistency tests, are numerical cross-checks or regressions. See
`CLAIMS.md`.

## Reproducibility status

| Component | Method | Status |
|---|---|---|
| Original artifacts (2 PDFs, 1 script) | SHA-256 against the historical record | PASS |
| Release copy of the script | byte comparison with the original minus line 2; the patch reproduces it | PASS |
| `MANIFEST.sha256` | `sha256sum -c` | PASS at commit time |
| Integrity checker and tests | `make check` | PASS at commit time (see `REPRODUCIBILITY.md`) |
| Quick reproduction | `make reproduce` | 112 PASS / 1 FAIL / 2 INFO; script exit 1 (`make` exit 2) |
| Full reproduction | `make full` | 121 PASS / 1 FAIL / 2 INFO; script exit 1 (`make` exit 2) |
| Theorem 3.9 certificate | `levin_N3_certificate.py` | NOT RUN: file missing |
| Paper 1 Appendix A scripts (`cert_series.py`, …) | — | Not present. Their computations appear to be covered by S1–S4 (inferred from the check descriptions) |
| Release PDFs without notices | rebuild from sources | NOT DONE: sources missing |
| Bibliographic verification | primary records (Crossref, arXiv) | NOT DONE: network access refused; search-corroborated only |

## Citation

Please cite Paper 1, and the repository with the commit you used. BibTeX for
all works, including the manuscript's bibliography with verification status,
is in [`REFERENCES.bib`](REFERENCES.bib). [`CITATIONS.md`](CITATIONS.md)
separates the established results the manuscripts cite from the claims that
originate in the manuscripts.

```bibtex
@unpublished{lockwood2026arealaw,
  author = {Lockwood, James M.},
  title  = {Area law for four-dimensional {SU(2)} lattice {Yang--Mills} theory at $\beta_W < 2/3$, and the limits of single-site mixing criteria},
  note   = {Draft, 28 September 2026, Spectrality Institute. Unpublished manuscript. PDF: https://github.com/Blaze61029dogQ-pixel/Chronomagnetics/blob/claude/su2-yang-mills-repo-1tb9ll/su2_yang_mills_area_law/paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf},
  year   = {2026},
  month  = sep
}

@unpublished{lockwood_companion_dobrushin,
  author = {Lockwood, James M.},
  title  = {A direct {Wasserstein--Dobrushin} approach to four-dimensional {SU(2)} lattice {Yang--Mills} theory: uniqueness, explicit clustering and a transfer-matrix gap for $\beta_W < 2/9$},
  note   = {Companion paper (draft), cited as reference [13] in Paper 1. Not included in this repository}
}

@software{lockwood2026su2repo,
  author  = {Lockwood, James M.},
  title   = {su2-yang-mills-area-law: manuscript and reproducibility materials for strong-coupling area-law and mixing results in four-dimensional {SU(2)} lattice {Yang--Mills} theory},
  year    = {2026},
  version = {draft-2026-09-28},
  url     = {https://github.com/Blaze61029dogQ-pixel/Chronomagnetics/tree/claude/su2-yang-mills-repo-1tb9ll/su2_yang_mills_area_law},
  note    = {Unreleased. Code under the MIT License; manuscripts all rights reserved (see LICENSING.md)}
}
```

No DOI, arXiv identifier or journal reference exists for either manuscript
or for the repository. Paper 2 is known only from its citation in Paper 1,
so its entry has no date or URL.

## License and rights

The **code** is released under the MIT License ([`LICENSE`](LICENSE),
Copyright (c) 2026 James M. Lockwood). That covers the release copy of the
reproduction script, the run wrapper, the integrity checker, the tests, and
the build and CI configuration. **The manuscripts, the SI document, the
original script, the documentation and any figures are not MIT-licensed.**
They remain under the author's copyright or their respective rights holders'.
Third-party dependencies (numpy, scipy, mpmath) are not bundled and keep
their own licences. The full scope is in [`LICENSING.md`](LICENSING.md). MIT
licensing does not replace scholarly attribution.

## Contact / issues

Report reproduction failures, integrity-check failures and documentation
errors through the Issues of the hosting GitHub repository. For mathematical
corrections, see [`CONTRIBUTING.md`](CONTRIBUTING.md).
