# D067-ART-v1: Adaptive Resonance Tracked phononic light source

Author: James Lockwood

A runnable transcription of the reduced-order architecture audited in
*"Adaptive-Resonance-Tracked Phononic Piezoelectric Light Source: From
100 phononic metacrystals to D067-ART-v1 adaptive resonance tracking"*
(Lockwood, September 2026): a design program that screened 100 phononic
metacrystal families, converted the strongest candidate (D067, a nested
inertial core-shell resonator) into a finite electromechanical
light-source model, audited it independently, closed the coupling and
capacitance physically against PZT-5A material data, and rejected a
passive fixed-frequency production design on manufacturing-corner
robustness grounds. The frozen result, D067-ART-v1, adds adaptive
resonance tracking and adaptive electrical loading because the useful
passive resonance (Q ~= 60, ~1.7% fractional bandwidth) is narrower than
ordinary manufacturing tolerance.

## Layout

- `constants.py` -- physical constants and the monograph's own quoted
  reference values: Appendix C's physically constrained D067 parameters
  (capacitance, coupling, modal frequencies), the Section 20 operating
  point (frequency, load, power, efficiencies, safety factors, Q,
  bandwidth), and the Section 16 robustness-screen results.
- `electromechanical.py` -- the condensed coupled electromechanical
  reduced-order model from Sec. 8 (`[D_m + i*omega*Theta*Y^-1*Theta^T] u
  = F`), plus the load-power, impedance-matching, Q/bandwidth, robustness
  ratio, and linear-response scaling (`V~a`, `P~a^2`) relations used
  throughout the study (Sec. 14, 16-21).
- `photonics.py` -- optical power to photon-rate and idealized
  monochromatic photopic-lumen conversions at the 555 nm reference
  wavelength (Sec. 20).
- `report.py` -- self-check script. Run with:

  ```
  python3 -m d067_art_v1.report
  ```

## Status discipline

This package does **not** re-derive the monograph's reduced-order model
from first principles: the underlying per-branch modal mass, stiffness,
and stress-allowable values are not specified in the condensed report,
only in the (unpublished) source solver. Instead, `report.py` verifies
that the monograph's own independently quoted numbers are algebraically
consistent with each other through the documented formulas (e.g. Q from
frequency/bandwidth, peak voltage from power/load, photon rate from
optical power and photon energy, the Sec. 14 physical-closure identity
linking Theta, kappa_eff^2, C_p and effective stiffness). A failure here
means a transcription error in `constants.py`, not a change in the
underlying physics.

## Boundary statement

**REDUCED-ORDER ARCHITECTURE FREEZE -- NOT EXPERIMENTALLY VALIDATED.**

Every numerical value in the source monograph, and therefore in this
package, belongs to a reduced-order (2-DOF-class, linear, condensed)
model unless explicitly labeled otherwise. No 3-D tensor piezoelectric
finite-element model, no bench prototype, no illumination-class
performance claim, no fatigue-lifetime claim, and no thermal
certification has been performed (Appendix F/G). The full monograph is
included at
`docs/James_Lockwood_Phononic_Light_Source_Condensed_Report.pdf`.
