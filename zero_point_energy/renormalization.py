"""Regulator independence: the absolute zero-point sum is divergent, but a
geometry-dependent observable built from it has a finite, regulator-
independent limit.

Benchmark: a massless scalar field on a 1D interval [0, L] with Dirichlet
boundaries has mode frequencies omega_n = n*pi*c/L (n = 1, 2, 3, ...). The
bare ground-state energy E = (1/2)*hbar*sum_n omega_n is divergent; the
renormalized (regulator-removed) Casimir energy is the finite constant

    E_C = -pi*hbar*c / (24*L)

(this is D26 in the ZPE reference document; zero_point_energy.casimir
already implements it as `scalar_interval_energy` -- this module exists to
demonstrate, by four independent regularization routes, that the same
finite answer is what remains after the regulator is removed, not to
recompute a different result).

FOUR REGULARIZATION ROUTES

1. Exponential cutoff (`exponential_cutoff_remainder`): sum_n n*e^(-n*a) has
   the exact closed form e^(-a)/(1-e^(-a))^2 (mpmath, arbitrary precision --
   the whole point of this route is that as the regulator a -> 0 the sum
   diverges as 1/a^2, and naively subtracting two large floating-point
   numbers of nearly equal magnitude loses precision catastrophically; see
   PRECISION NOTE below).

2. Mode-sum-minus-continuum (`mode_sum_minus_continuum_remainder`): the same
   subtraction, but computed as [regularized discrete sum] minus
   [regularized continuum integral int_0^inf x*e^(-a*x) dx], each evaluated
   independently (the sum via its closed form, the integral via
   scipy.integrate.quad) rather than combined into one algebraic
   expression -- a genuinely different computational path to the same
   remainder.

3. Zeta-regularization (`zeta_regularized_energy`): sum_n n is analytically
   continued to zeta(-1) = -1/12 (Riemann 1859's analytic continuation;
   see e.g. Elizalde et al., "Zeta Regularization Techniques with
   Applications" (World Scientific, 1994) for the mathematical
   justification of zeta regularization in this context). Computed here via
   mpmath's independent zeta-function implementation, not by hard-coding
   the fraction -1/12.

4. Abel-Plana (`abel_plana_remainder`): the Abel-Plana formula
   sum_{n=0}^inf f(n) = f(0)/2 + int_0^inf f(x)dx
                          + i*int_0^inf [f(it)-f(-it)]/(e^(2*pi*t)-1) dt
   applied to f(x) = x*e^(-a*x) reduces (see derivation in this module's
   source comments) to a purely REAL integral that needs no divergent
   subtraction at all, even at a=0 -- a genuinely independent confirmation
   that does not share the exponential-cutoff route's cancellation risk.

PRECISION NOTE (routes 1-2): as a -> 0, sum_n n*e^(-n*a) ~ 1/a^2 - 1/12 +
O(a^2). At a = 1e-4, 1/a^2 = 1e8 while the finite remainder is ~0.083 --
representing this subtraction in IEEE double precision (~16 significant
digits) leaves only ~8 digits of accuracy in the remainder, and the
situation degrades as a shrinks further. Both routes here therefore use
mpmath at 50 decimal digits of precision throughout, so the subtraction
1/a^2 - (huge intermediate) - (huge intermediate) never loses more than a
handful of the 50 digits carried -- an explicit, controlled precision
budget rather than hoping IEEE double precision happens to be enough.

An electromagnetic 3D analytic benchmark (ideal parallel plates,
E/A = -pi^2*hbar*c/(720*a^3), P = -pi^2*hbar*c/(240*a^4), Casimir 1948) is
also provided via `parallel_plate_benchmark`, cross-checked against the
independent finite-temperature-Lifshitz T->0 calculation in
zero_point_energy.lifshitz (see tests/test_renormalization.py and
tests/test_lifshitz.py) -- regulator independence demonstrated by an
entirely different numerical method (Matsubara/Fresnel sum vs 1D mode
counting) arriving at the same finite answer.

REGULATOR vs RENORMALIZED OBSERVABLE: nothing here suggests that analytic
continuation makes the divergent absolute vacuum level itself measurable.
Only the finite geometry-dependent *difference* (interval vs free space,
or equivalently the L-dependent piece surviving regulator removal) is a
renormalized observable; the regulator-dependent pieces subtracted along
the way (the 1/a^2 term, the free-space continuum) are convention, not
physics (D24/S8 in the ZPE reference document make the same point for the
3D hard-cutoff case).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import mpmath as mp
from scipy import integrate

from .constants import C_LIGHT, HBAR

_ZETA_MINUS_ONE_EXACT = mp.mpf(-1) / 12


@dataclass
class RegulatorResult:
    """One regularization route's remainder and how it was obtained."""

    method: str
    regulator_value: float  # the regulator parameter used (0.0 for methods with no regulator)
    remainder: float  # dimensionless: should -> -1/12 as the regulator is removed
    reference: float = -1.0 / 12.0
    absolute_error: float = 0.0

    def __post_init__(self):
        self.absolute_error = abs(self.remainder - self.reference)


def exponential_cutoff_remainder(a: float, dps: int = 50) -> RegulatorResult:
    """Route 1: sum_{n=1}^inf n*e^(-n*a) - 1/a^2, via mpmath closed form.

    sum_{n=1}^inf n*x^n = x/(1-x)^2 for |x|<1; with x=e^(-a) this is
    e^(-a)/(1-e^(-a))^2. The 1/a^2 subtraction is the UV-divergent,
    regulator-dependent piece (physically a vacuum-normalization
    convention, D2/D8-style); the remainder converges to -1/12 as a -> 0
    like O(a^2) (verified in tests/test_renormalization.py).
    """
    if a <= 0:
        raise ValueError(f"regulator a must be > 0, got {a!r}")
    with mp.workdps(dps):
        a_mp = mp.mpf(a)
        closed_form = mp.e ** (-a_mp) / (1 - mp.e ** (-a_mp)) ** 2
        remainder = closed_form - 1 / a_mp**2
        return RegulatorResult(method="exponential_cutoff", regulator_value=a, remainder=float(remainder))


def mode_sum_minus_continuum_remainder(a: float, dps: int = 50) -> RegulatorResult:
    """Route 2: [regularized discrete sum] minus [regularized continuum
    integral], each obtained independently (not by algebraic simplification
    of the same closed form as route 1).
    """
    if a <= 0:
        raise ValueError(f"regulator a must be > 0, got {a!r}")
    with mp.workdps(dps):
        a_mp = mp.mpf(a)
        discrete_sum = mp.e ** (-a_mp) / (1 - mp.e ** (-a_mp)) ** 2  # sum_n n e^{-na}, closed form
        continuum_integral = mp.quad(lambda x: x * mp.e ** (-a_mp * x), [0, mp.inf])  # = 1/a^2
        remainder = discrete_sum - continuum_integral
        return RegulatorResult(
            method="mode_sum_minus_continuum", regulator_value=a, remainder=float(remainder)
        )


def zeta_regularized_energy(dps: int = 50) -> RegulatorResult:
    """Route 3: sum_{n=1}^inf n -> zeta(-1), via mpmath's independent zeta
    implementation (not the hard-coded fraction -1/12)."""
    with mp.workdps(dps):
        value = mp.zeta(-1)
        return RegulatorResult(method="zeta_regularization", regulator_value=0.0, remainder=float(value))


def _abel_plana_correction_integral(a: float, limit: int = 200) -> float:
    """int_0^inf t*cos(a*t)/(e^(2*pi*t)-1) dt, written to avoid overflow
    (exp(-2*pi*t)-based form instead of exp(2*pi*t)-1, and the t->0
    removable singularity handled explicitly rather than approximated)."""

    def integrand(t: float) -> float:
        if t == 0.0:
            return 1.0 / (2.0 * math.pi)  # lim_{t->0} t/(e^{2*pi*t}-1)
        return t * math.cos(a * t) * math.exp(-2.0 * math.pi * t) / (-math.expm1(-2.0 * math.pi * t))

    value, _err = integrate.quad(integrand, 0.0, math.inf, limit=limit)
    return value


def abel_plana_remainder(a: float = 0.0, limit: int = 200) -> RegulatorResult:
    """Route 4: Abel-Plana applied to f(x) = x*e^(-a*x).

    Derivation (real-valued after simplification): for f(x) = x*e^(-a*x),
    f(it) - f(-it) = 2*i*t*cos(a*t), so the Abel-Plana correction integral
    i*int_0^inf [f(it)-f(-it)]/(e^(2*pi*t)-1) dt reduces to
    -2*int_0^inf t*cos(a*t)/(e^(2*pi*t)-1) dt -- purely real, no complex
    arithmetic needed. Together with f(0)/2 = 0 and int_0^inf f(x)dx = 1/a^2
    (a>0), this reproduces sum_{n=0}^inf n*e^(-n*a) = 1/a^2 - 2*I(a); at
    a=0 the 1/a^2 term is simply absent (int_0^inf x dx does not appear)
    and this function directly returns -2*I(0) = -1/12 with no divergent
    piece ever computed -- a genuinely independent confirmation that never
    shares the exponential-cutoff route's cancellation risk (see
    PRECISION NOTE in the module docstring).
    """
    if a < 0:
        raise ValueError(f"a must be >= 0, got {a!r}")
    integral = _abel_plana_correction_integral(a, limit=limit)
    return RegulatorResult(method="abel_plana", regulator_value=a, remainder=-2.0 * integral)


def renormalized_casimir_energy_1d_interval(
    length: float,
    method: str = "zeta",
    hbar: float = HBAR,
    c: float = C_LIGHT,
    regulator: float = 1e-6,
) -> float:
    """Renormalized 1D Dirichlet-interval Casimir energy, E_C = -pi*hbar*c/(24*L), Joules.

    `method` selects which of the four routes above supplies the -1/12
    remainder; `regulator` is only used by the exponential-cutoff and
    mode-sum-minus-continuum routes (dimensionless; smaller -> closer to
    the true a->0 limit but see PRECISION NOTE -- mpmath's 50-digit default
    keeps this safe well below regulator ~1e-15).
    """
    if length <= 0:
        raise ValueError(f"length must be > 0, got {length!r}")
    dispatch = {
        "exponential": lambda: exponential_cutoff_remainder(regulator).remainder,
        "mode_sum": lambda: mode_sum_minus_continuum_remainder(regulator).remainder,
        "zeta": lambda: zeta_regularized_energy().remainder,
        "abel_plana": lambda: abel_plana_remainder(0.0).remainder,
    }
    if method not in dispatch:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(dispatch)}")
    remainder = dispatch[method]()
    # E0 = (1/2)*hbar*sum_n omega_n = (1/2)*hbar*(pi*c/L)*sum_n n
    #    = hbar*pi*c/(2*L) * remainder, remainder -> -1/12 gives -pi*hbar*c/(24*L)
    return hbar * (math.pi * c / length) * remainder / 2.0


def parallel_plate_benchmark(a: float, hbar: float = HBAR, c: float = C_LIGHT):
    """Electromagnetic 3D analytic benchmark (Casimir 1948): (E/A, P).

    E/A = -pi^2*hbar*c/(720*a^3), P = -pi^2*hbar*c/(240*a^4). Delegates to
    zero_point_energy.casimir (the same D5/D16 formulas already validated
    in zero_point_energy.report) rather than redefining them, so this
    module's role is purely to state the benchmark for regulator-
    independence comparisons -- see tests/test_renormalization.py, which
    cross-checks it against the independent T->0 Lifshitz calculation.
    """
    from .casimir import plate_energy_per_area, plate_pressure

    return plate_energy_per_area(a), plate_pressure(a)
