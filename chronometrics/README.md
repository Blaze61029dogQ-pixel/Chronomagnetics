# Chronometrics registry

Author: James Lockwood

A runnable transcription of the chronomagnetics chronometric registry:
one exact triangle (`a,b,c = 144,138,116`) seeds a Brocard phase, a
q-screen constant with an exact leakage defect, a frozen log-time phase
law, a locked recurrence-gate/spectral-operator model, the **Dark-to-Bright
Chronometric Separation** (`dark_bright.py`), and — the newest layer, in
`geophysics.py` — the **Geophysical Bridge**: mapping the dimensionless
chronometric basis onto real-time observables (angular rate, magnetic
energy density, skin depth, telluric-field proxy) for eventual testing
against real magnetometer/Kp/Dst/solar-wind data.

## Layout

- `constants.py` — triangle seed, Brocard phase, q-screen defect,
  log-time phase law, recurrence gate, bounded phase, voltage proxy,
  K_QP bright-ridge constant, and (transcribed reference data only) the
  iso-gap sensitivity vector and the source audit's own G_16 result.
  Each block is tagged EXACT / FROZEN / AUDITED / REJECTED, matching the
  status discipline in the source registry (nothing gets promoted past
  its proof level).
- `spectral.py` — the frozen spectral operator `L_chrono` on
  `kappa in [0,12]`, solved independently here by finite differences
  (not copied from the source audit) to check the `G_12` gap relation
  and the *rejected* `G_16` lead.
- `bright_ridge.py` — an independent numeric search for the bright-ridge
  local maximum, to check `K_QP` rather than just assert it.
- `dark_bright.py` — `Delta_kappa_DB`, `Delta_theta_DB`, and the
  shifted-time ratio `R_DB` between the exact leakage-null branch and the
  audited bright-ridge branch.
- `geophysics.py` — **new block**: the geophysical bridge. Real-time
  `omega_Delta(t)`/`f_Delta(t)`, the observable templates `Z_Delta(t)`,
  `L_null(t)`, `T_Gamma(t)` feeding the `B_obs(t) = B_base(t) + A_Z*Z_Delta
  + A_L*L_null + A_G*T_Gamma + epsilon(t)` residual-audit model (M1, tested
  against the null model M0), plus magnetic energy density, chronometric
  skin depth, and a Faraday-induction telluric-field proxy. Includes
  `demo_anchor()`, reproducing the source documents' worked numerical
  example at `T_0 = t_c = 86400 s`.
- `report.py` — prints the full registry and self-checks the EXACT/FROZEN
  values (including the geophysical bridge's demo anchor) against
  30-to-50-digit references transcribed from the source documents. Run
  with:

  ```
  python3 -m chronometrics.report
  ```

## Status discipline

- **EXACT** and **FROZEN** values reproduce the documented references to
  ~1e-50 (mpmath, 50 digits of precision) and are hard-checked; the
  report raises if one of these drifts.
- **AUDITED** values (`K_QP`, `G_12`, `G_16`) are *not* re-derived
  symbolically — this package re-runs its own independent numeric search
  / finite-difference solve and reports the resulting miss as a warning,
  rather than hard-coding agreement. The independent spectral solve
  lands within a few percent of the documented gaps, not on top of them;
  that gap is reported honestly rather than tuned away, since the exact
  finite-difference scheme and grid used in the original audit (run
  under the name "Termius" in the source material) is not fully
  specified in the source documents.
- The **iso-gap lock direction** (`delta_B_gate ~= -(20/7) delta_chi`)
  and its full 6-term sensitivity vector are transcribed, not re-derived,
  since they depend on a general `(A_main, kshift, sigma, chi, B_gate,
  D_defect)` parameterization of the operator that isn't fully specified
  in the source documents.
- The **geophysical bridge** (`geophysics.py`) is a further BRIDGE tag:
  dimensioned demo/proxy constants for mapping the chronometric basis
  onto real units, not intrinsic chronometric constants. Its demo-anchor
  numbers (`T_0 = t_c = 86400 s`) are hard-checked against the source
  documents to ~1e-47 in `report.py`.

## Boundary statement

None of this is a confirmed physical law. No measured voltage, clock,
flux, timing, or geophysical channel has been shown to contain this
residual. This is a closed internal chronometric object, not physics.
