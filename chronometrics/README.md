# Chronometrics registry

A runnable transcription of the chronomagnetics chronometric registry:
one exact triangle (`a,b,c = 144,138,116`) seeds a Brocard phase, a
q-screen constant with an exact leakage defect, a frozen log-time phase
law, a locked recurrence-gate/spectral-operator model, and — the newest
layer, in `dark_bright.py` — the **Dark-to-Bright Chronometric
Separation** block: the closed-form gap between the exact leakage-null
branch and the audited bright-ridge branch.

## Layout

- `constants.py` — triangle seed, Brocard phase, q-screen defect,
  log-time phase law, recurrence gate, bounded phase, voltage proxy,
  K_QP bright-ridge constant. Each block is tagged EXACT / FROZEN /
  AUDITED / REJECTED, matching the status discipline in the source
  registry (nothing gets promoted past its proof level).
- `spectral.py` — the frozen spectral operator `L_chrono` on
  `kappa in [0,12]`, solved independently here by finite differences
  (not copied from the source audit) to check the `G_12` gap relation
  and the *rejected* `G_16` lead.
- `bright_ridge.py` — an independent numeric search for the bright-ridge
  local maximum, to check `K_QP` rather than just assert it.
- `dark_bright.py` — the new block: `Delta_kappa_DB`, `Delta_theta_DB`,
  and the shifted-time ratio `R_DB`.
- `report.py` — prints the full registry and self-checks the EXACT/FROZEN
  values against 50-digit references transcribed from the source
  documents. Run with:

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
  is transcribed, not re-derived, since it depends on sensitivity
  parameters (`A_main`, `kshift`, `sigma`) whose general form isn't
  fully specified in the source documents either.

## Boundary statement

None of this is a confirmed physical law. No measured voltage, clock,
flux, timing, or geophysical channel has been shown to contain this
residual. This is a closed internal chronometric object, not physics.
