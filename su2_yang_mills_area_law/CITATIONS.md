# Citations and attribution

BibTeX for everything below is in [`REFERENCES.bib`](REFERENCES.bib).
Machine-readable citation metadata for the repository is in
[`CITATION.cff`](CITATION.cff).

## Verification status of the bibliographic data

These records were prepared on 2026-09-30 in an environment whose network
policy refused direct access to `doi.org`, `api.crossref.org` and
`arxiv.org` (HTTP 403 on CONNECT). **No reference was checked against a
retrieved primary record.** Each entry was compared with web-search results
that listed the publisher or arXiv page. Such entries are marked
*search-corroborated*. A DOI appears only when it was visible inside a
publisher URL in those results. Re-check the DOIs and page ranges against
Crossref or the publisher before relying on them.

## How to cite

| Work | Status | BibTeX key |
|---|---|---|
| Paper 1: J. M. Lockwood, *Area law for four-dimensional SU(2) lattice Yang–Mills theory at β_W < 2/3, and the limits of single-site mixing criteria*, draft, 28 September 2026, Spectrality Institute | Unpublished draft. No DOI or arXiv identifier. PDF in `paper/original/` | `lockwood2026arealaw` |
| Paper 2: J. M. Lockwood, *A direct Wasserstein–Dobrushin approach to four-dimensional SU(2) lattice Yang–Mills theory: uniqueness, explicit clustering and a transfer-matrix gap for β_W < 2/9*, companion paper (draft) | Unpublished draft, cited as [13] in Paper 1. **Not in this repository**; no date or URL available | `lockwood_companion_dobrushin` |
| SI progress document: J. M. Lockwood, *Yang–Mills, Tracks 1 and 2: …*, draft v0.1, 28 September 2026 | Unpublished. PDF in `supplementary/original/` | `lockwood2026si` |
| This repository | Unreleased; no DOI. Version label `draft-2026-09-28`. Cite the git commit you used | `lockwood2026su2repo` |

## Works cited by Paper 1

Numbering follows the manuscript's reference list. The manuscript's entries
are unchanged. Differences found are listed here only.

| # | Work | Status | Difference from the manuscript's entry |
|---|---|---|---|
| [1] | Cao, Nissim, Sheffield, arXiv:2505.16585 | search-corroborated (arXiv) | none; no journal version found |
| [2] | Cao, Nissim, Sheffield, arXiv:2509.04688 | search-corroborated (arXiv) | none confirmed (one search summary mentioned "to appear in Proc. AMS"; unconfirmed) |
| [3] | Chatterjee, CMP 377 (2020) 307–340 | search-corroborated; DOI 10.1007/s00220-020-03738-9 | none |
| [4] | Chatterjee, CMP 385 (2021) 1007–1039 | search-corroborated; DOI 10.1007/s00220-021-04086-y | none |
| [5] | Dobrushin, Theory Probab. Appl. 15 (1970) 458–486 | search-corroborated; DOI 10.1137/1115049 | none |
| [6] | Dyson, Lieb, Simon, J. Stat. Phys. 18 (1978) 335–383 | search-corroborated; DOI 10.1007/BF01106729 | none |
| [7] | Durhuus, Fröhlich, CMP 75 (1980) 103–151 | search-corroborated; DOI 10.1007/BF01222514 | none |
| [8] | Föllmer, J. Funct. Anal. 46 (1982) 387–395 | search-corroborated | none |
| [9] | Dorlas, Savoie, arXiv:2305.19371 | search-corroborated | **Journal version exists:** Rev. Math. Phys. 37 (2025), DOI 10.1142/S0129055X25300018 (per search results). The manuscript cites the preprint only |
| [10] | Fröhlich, Simon, Spencer, CMP 50 (1976) 79–95 | search-corroborated; DOI 10.1007/BF01608557 | none |
| [11] | Kanaya, Kaya, Phys. Rev. D 51 (1995) 2404–2410 | search-corroborated; DOI 10.1103/PhysRevD.51.2404 | Publisher title reads "three-dimensional" (hyphenated). End page 2410 not confirmed |
| [12] | Künsch, CMP 84 (1982) 207–222 | search-corroborated | none |
| [13] | Lockwood, companion paper (draft) | not externally verifiable | — |
| [14] | Levin, CMP 78 (1980) 65–74 | search-corroborated | none; no DOI found |
| [15] | Osterwalder, Seiler, Ann. Phys. 110 (1978) 440–471 | search-corroborated | none |
| [16] | Royer, Ann. Inst. H. Poincaré Phys. Théor. 44 (1986) 29–38 | search-corroborated (Numdam) | none |
| [17] | Shen, Zhu, Zhu, CMP 400 (2023) 805–851 | search-corroborated; DOI 10.1007/s00220-022-04609-1 | none |
| [18] | Wilson, Phys. Rev. D 10 (1974) 2445 | search-corroborated; DOI 10.1103/PhysRevD.10.2445 | none (a search summary gave pages 2445–2459; unconfirmed) |

## Established results versus claims originating in these manuscripts

**Established results the manuscripts cite and build on.** The credit
belongs to the cited authors.

| Result used | Source cited in Paper 1 |
|---|---|
| Wilson's area-law criterion for confinement | Wilson [18] |
| Area law at sufficiently small β by cluster expansion (non-explicit threshold) | Osterwalder–Seiler [15, Thm 5.1] |
| Reduction of ν-dimensional lattice gauge theory to (ν−1)-dimensional σ-models in random gauge fields; the slab criterion (Theorem 2.1) | Durhuus–Fröhlich [7], as stated in Cao–Nissim–Sheffield [2, Thm 2.3] |
| Dobrushin's uniqueness criterion | Dobrushin [5] |
| Covariance estimate in total-variation form; decay of correlations under Dobrushin's condition | Föllmer [8]; Künsch [12] (and Gross, per Remark 2.6) |
| Coupling-based Wasserstein restatement of Dobrushin's theorem | Dorlas–Savoie [9] |
| Wasserstein estimate W₁(μ_h, μ_h′) ≤ (√5/N)\|h − h′\| for N-vector models, the √5 → 1 conjecture, and the transverse and longitudinal estimates reused in Theorems 3.8 and 3.9 | Levin [14] (with Dyson–Lieb–Simon [6]) |
| Geodesic Lipschitz-variance bound C(3) < π²/3 − 5/2 | Royer [16] |
| Infrared bound and Gaussian domination | Fröhlich–Simon–Spencer [10] |
| Numerical critical coupling K_c = 0.9360(1) of the 3D O(4) model | Kanaya–Kaya [11] |
| Area law for β_W < 1/6 by the Bakry–Émery method | Cao–Nissim–Sheffield [2], building on Shen–Zhu–Zhu [17] |
| Background on probabilistic approaches to confinement | Chatterjee [3, 4] |

**Claims originating in Paper 1** (the author's own results, as stated by
the manuscript):

- Theorem A (area law for β_W < 2/3). The manuscript describes this as the
  range "asserted without proof by Durhuus and Fröhlich in 1980".
- Theorem B and Theorem 3.1 (Neumann-flow bound; optimal constant 1/4 for
  \|η\| ≤ 4), with Propositions 3.2–3.3, Lemma 3.4 and Corollary 3.6.
- Theorem 3.8 (Levin's conjecture for N = 4) and Theorem 3.9 (N = 3), with
  Corollary 3.7.
- Theorem C (limits of single-site criteria), Proposition 6.1, and
  Conjecture 6.2 (unproved).
- The self-contained Wasserstein proofs of Section 2.2 (Lemmas 2.3–2.4,
  Proposition 2.5). The manuscript attributes the method to [5, 8, 12] and
  calls its proofs "the Wasserstein analogues".
- Remark 7.1 (a normalisation reading of [7]).
- The derived ranges β_W < 2/(3√5) and β_W < 1/(3√(π²/3 − 5/2)), which the
  manuscript reports as "derivable; not found recorded". This is a
  literature-search statement, not an established priority claim.

**Claims attributed to Paper 2 and the SI document** (uniqueness, clustering
and a transfer-matrix gap for β_W < 2/9 at fixed lattice spacing): Paper 2 is
not available here. The SI document (v0.1) labels its central result
"(Open)".

## Methods used in the code that Paper 1 does not cite

These attributions were added by the repository maintainer to credit
methods that the reproduction script implements. They are not part of the
manuscript's bibliography. The author may wish to add them to the
manuscripts.

| Code location | Method | Suggested citation (search-corroborated) |
|---|---|---|
| S2/2.10; Paper 1 §5.4 ("Watson's W") | Simple-cubic lattice Green function at the origin; Gamma-product closed form | Watson (1939), `watson1939`; Glasser–Zucker (1977), `glasserzucker1977`. Search results describe the Gamma-function form as Glasser–Zucker's. The prefactor was not checked against the paper |
| S8, `haar_su` | Haar-random SU(N) by QR with phase correction | Mezzadri (2007), `mezzadri2007` |
| S10 | One- and two-loop β-function coefficients b₀, b₁ | Gross–Wilczek (1973), Politzer (1973), Caswell (1974), Jones (1974) |

MIT licensing of the code (see [`LICENSING.md`](LICENSING.md)) does not
replace scholarly attribution. Anyone reusing the methods should cite the
manuscripts and the original sources above.
