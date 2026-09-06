# D067-ART-v1 parameter provenance

Every parameter in `d067_art_v1/constants.py` traces to one of the
categories below. Where the underlying computational configuration (the
"(unpublished) source solver" referenced throughout `d067_art_v1/README.md`
and `report.py`) was not retained, this is stated explicitly as
**PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED** rather than invented. No
citation is added where none is independently verifiable.

Categories used below: *exact constant*, *literature value*,
*geometry-derived*, *solver-derived*, *fit*, *engineering assumption*,
*internal/unpublished source*, *unknown provenance*.

| Parameter | Symbol | Value | SI units | Category | Origin | Reference/source | Derivation | Uncertainty/status |
|---|---|---|---|---|---|---|---|---|
| `H_PLANCK` | h | 6.62607015e-34 | J·s | exact constant | 2019 SI redefinition | SI (2019) | defined exactly | exact, no uncertainty |
| `C_LIGHT` | c | 299792458.0 | m/s | exact constant | SI definition (1983) | SI | defined exactly | exact, no uncertainty |
| `K_CD` | K_cd | 683.0 | lm/W | exact constant | 2019 SI/CGPM photometric definition | SI (2019 SI/CGPM) | defined exactly at `NU_CD_HZ` | exact, no uncertainty (see Section 5 of the scientific audit for the exact-frequency vs. ~555 nm distinction) |
| `NU_CD_HZ` | ν_cd | 540e12 | Hz | exact constant | 2019 SI/CGPM photometric definition | SI (2019 SI/CGPM) | defined exactly | exact, no uncertainty |
| `LAMBDA_CD_M` | λ_cd | c/ν_cd (unrounded) | m | solver-derived (exact arithmetic) | derived at import time from `C_LIGHT`/`NU_CD_HZ` | this repository | `LAMBDA_CD_M = C_LIGHT / NU_CD_HZ` | exact given exact inputs; not itself an SI-defined constant |
| `REFERENCE_WAVELENGTH_M` | -- | 555e-9 | m | engineering assumption | conventional rounding used throughout Sec. 20 of the monograph | Lockwood2026D067 | rounded engineering reference, not derived from `LAMBDA_CD_M` | approximate by construction; see Section 5 of the audit |
| `BULB_RADIUS` | -- | 3.3444...e-02 | m | geometry-derived | Appendix C physical reference geometry | Lockwood2026D067 | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED | precision reflects the source solver's internal representation, not measurement |
| `ACTIVE_HEIGHT` | -- | 5.75e-02 | m | geometry-derived | Appendix C | Lockwood2026D067 | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED | as above |
| `SHELL_THICKNESS` | -- | 1.7733...e-03 | m | geometry-derived | Appendix C | Lockwood2026D067 | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED | as above |
| `PIEZO_MATERIAL` | -- | "PZT-5A" | -- | literature value (material designation only) | Appendix C | Lockwood2026D067 | material choice, not a numeric material-property citation | no independently verifiable PZT-5A material-constant citation is included here (see REFERENCES.bib note) |
| `PIEZO_COVERAGE` | -- | 0.65 | dimensionless | engineering assumption | Appendix C design choice | Lockwood2026D067 | design parameter | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED for the optimization that selected this value |
| `PIEZO_THICKNESS` | -- | 6.5e-04 | m | geometry-derived | Appendix C | Lockwood2026D067 | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED | -- |
| `PIEZO_HEIGHT_FRACTION` | -- | 0.90 | dimensionless | engineering assumption | Appendix C design choice | Lockwood2026D067 | design parameter | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `RESONATOR_MASS_SCALE` | -- | 1.00 | dimensionless | engineering assumption | Appendix C normalization | Lockwood2026D067 | defined as the normalization reference (1.0 by construction) | not a measured/fit quantity |
| `LOCAL_STIFFNESS_SCALE` | -- | 1.75 | dimensionless | fit | Appendix C, screened against 100 metacrystal families | Lockwood2026D067 | selected by the 100-family screening program described in the monograph | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED for the screening solver/data |
| `DAMPING_SCALE` | -- | 1.25 | dimensionless | fit | Appendix C, screened against 100 metacrystal families | Lockwood2026D067 | as above | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `CAPACITANCE_CP` | C_p | 1.6369e-07 | F | solver-derived | Appendix C, closed physically against PZT-5A material data per Lockwood2026D067 | Lockwood2026D067 | reduced-order electromechanical solve | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED (solver configuration not retained) |
| `COUPLING_THETA` | Θ | 1.2095e-02 | N/V (electromechanical coupling) | solver-derived | Sec. 14 physical closure | Lockwood2026D067 | Θ=√(κ_eff²·K_eff·C_p), see `electromechanical.py` | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED for the solver that produced K_eff |
| `KAPPA_EFF_SQUARED` | κ_eff² | 1.2300e-03 | dimensionless | solver-derived | Sec. 14 | Lockwood2026D067 | reduced effective electromechanical coupling measure | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `MODE_1_HZ` | -- | 183.59 | Hz | solver-derived | Appendix C modal analysis | Lockwood2026D067 | lower mechanical branch of the reduced-order model | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `MODE_2_HZ` | -- | 753.48 | Hz | solver-derived | Appendix C modal analysis | Lockwood2026D067 | upper mechanical branch | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `OPERATING_FREQUENCY_HZ` | f_op | 183.59 | Hz | solver-derived | Sec. 15/20 | Lockwood2026D067 | operating point selection near `MODE_1_HZ` | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `LOAD_RESISTANCE_OHM` | R_L | 5296.06 | Ω | solver-derived | Sec. 18/19 impedance-match estimate | Lockwood2026D067 | R_L*≈1/(ω·C_p), see `impedance_matched_load` | consistent with `CAPACITANCE_CP`/`OPERATING_FREQUENCY_HZ` to 1e-9 rel. tol (hard-checked in `report.py`) |
| `REFERENCE_BASE_ACCEL` | -- | 1.00 | m/s² (peak) | engineering assumption | Sec. 15 normalization | Lockwood2026D067 | defined as the reference input (1.0 by construction) | not measured |
| `PIEZO_AC_POWER_W` | -- | 1.2938e-04 | W | solver-derived | Sec. 19/20 | Lockwood2026D067 | reduced-order electromechanical solve at the operating point | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `OPTICAL_POWER_W` | -- | 4.4279e-05 | W | solver-derived | Sec. 20 | Lockwood2026D067 | piezo AC power × conversion-chain efficiency | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `MECH_TO_ELEC_EFFICIENCY` | -- | 1.8336e-02 | dimensionless | solver-derived | Sec. 20 | Lockwood2026D067 | reduced-order electromechanical solve | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `TOTAL_OPTICAL_EFFICIENCY` | -- | 6.2754e-03 | dimensionless | solver-derived | Sec. 20 | Lockwood2026D067 | full mechanical→electrical→optical chain | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `PEAK_VOLTAGE_V` | -- | 1.1706 | V | solver-derived | Sec. 19/20 | Lockwood2026D067 | |V|=√(2·P·R_L), hard-checked in `report.py` | consistent with `PIEZO_AC_POWER_W`/`LOAD_RESISTANCE_OHM` to 1e-12 rel. tol |
| `SHELL_SAFETY_FACTOR` | -- | 4.478 | dimensionless | solver-derived | Appendix C structural check | Lockwood2026D067 | stress-allowable ratio from the (unspecified) per-branch stress model | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED; only the ratio, not the underlying stress-allowable model, is available |
| `PIEZO_SAFETY_FACTOR` | -- | 2.016 | dimensionless | solver-derived | Appendix C structural check | Lockwood2026D067 | as above | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `HALF_POWER_BANDWIDTH_HZ` | BW | 3.0617 | Hz | solver-derived | Sec. 17 | Lockwood2026D067 | half-power bandwidth of the reduced-order resonance | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `EFFECTIVE_Q` | Q | 59.964 | dimensionless | solver-derived | Sec. 17 | Lockwood2026D067 | Q=f_op/BW, hard-checked in `report.py` | consistent with `OPERATING_FREQUENCY_HZ`/`HALF_POWER_BANDWIDTH_HZ` to 1e-12 rel. tol |
| `PHOTON_RATE_HZ` | -- | 1.2371e+14 | s⁻¹ | solver-derived | Sec. 20 | Lockwood2026D067 | P_optical/(hc/λ) at `REFERENCE_WAVELENGTH_M`, hard-checked in `report.py` | consistent with `OPTICAL_POWER_W` to 1e-9 rel. tol |
| `PHOTOPIC_LUMEN_EQUIVALENT` | -- | 3.0243e-02 | lm (idealized) | solver-derived | Sec. 20 | Lockwood2026D067 | `OPTICAL_POWER_W` × `K_CD`, hard-checked in `report.py` | consistent to 1e-9 rel. tol; idealized monochromatic figure, not a broadband LED measurement |
| `ROBUST_NOMINAL_OPTICAL_POWER_W` | -- | 4.4279e-05 | W | solver-derived | Appendix D manufacturing-corner screen | Lockwood2026D067 | nominal corner of the 2⁵=32-corner sweep | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `ROBUST_WORST_CASE_OPTICAL_POWER_W` | -- | 1.9869e-06 | W | solver-derived | Appendix D | Lockwood2026D067 | worst corner of the 32-corner sweep | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `ROBUSTNESS_RATIO` | -- | 4.4871e-02 | dimensionless | solver-derived | Sec. 16 | Lockwood2026D067 | worst/nominal ratio, hard-checked in `report.py` | consistent to 1e-9 rel. tol |
| `FIXED_POINT_ALL_DESIGN_WORST_CASE_W` | -- | 2.2840e-06 | W | solver-derived | Appendix D, passive fixed-frequency comparator design | Lockwood2026D067 | worst-case optical power for the *rejected* passive design | PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED |
| `MANUFACTURING_CORNERS` | -- | {0.05, 0.05, 0.05, 0.03, 0.10} | fractional (dimensionless) | engineering assumption | Appendix D | Lockwood2026D067 | assumed two-sided manufacturing-tolerance perturbations, not measured tolerances of an actual manufacturing line | engineering assumption, not a fit to real process data |

## Notes

- **"PROVENANCE INCOMPLETE — SOURCE NOT ARCHIVED"** means: the *category*
  of the parameter (geometry, solver output, fit, etc.) is known from the
  monograph's own section references, but the specific numerical
  procedure that produced the quoted digits (mesh/grid, iteration
  tolerance, package versions, random seed if any) was not retained
  anywhere accessible to this repository. `d067_art_v1/report.py` checks
  internal algebraic consistency between these quoted numbers, which is
  independent of that missing configuration -- see
  `SCIENTIFIC_VALIDATION.md`.
- No PZT-5A material-property citation (d33, permittivity, elastic
  compliance, etc.) is included in `REFERENCES.bib` because none could be
  independently verified against the specific values used in this
  monograph. Adding a plausible-looking materials-handbook citation
  without verifying it matches the model's actual inputs would be worse
  than leaving it out.
- Electromechanical coupling quantities (`COUPLING_THETA`,
  `KAPPA_EFF_SQUARED`, `CAPACITANCE_CP`) are explicit about their SI
  units in the table above: `COUPLING_THETA` in N/V (force per volt, the
  scalar piezoelectric transformer-ratio convention used in
  `electromechanical.py`'s condensed dynamic-stiffness equation),
  `KAPPA_EFF_SQUARED` dimensionless, `CAPACITANCE_CP` in farads.
