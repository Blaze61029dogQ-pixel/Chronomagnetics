"""SI constants used throughout this package.

hbar, c, e, h, and kB are exact by the post-2019 SI definitions. G and
eps0 are measured (CODATA 2018) and carry their own uncertainty -- see
D10/C10 in the source document: a quantity proportional to G**n inherits
a relative uncertainty of |n| * u_r(G) from G alone.
"""
from __future__ import annotations

import math

H_PLANCK = 6.62607015e-34          # J s (exact, SI)
HBAR = H_PLANCK / (2 * math.pi)    # J s
C_LIGHT = 299792458.0              # m/s (exact, SI)
E_CHARGE = 1.602176634e-19         # C (exact, SI)
K_BOLTZMANN = 1.380649e-23         # J/K (exact, SI)
EPS0 = 8.8541878128e-12            # F/m (CODATA 2018; measured, not SI-exact)
G_NEWTON = 6.67430e-11             # m^3 kg^-1 s^-2 (CODATA 2018; measured)

GEV_TO_JOULE = 1.0e9 * E_CHARGE    # J per GeV (exact)
HBAR_C = HBAR * C_LIGHT            # J m
