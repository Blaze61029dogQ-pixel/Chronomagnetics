# Scientific validation ledger

This table is a formula-to-source traceability record. Every "Computed
value" / "Absolute error" / "Relative error" cell below was captured by
actually running the corresponding `report.py` (or `experiments/`) module
and copying its printed output -- none of these were hand-typed as "PASS".
To regenerate: run each module listed under "Module" with
`python3 -m <module>` and compare against the values here; a mismatch
means either this file is stale (re-run and update it) or a real
regression occurred.

Legend (see each package's own README for the full status discipline):

- **zero_point_energy/** = mainstream QFT / established computational physics.
- **chronometrics/** = project-specific hypothesis framework (not a
  confirmed physical law).
- **experiments/** = numerical falsification and synthetic-control studies.
- **d067_art_v1/** = independent phononic/piezoelectric research artifact
  (reduced-order architecture freeze, not experimentally validated).

Status values: **OK** = hard-checked, passed. **WARN** = an independent,
non-hard-checked re-derivation reported for information (see chronometrics
AUDITED items). **NOT DETECTED** / **INCONCLUSIVE** = a blind falsification
test's honest, non-PASS/FAIL outcome (see experiments/).

## zero_point_energy/ (mainstream QFT)

| Module | Physical result | Equation/convention | Primary reference | Secondary reference | Validation method | Computed value | Reference value | Absolute error | Relative error | Tolerance | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `zero_point_energy.casimir` | Casimir pressure, parallel plates, a=100 nm | P = -π²ħc/(240 a⁴) | Casimir1948 | LockwoodZPE2026 | `math.isclose` vs. source-document worked value | -13.001257732443657 | -13.0013 | 4.2268e-05 | 3.2510e-06 | 1e-05 | OK |
| `zero_point_energy.units` | 1 GeV⁴ → J/m³ | SI/natural-unit conversion (2019 SI) | -- (SI convention) | -- | `math.isclose` vs. source-document worked value | 2.0852156845242993e+37 | 2.085215688e+37 | 3.4757e+28 | 1.6668e-09 | 1e-08 | OK |
| `zero_point_energy.modes` | Proca (g=3) / scalar (g=1) massive ZPE density ratio | mode counting, D32 | LockwoodZPE2026 | -- | exact ratio vs. 3.0 | 3.0 | 3.0 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.modes` | Massive-field exact integral vs. large-cutoff asymptotic series | D3/D4 | LockwoodZPE2026 | -- | cross-check at k_c=1e6·(mc/ħ) | 9.003498278499658e+45 | 9.003498278499656e+45 | 2.5353e+30 | 2.8159e-16 | 1e-09 | OK |
| `zero_point_energy.resonators` | LC zero-point: V_zpf = Q_zpf/C | D59 | LockwoodZPE2026 | -- | identity at ω₀=2π·5 GHz | 1.2870577055827762e-06 | 1.2870577055827762e-06 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.resonators` | LC zero-point: I_zpf = Φ_zpf/L | D59 | LockwoodZPE2026 | -- | identity at ω₀=2π·5 GHz | 4.043411032604985e-08 | 4.043411032604984e-08 | 6.6174e-24 | 1.6366e-16 | 1e-12 | OK |
| `zero_point_energy.casimir` | Boyer sphere self-energy, two algebraic forms | D40 | Boyer1968 | LockwoodZPE2026 | cross-check of two displayed forms | 1.4598349876620968e-27 | 1.4598349876620968e-27 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.casimir` | Scalar ring (L) / interval (L) energy ratio | ζ(-1)=-1/12 regularization, D25/D26 | Elizalde1994 | LockwoodZPE2026 | exact ratio vs. 4.0 | 4.0 | 4.0 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.casimir` / `stress_tensor` | Stress-tensor T_zz equals plate pressure | D29 | Casimir1948 | LockwoodZPE2026 | identity at gap=250 nm | -0.33283219795055763 | -0.33283219795055763 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.stress_tensor` | Vacuum equation of state p = -ρ | D6/D10 | -- (standard QFT vacuum EOS) | -- | identity at ρ=4.2e30 | -4.2e+30 | -4.2e+30 | 0.0 | 0.0 | 1e-12 | OK |
| `zero_point_energy.thermal` | Hawking temperature, 1 M☉ | D71 | Hawking1975 | LockwoodZPE2026 | order-of-magnitude vs. well-known ~6.17e-8 K | 6.170073828591918e-08 | 6.17e-08 | 7.3829e-13 | 1.1966e-05 | 1e-02 | OK |
| `zero_point_energy.thermal` | Evaporation time, 1 M☉ [yr] | D72 | Hawking1975 | LockwoodZPE2026 | order-of-magnitude vs. well-known ~2.1e67 yr | 2.095682421948516e+67 | 2.1e+67 | 4.3176e+64 | 2.0560e-03 | 1e-02 | OK |
| `zero_point_energy.thermal` | Schwinger critical field, electron | D75 | Schwinger1951 | LockwoodZPE2026 | order-of-magnitude vs. well-known ~1.323e18 V/m | 1.3232854741373635e+18 | 1.323e+18 | 2.8547e+14 | 2.1578e-04 | 1e-03 | OK |

## d067_art_v1/ (independent phononic/piezoelectric research artifact)

*Internal algebraic consistency of the source monograph's own quoted
numbers -- not a re-derivation from first principles, and not
experimental validation (see `d067_art_v1/README.md` Status discipline
and `d067_art_v1/PARAMETER_PROVENANCE.md`).*

| Module | Physical result | Equation/convention | Primary reference | Secondary reference | Validation method | Computed value | Reference value | Absolute error | Relative error | Tolerance | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `d067_art_v1.electromechanical` | Effective Q = f_op / half-power bandwidth | Sec. 17 | Lockwood2026D067 | -- | identity vs. quoted EFFECTIVE_Q | 59.96447405721183 | 59.96447405721183 | 0.0 | 0.0 | 1e-12 | OK |
| `d067_art_v1.electromechanical` | ω_op·R_L·C_p ≈ 1 (impedance-matched load) | Sec. 19 | Lockwood2026D067 | -- | identity from quoted operating point | 1.0000000000000024 | 1.0 | 2.4425e-15 | 2.4425e-15 | 1e-09 | OK |
| `d067_art_v1.electromechanical` | Peak voltage from P=0.5V²/R_L | Sec. 19/20 | Lockwood2026D067 | -- | identity vs. quoted PEAK_VOLTAGE_V | 1.1706456615561858 | 1.1706456615561858 | 0.0 | 0.0 | 1e-12 | OK |
| `d067_art_v1.electromechanical` | Physical-closure round trip: Θ(K_eff) = Θ | Sec. 14 | Lockwood2026D067 | -- | round-trip inversion consistency | 0.012094963159784465 | 0.012094963159784464 | 1.7347e-18 | 1.4343e-16 | 1e-12 | OK |
| `d067_art_v1.photonics` | Photon rate at ~555 nm from optical power | E=hc/λ (Sec. 20) | -- (Planck-Einstein relation) | Lockwood2026D067 | identity vs. quoted PHOTON_RATE_HZ | 123712829446936.03 | 123712829446936.03 | 0.0 | 0.0 | 1e-09 | OK |
| `d067_art_v1.photonics` | Idealized photopic lumen equivalent at ~555 nm | K_cd=683 lm/W at exactly 540e12 Hz (Sec. 20) | -- (SI photometric definition, 2019 SI/CGPM) | Lockwood2026D067 | identity vs. quoted PHOTOPIC_LUMEN_EQUIVALENT | 0.030242604690756576 | 0.030242604690756576 | 0.0 | 0.0 | 1e-09 | OK |
| `d067_art_v1` (report cross-check) | Optical/mechanical efficiency ratio = optical/piezo power ratio | Sec. 20 | Lockwood2026D067 | -- | identity of two independently quoted ratios | 0.34224000000000004 | 0.34224000000000004 | 0.0 | 0.0 | 1e-09 | OK |
| `d067_art_v1.electromechanical` | Robustness ratio = worst-case/nominal optical power | Sec. 16 | Lockwood2026D067 | -- | identity vs. quoted ROBUSTNESS_RATIO | 0.044871155233013806 | 0.044871155233013806 | 0.0 | 0.0 | 1e-09 | OK |

## chronometrics/ (project-specific hypothesis framework -- not a confirmed physical law)

*All references are internal to this repository's own registry
(`chronometrics/constants.py`, `chronometrics/README.md`); this is
original project-specific work, not a transcription of a published paper.
Tolerances are absolute, in `mpmath` 50-digit precision (see
`chronometrics/report.py` source for the exact tolerance passed to each
check).*

| Module | Physical result | Equation/convention | Primary reference | Secondary reference | Validation method | Computed value | Reference value | Absolute error | Tolerance | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `chronometrics.constants` | Triangle side \|CA\| = b [EXACT] | Heron/coordinate model | this repository | -- | mpmath identity | 138.0 | 138 | 0.0 | 1e-30 | OK |
| `chronometrics.constants` | Brocard phase seed β_Δ [EXACT] | tan(β_Δ)=Area/13309 | this repository | -- | 50-digit mpmath vs. transcribed reference | 0.50997646765152867533... | 0.50997646765152867533... | 5.3455e-51 | 1e-40 | OK |
| `chronometrics.constants` | q-screen constant q_Δ [EXACT] | q_Δ=7444/√Area² | this repository | -- | 50-digit mpmath vs. transcribed reference | 0.99998737687837740309... | 0.99998737687837740309... | 2.6728e-51 | 1e-40 | OK |
| `chronometrics.constants` | Leakage-null branch κ_null(0) [EXACT, in form] | cos(θ_Δ)=0 | this repository | -- | 50-digit mpmath vs. transcribed reference | 0.16883472431271515108... | 0.16883472431271515108... | 3.0069e-51 | 1e-30 | OK |
| `chronometrics.constants` | Bright-ridge constant K_QP [AUDITED, not exact] | K_QP=(38/219)·q_Δ | this repository | -- | 50-digit mpmath vs. transcribed reference | 0.17351379142181891012... | 0.17351379142181891012... | 4.3432e-51 | 1e-30 | OK |
| `chronometrics.bright_ridge` | Independent numeric bright-ridge search vs. canonical K_QP [AUDITED] | local-max search | this repository | -- | independent numeric search, NOT hard-checked | 0.178342684347022 | 0.1735137914218189 | miss=4.829e-03 | -- | WARN (informational) |
| `chronometrics.spectral` | Frozen operator gap G_12 vs. target [AUDITED, not exact] | independent finite-difference re-solve | this repository | -- | independent finite-difference solve, NOT hard-checked | 1.694936083656 | 1.603134129294 | rel. miss=5.726e-02 | -- | WARN (informational) |
| `chronometrics.dark_bright` | Dark-to-bright separation Δκ_DB | closed-form of the registry | this repository | -- | 50-digit mpmath vs. transcribed reference | 0.0046790671091037590406... | 0.0046790671091037590406... | 1.2946e-51 | 1e-30 | OK |
| `chronometrics.geophysics` | Chronometric period under demo anchor (T₀=t_c=86400 s) | geophysical bridge (BRIDGE, proxy only) | this repository | -- | 50-digit mpmath vs. transcribed reference | 27575.358847627464325521... s | 27575.358847627464325521... s | 0.0 | 1e-25 | OK |
| `chronometrics.geophysics` | Dark-to-bright delay under demo anchor | geophysical bridge (BRIDGE, proxy only) | this repository | -- | 50-digit mpmath vs. transcribed reference | 136.27205240371491277434... s | 136.27205240371491277434... s | 6.4317e-47 | 1e-25 | OK |

## experiments/ (numerical falsification and synthetic-control studies)

*Not a re-derivation of physics from a paper -- these test whether the
chronometrics target frequency emerges from RCSJ junction dynamics without
being injected into the analyzed observable (see
`experiments/junction_log_periodic_simulation.py` module docstring for the
blind pipeline and why the earlier, circular version was wrong).*

| Module | Physical result | Equation/convention | Primary reference | Secondary reference | Validation method | Computed value | Reference value | Absolute error | Relative error | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `experiments.log_periodic_utils` | FFT peak of sin(ω·u) recovered in log-time (positive control) | ω=2π·f_cycles | this repository | -- | blind FFT peak recovery, THEN compared to injected ω | ω=19.5311847963 rad | ω=19.6866780063 rad | 0.1555 | 0.0079 | DETECTED |
| `experiments.log_periodic_utils` | FFT peak of \|sin(ω·u)\| recovered in log-time (abs-sine control) | abs-sine period = π/ω ⟹ FFT peak at 2ω | this repository | -- | blind FFT peak recovery, THEN compared to 2×injected ω | ω=39.5902394520 rad | 2ω=39.3733560125 rad | 0.2169 | 0.0055 | DETECTED |
| `experiments.junction_log_periodic_simulation` | Blind order-parameter r(t) spectral peak vs. chronometrics target ω_LOG | RCSJ network → Kuramoto order parameter → log-time FFT (no injection) | this repository | chronometrics.constants.OMEGA_DELTA | blind FFT peak recovery, THEN compared to ω_LOG | ω=0.7670801821 rad | ω_LOG=19.6866780063 rad | 18.9196 | 0.9611 | NOT DETECTED |

The last row is the headline falsification result: the current
reduced-order RCSJ junction model, analyzed without any injected target,
does **not** reproduce the chronometrics log-periodic frequency. This is
reported as a genuine null result (see Section 19 of the audit and
`experiments/junction_log_periodic_simulation.py`) -- it is not tuned,
filtered, or hidden.
