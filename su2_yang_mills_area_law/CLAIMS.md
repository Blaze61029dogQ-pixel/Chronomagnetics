# Claims and evidence

This file maps statements in **Paper 1**
(`paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf`, draft of 28 September
2026) to the evidence the manuscript gives for them. For computations it also
gives the check IDs in `reproduction/SI_YangMills_reproduce_all.py` and their
recorded status (`results/quick/`, `results/full/`, run 2026-09-30). The
statements come from the manuscript and the check IDs from the script. No
mathematical content has been added or altered. Where this table and the PDF
differ, the PDF governs.

A passing check shows that a computation reproduces. It is not a proof of the
statement it supports. Only the exact and interval certificates the
manuscript names below are part of its proofs. Everything else is a
consistency check or evidence.

## Evidence labels (this file)

- **ANALYTIC**: proved by a written argument in the manuscript, or taken from
  a cited reference.
- **EXACT CERTIFICATE**: computer-assisted step in exact rational arithmetic
  (Python `fractions.Fraction`). Part of the proof.
- **INTERVAL CERTIFICATE**: computer-assisted step in outward-rounded interval
  arithmetic (`mpmath.iv`). Part of the proof.
- **NUMERICAL CROSS-CHECK**: floating-point or high-precision evaluation used as
  a consistency check or as evidence. No proof depends on it.
- **REFERENCE OUTPUT**: stored output of a run (`results/`).

The script uses its own tier labels: `EXACT`, `CERT`, `NUM`, `MC`, `REG`,
`INFO`. Its `EXACT` tier includes many floating-point or high-precision
comparisons within a tolerance, for example quadrature against closed forms
or double-precision eigenvalues. Those checks are listed here as NUMERICAL
CROSS-CHECK, even though the identity they test is proved analytically in the
manuscript. `REG` checks compare against values quoted in the author's
documents: they test reproducibility, not correctness.

## Status of the checks

| Mode | Command | Checks | PASS | FAIL | INFO | Exit | Wall time |
|---|---|---|---|---|---|---|---|
| quick | `python3 reproduction/run_reproduction.py` | 115 | 112 | 1 | 2 | 1 | 38.7 s |
| full | `python3 reproduction/run_reproduction.py --full` | 124 | 121 | 1 | 2 | 1 | 105.8 s |

The only FAIL, in both modes, is **S1/1.25**: `levin_N3_certificate.py` is
missing, so the Theorem 3.9 certificate did not run (see below).

## Paper 1: principal results

| Claim | Manuscript location | Evidence type | Script checks (status, full mode) |
|---|---|---|---|
| Area law, 4D SU(2) Wilson action, β_W < 2/3, uniform in L, loops with sides ≤ L/2 | Theorem A; proof §4 | ANALYTIC. Uses Theorem 2.1 (Durhuus–Fröhlich [7], as stated in [2]), Lemma 2.2, Proposition 2.5 and Theorem B | none. No computation checks Theorem A directly |
| W₁(μ_{η₀}, μ_{η₁}) ≤ ¼ \|η₀ − η₁\| for \|η₀\|, \|η₁\| ≤ 4 on S³ (chordal); ¼ attained as η → 0 | Theorem B; proof after Cor. 3.6 | ANALYTIC, resting on Lemma 3.4 (EXACT CERTIFICATE) | attainment: 1.2, 2.8 (PASS, NUMERICAL CROSS-CHECK) |
| Theorem C(i): Bakry–Émery holds uniformly iff K < 1/6 | Theorem C; §5.1 | ANALYTIC | 2.1-0.100, 2.1-0.167, 2.1-0.250: staggered configuration attains 2 − 12K on a 4³ torus (double precision, tolerance 1e-10). 2.2-*: random configurations stay above. 2.3: arithmetic of the CNS condition. All PASS; NUMERICAL CROSS-CHECK |
| Theorem C(ii): single-site TV criteria fail for K ≥ K_TV = 0.39629095688184401321…, the root of 6 L₁(K) = I₁(K) | Theorem C; §5.2 | ANALYTIC (TV identity; monotonicity of L₁/I₁ via association). The digits of K_TV are numerical | 2.4 (root to 20 digits; `REG`), 2.5, 2.6 (TV identity by quadrature), 2.7 (grid monotonicity), 2.7b (numerical check of the proof's ingredients). All PASS; NUMERICAL CROSS-CHECK. Computed K_TV = 0.3962909568818440132141 |
| Theorem C(iii): chordal-W₁ single-site criteria hold for K < 2/3 and fail for K ≥ 2/3 | Theorem C; §5.3 | ANALYTIC | 2.8 (attainment a(δ)/δ → 1/4), 2.9 (row sum 6K/4 = 1 at K = 2/3). PASS |
| Theorem C(iv): slab-criterion hypothesis fails for K > 4 G_{ℤ³}(0) = 1.0109… | Theorem C; §5.4 | ANALYTIC (infrared bound [10]; Watson's constant) | 2.10: 4 G_{ℤ³}(0) = 1.01092403943 from the Gamma-product closed form. PASS; NUMERICAL CROSS-CHECK |
| Numerical transition K_c = 0.9360(1) | Theorem C(iv); §5.4 | Literature value (Kanaya–Kaya [11]); not computed | none |

## Paper 1, Section 2: Dobrushin in Wasserstein form

| Claim | Location | Evidence type | Script checks |
|---|---|---|---|
| Slab criterion | Theorem 2.1 | ANALYTIC (cited: [7] Thms 1.2–1.3; [2] Thm 2.3) | none |
| SO(4) reduction; \|η_x\| ≤ 6K | Lemma 2.2 | ANALYTIC | none |
| Propagation lemmas; Wasserstein–Dobrushin covariance estimate | Lemmas 2.3–2.4; Proposition 2.5 | ANALYTIC (self-contained) | none prove it |
| Numerical tests on exactly solvable systems ("Section S5"; "no proof in this paper depends on them") | Remark 2.6 | NUMERICAL CROSS-CHECK | S5: 5.8-* and 5.9-* (covariance bound ratio ≤ 1 on exact finite systems; `REG`), 5.10–5.13 (generator reversibility, spectral identity, propagation bound, Metzler positivity). All PASS |

## Paper 1, Section 3: vMF Lipschitz constant and Levin's conjecture

| Claim | Location | Evidence type | Script checks |
|---|---|---|---|
| L(η, v) ≤ ½ √Q; equality ¼ at η = 0 | Theorem 3.1 | ANALYTIC | 1.1 (constant \|B⁴\|^{1/2}/\|S³\|^{1/2} = 1/2), 1.2 (Var_σ(v·n) = 1/4). PASS; NUMERICAL CROSS-CHECK |
| Q = c²A + s²B | Proposition 3.2 | ANALYTIC | none |
| Closed forms for A and B | Proposition 3.3 | ANALYTIC | 1.3, 1.4, 1.4b, 1.5, 1.6 (closed forms against 30–50-digit quadrature and numerical differentiation; max deviation 4.68e-31). PASS; NUMERICAL CROSS-CHECK |
| For 0 < r ≤ 4: F_B(r)/r⁸ > 8.466 × 10⁻⁴ and D_A(r)/r² > 0.3749 | Lemma 3.4 | **EXACT CERTIFICATE** | 1.7 (c₄…c₈ = 1/1152, 7/92160, 1/368640, 17/371589120, 1/9909043200), 1.8 (c₉ < 0), 1.9 (Σ_{9≤k≤80} \|c_k\|16^{k−4} = 2.1438097929853266e-05), 1.10 (tail k ≥ 81 ≤ 5.384e-43, exact rational majorant), 1.11 (margin 8.466174576257e-04 > 8.466e-4), 1.12 (d₁, d₂, d₃ = 3/8, 9/64, 143/5760), 1.13 (d_k ≥ 0 for 1 ≤ k ≤ 189 in full mode; ≤ 70 in quick mode), 1.15 (tail k ≥ 190 ≤ 9.111e-99 in full mode), 1.16 (D_A/r² > 0.3749). All PASS. Check 1.14 (`REG`, full only) gives Σ_{71..189} \|d_k\|16^{k−1} = 2.0771e-85 |
| 50-digit grid r = k/200: min F_B/r⁸ = 8.6806 × 10⁻⁴, min D_A/r² = 0.3750035, at r = 0.005 | Remark 3.5 | NUMERICAL CROSS-CHECK | 1.17 (0.0008680574544), 1.18 (0.3750035156). PASS; full grid in full mode, every 8th point in quick mode |
| L(η, v) < ¼ for 0 < \|η\| ≤ 4 | Corollary 3.6 | ANALYTIC (from 3.1, 3.3, 3.4) | 1.19 (4 sample radii; max 0.249999422547828). PASS; NUMERICAL CROSS-CHECK |
| Uniqueness for sup_a Σ_b ‖J_ab‖_op < 4 (N = 4) | Corollary 3.7 | ANALYTIC | none |
| Levin's conjecture, N = 4, all fields | Theorem 3.8 | ANALYTIC for \|g\| ≤ 4 and for r ≥ 262.45; **INTERVAL CERTIFICATE** on [4, 262.45] | 1.22: "interval certificate Λ² < 1/16 on [4, 262.45] (58 cells) + tail", max cell ≤ 0.062363, tail ≤ 0.045694 (outward-rounded). PASS. The manuscript's "59 dyadic points" gives 58 cells. The manuscript quotes 0.06237 and 0.0457. 1.21 (NUMERICAL CROSS-CHECK beyond the window): exact Neumann-flow bound 0.2500, 0.2493, 0.2454, 0.2408, 0.2339, 0.2255, 0.2215 at r = 0.5…30. PASS |
| Levin's conjecture, N = 3 (Heisenberg); uniqueness for sup_a Σ_b ‖J_ab‖_op < 3 | Theorem 3.9 | EXACT CERTIFICATE (weak fields, order ≤ 120) and INTERVAL CERTIFICATE (38 cells on [3.3, 103.53]), per the manuscript | **1.25: FAIL.** `levin_N3_certificate.py` is not present. **The computer-assisted part of Theorem 3.9 has not been reproduced from this repository** |
| For N ≥ 5 the Neumann-flow bound exceeds 1/N at small fields (0.2003 > 1/5 at N = 5, r = 0.3) | Remark 3.10 | NUMERICAL CROSS-CHECK | 1.23 (value 0.20025233; the script labels it "Remark 3.9"), 1.20 (general-N constant N^{−1/2}). PASS |

## Paper 1, Remark 1.1: comparison ranges

| Claim | Location | Evidence type | Script checks |
|---|---|---|---|
| Levin's √5/4 with [7] gives β_W < 2/(3√5) ≈ 0.298 | Abstract; §1.2; Remark 1.1 | ANALYTIC (derived); "not found recorded" | 2.3b: 0.2981424. PASS |
| Royer's geodesic bound: L_R ≤ ½√(π²/3 − 5/2); β_W < 1/(3√(π²/3 − 5/2)) | Remark 1.1 | ANALYTIC (derived from [16]); "not found recorded" | 2.11 (2/√(π²/3 − 5/2) = 2.250363624), 2.12 (slab range 0.37506060; link range 0.125020201; factor 1.777491). PASS. **Discrepancy:** Remark 1.1 prints "≈ 0.37507" for the slab range. The script's value and an independent evaluation both give 0.3750606…, which rounds to 0.37506. The manuscript is not changed here |
| Single-site geodesic criteria capped at 9π/8 < 4 (Cov(θ, cos θ) = −8/(9π)) | Remark 1.1 | ANALYTIC | 6.2: −0.282942121052258. PASS |

## Paper 1, Sections 6–7

| Claim | Location | Evidence type | Script checks |
|---|---|---|---|
| (a) MAD ≤ ½ ⇒ TV success for β_W < 1/3; (b) E₀\|v·n\| = 4/(3π); (c) transverse monotonicity; (d) κ∥ = 13/(120π), κ⊥ = 1/(30π) | Proposition 6.1 | ANALYTIC | 3.5 (arithmetic for (a)), 3.1 (b), 3.2 (c, grid), 3.7 and 3.8 (d, Richardson extrapolation, agreement to 1e-9). PASS; NUMERICAL CROSS-CHECK. The script calls this "Prop D" |
| sup MAD = 4/(3π) ⇒ TV success for β_W < π/8 | Conjecture 6.2 | **CONJECTURE.** Proved near ζ = 0 only; the manuscript calls the grid "evidence, not a proof" | 3.3-* (`REG` against "addendum v1.5"), 3.4 (grid maximum < 4/(3π), attained at θ = 90°), 3.6 (π/8 arithmetic). PASS. Evidence only |
| DF80 Sect. 5 per-bond coupling is β, not 2β; their proven range is β_W < 1/6 | Remark 7.1 | ANALYTIC (reading of [7]) | 4.1 (Tr(φ(S₁)⁻¹φ(S₂)) = 2 S₁·S₂), 4.2 (vertical-plaquette action identity on a random 4×4 configuration), 4.3. PASS; NUMERICAL CROSS-CHECK |

## Checks for Paper 2 and other "tracks" (documents not in this repository)

The script also covers **Paper 2** (the companion manuscript, reference [13]
of Paper 1) and further tracks named in its docstring ("Track 3", "Track 4",
"Track 5 spec v0.1", "Record v1.4", "addendum v1.5"). None of these documents
is in this repository. So the checks below **cannot be mapped to manuscript
statements here**. Their descriptions are the script's own.

| Section | Script description | Checks | Status (full) |
|---|---|---|---|
| S1 | "Paper 2 Cor. (Chatterjee): one-block smoothing" | 1.24 | PASS (NUM) |
| S5 | Track 2 (Paper 2 §§2–3): 18 plaquette-neighbours per link, α = 9β_W/2, threshold 2/9, plaquette-exponent audit, quaternion isometry, block incidences, "Cor. 5.5" block ceilings | 5.1–5.7, 5.4b, 5.20, 5.21 | PASS |
| S6 | Sharpness and block criteria (Paper 2 §5) | 6.1–6.9 | PASS |
| S7 | Track 4 (Paper 2 §4): character coefficients, 2D exact gap, mass-bound table | 7.1–7.6 | PASS; 7.6 INFO |
| S8 | Track 3: SU(N) zero-field linear response (Monte Carlo); "Paper 2 Lemma T7" reflection-positivity Gram matrices (check 7.10) | 8.0-*, 8.1-*, 8.2-*, 7.10 | PASS (MC and numerical; 7.10 accepts minimum eigenvalues −1.1e-06 and −3.8e-07 as PSD within tolerance −1e-5, computed in float32) |
| S9 | Track 5 specification: Lemma A ingredients, calibration, 2D prototype, critical scale l* | 9.1–9.8 | PASS; 9.5 INFO |
| S10 | Asymptotic-scaling constants (SU(2)) | 10.1–10.3 | PASS |

The supplementary progress document
(`supplementary/original/SI_YangMills_Tracks1-2_v0.1.pdf`, v0.1) gives Paper 2's
central result ("Track 2", uniqueness, clustering and a transfer-matrix gap
for β_W < 2/9) as **"Open"**, pending literature items. That document's
lemma numbering (for example "Lemmas 6.1–6.2", "Corollary 6.3",
"Prop. 5.2" for Paper 1 "v1.1") differs from the current Paper 1 draft
(Lemma 3.4, Corollary 3.6, Proposition 3.3).

## What is not claimed

- No statement about the continuum limit, continuum Yang–Mills theory,
  or a continuum mass gap (Paper 1, abstract and §8(3)). Any
  "mass gap" or "transfer-matrix gap" in Paper 2 or the SI document is a
  fixed-lattice-spacing, strong-coupling statement. The SI document says so
  explicitly: "Nothing here bears on the Clay statement."
- No area law for β_W ≥ 2/3. Theorem C(iii)–(iv) concerns the limits of the
  method.
- No result for SU(N), N ≥ 3 (Paper 1 §8(2)).
- No resolution of Levin's conjecture for N ≥ 5 (Remark 3.10).
- No priority claim beyond the manuscript's own qualified wording ("not
  found recorded"). A passing numerical check is not evidence of novelty.
