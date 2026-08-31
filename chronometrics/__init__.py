"""Chronomagnetics chronometric registry.

This package is a runnable transcription of a closed internal mathematical
object: a log-time phase model seeded by one exact triangle, {a,b,c} =
{144,138,116}. Every value here is either

  * EXACT      - a rational/triangle identity, provable in closed form,
  * FROZEN     - a fixed modelling choice (not derived, but held constant
                 across the whole registry),
  * AUDITED    - a numerically located constant (a local maximum, a
                 spectral gap) that is stable but not a closed-form identity,
  * REJECTED   - a candidate relation that was tested and did not survive
                 its own convergence audit; kept on record deliberately.

None of this is a confirmed physical law. No measured voltage, clock,
flux, timing, or geophysical channel has been shown to contain this
residual. Until real data survives null controls against it, this is an
internal chronometric object only. See `chronometrics/report.py` for a
full printed accounting, including which status tag each constant carries.
"""

from . import constants, spectral, bright_ridge, dark_bright  # noqa: F401
