"""Finite-temperature planar Lifshitz theory (source: Lifshitz 1956; see
REFERENCES.bib and zero_point_energy/README.md for the full citation list).

Implements the free energy per unit area between two parallel planar
half-spaces (materials 1 and 2, separation a), from the Matsubara
representation of the fluctuation-electrodynamic (Lifshitz) formula:

    F/A = (kB T / 2*pi) * sum'_{n=0}^inf  integral_0^inf k_perp dk_perp
              [ ln(1 - r_TE1 r_TE2 e^(-2 kappa_0 a))
              + ln(1 - r_TM1 r_TM2 e^(-2 kappa_0 a)) ]

with Matsubara frequencies xi_n = 2*pi*n*kB*T/hbar, vacuum gap wavenumber
kappa_0 = sqrt(k_perp^2 + xi_n^2/c^2), and the prime on the sum meaning the
n=0 term carries HALF weight (standard Lifshitz/Matsubara convention,
e.g. Bordag, Mohideen & Mostepanenko, Phys. Rep. 353, 1 (2001), Eq. (2.7)).
Reflection coefficients r_TE, r_TM come from zero_point_energy.materials
(nonmagnetic media only, mu = mu_0).

NUMERICAL ARCHITECTURE

The k_perp integral at fixed xi is rewritten in the dimensionless variable
x = 2*kappa_0*a (so kappa_0 = x/(2a), and by kappa_0 dkappa_0 = k_perp dk_perp,
k_perp dk_perp = x dx/(4 a^2)), turning a semi-infinite physical-units
integral into a well-conditioned dimensionless one with a finite lower
limit x_min = 2*a*xi/c:

    integral_0^inf k_perp dk_perp f(kappa_0)
        = (1/(4 a^2)) * integral_{x_min}^inf x * f(x/(2a)) dx

log(1 - r^2 e^(-x)) is evaluated as log1p(-r^2*exp(-x)) for numerical
stability (avoids catastrophic cancellation in log(1 - y) for small y, and
is well-defined since |r| <= 1 for a passive medium keeps the argument of
log1p in (-1, 0]). The mild integrable log singularity at x = x_min = 0
(only reached at xi = 0 for a normally-reflecting pair, e.g. two ideal
conductors) is handled by scipy.integrate.quad's adaptive subdivision,
hinted at with `points=[x_min]`.

T -> 0: rather than summing an ever-finer Matsubara ladder (which converges
slowly and reintroduces the two-nearly-equal-numbers cancellation problem
this module is built to avoid), the T -> 0 limit is taken analytically
first (kB*T*sum_n g(xi_n) -> (hbar/2*pi) * integral_0^inf g(xi) dxi as the
Matsubara spacing -> 0), giving a genuinely different, directly-integrable
formula (`zero_temperature_free_energy_per_area`) rather than a T=1e-9
finite-temperature evaluation.

MATSUBARA ZERO MODE

The n=0 term is treated explicitly (never regularized away): its
contribution depends on the low-frequency behavior of each material's
epsilon(i*xi)*xi^2 as xi -> 0, which is model-dependent -- see
zero_point_energy/materials.py's module docstring and the
`ZERO_MODE_PRESCRIPTIONS` note below for the Drude-vs-plasma distinction
this produces at T > 0.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional, Tuple

from scipy import integrate

from .constants import C_LIGHT, HBAR, K_BOLTZMANN
from .materials import DielectricModel

#: Neutral statement of a genuinely unresolved literature question -- see
#: module docstring and materials.py. This package takes no side; it
#: implements both prescriptions (DrudeModel, PlasmaModel) and reports
#: which one a given calculation used.
ZERO_MODE_PRESCRIPTIONS = """
Drude-vs-plasma TE zero mode (Matsubara n=0):

  Prescription       r_TE(xi=0)      High-T ideal-conductor-analog limit
  ----------------   -------------   ------------------------------------
  Ideal conductor    -1 (all k_perp) F/A -> -zeta(3) kB T / (4 pi a^2)
  Plasma model       != 0, model-    F/A -> -zeta(3) kB T / (4 pi a^2)
                     dependent       (matches ideal conductor, D28)
  Drude model        0 (all k_perp)  F/A -> -zeta(3) kB T / (8 pi a^2)
                                     (half the ideal/plasma value, D28)

This factor-of-2 discrepancy in the classical high-temperature limit is a
long-standing, literature-documented issue, not resolved here: see
Klimchitskaya, Mohideen & Mostepanenko, Rev. Mod. Phys. 81, 1827 (2009),
Sec. V.C, and Brevik, Ellingsen & Milton, New J. Phys. 8, 236 (2006), for a
neutral survey of the experimental and theoretical arguments on each side.
Both prescriptions are implemented (materials.DrudeModel,
materials.PlasmaModel); callers must choose one and this module reports
which was used rather than picking a default silently.
"""


@dataclass
class LifshitzResult:
    """Result and convergence diagnostics for a Lifshitz free-energy evaluation."""

    free_energy_per_area: float  # J/m^2
    te_part: float  # J/m^2, TE (s-polarization) contribution
    tm_part: float  # J/m^2, TM (p-polarization) contribution
    temperature: float  # K (0.0 for the T -> 0 limit)
    separation: float  # m
    n_matsubara_terms: int  # number of Matsubara terms summed (1 for T=0)
    converged: bool  # whether the Matsubara sum met its convergence criterion
    max_quadrature_error: float  # largest |abserr| reported by quad over all terms
    material1: DielectricModel = field(repr=False)
    material2: DielectricModel = field(repr=False)


def matsubara_frequencies(temperature: float, n_max: int) -> list:
    """xi_n = 2*pi*n*kB*T/hbar for n = 0..n_max (rad/s). T > 0 required."""
    if temperature <= 0:
        raise ValueError(f"temperature must be > 0 for a Matsubara ladder, got {temperature!r}")
    if n_max < 0:
        raise ValueError(f"n_max must be >= 0, got {n_max!r}")
    prefactor = 2 * math.pi * K_BOLTZMANN * temperature / HBAR
    return [prefactor * n for n in range(n_max + 1)]


def reflection_te(material: DielectricModel, xi: float, k_perp: float, c: float = C_LIGHT) -> float:
    """Public TE (s-polarization) reflection coefficient, r_TE(xi, k_perp)."""
    return material.reflection_coefficients(xi, k_perp, c)[0]


def reflection_tm(material: DielectricModel, xi: float, k_perp: float, c: float = C_LIGHT) -> float:
    """Public TM (p-polarization) reflection coefficient, r_TM(xi, k_perp)."""
    return material.reflection_coefficients(xi, k_perp, c)[1]


def _log1p_safe(y: float) -> float:
    """log1p(-y) guarding tiny floating-point overshoot of y above 1.0."""
    if y >= 1.0:
        y = 1.0 - 1e-300  # a passive medium has |r|<=1; clamp roundoff only
    return math.log1p(-y)


def _k_perp_integral(
    xi: float,
    a: float,
    material1: DielectricModel,
    material2: DielectricModel,
    c: float,
    epsabs: float,
    epsrel: float,
    limit: int,
) -> Tuple[float, float, float]:
    """TE and TM parts of integral_0^inf k_perp dk_perp [...] at fixed xi (D5/S5-style
    dimensionless-x reduction; see module docstring). Returns (te_value, tm_value, max_abserr).

    Units: J s^-1 (this is the k_perp-integral BEFORE the (kB T/2 pi) or
    (hbar/4 pi^2) prefactor and BEFORE dividing by 4a^2 -- those are applied
    by the caller); intermediate value has units of [k_perp^2] = m^-2, i.e.
    the raw dimensionless-x integral divided by 4a^2 below.
    """
    x_min = 2.0 * a * xi / c

    def kappa0_and_kperp(x: float):
        kappa0 = x / (2.0 * a)
        k_perp_sq = kappa0**2 - (xi / c) ** 2
        k_perp = math.sqrt(k_perp_sq) if k_perp_sq > 0 else 0.0
        return k_perp

    def integrand_te(x: float) -> float:
        k_perp = kappa0_and_kperp(x)
        r_te1 = reflection_te(material1, xi, k_perp, c)
        r_te2 = reflection_te(material2, xi, k_perp, c)
        return x * _log1p_safe(r_te1 * r_te2 * math.exp(-x))

    def integrand_tm(x: float) -> float:
        k_perp = kappa0_and_kperp(x)
        r_tm1 = reflection_tm(material1, xi, k_perp, c)
        r_tm2 = reflection_tm(material2, xi, k_perp, c)
        return x * _log1p_safe(r_tm1 * r_tm2 * math.exp(-x))

    # x_min is already the left endpoint of integration (not an interior
    # point), so quad's own adaptive endpoint handling applies; `points`
    # is for interior breakpoints and is not accepted together with an
    # infinite upper bound (scipy raises ValueError if passed here).
    te_val, te_err = integrate.quad(
        integrand_te, x_min, math.inf, epsabs=epsabs, epsrel=epsrel, limit=limit,
    )
    tm_val, tm_err = integrate.quad(
        integrand_tm, x_min, math.inf, epsabs=epsabs, epsrel=epsrel, limit=limit,
    )
    scale = 1.0 / (4.0 * a**2)
    return te_val * scale, tm_val * scale, max(te_err, tm_err) * scale


def zero_temperature_free_energy_per_area(
    a: float,
    material1: DielectricModel,
    material2: Optional[DielectricModel] = None,
    c: float = C_LIGHT,
    xi_max: float = 1e18,
    epsabs: float = 0.0,
    epsrel: float = 1e-8,
    limit: int = 200,
) -> LifshitzResult:
    """T -> 0 Lifshitz free energy (= internal energy) per unit area, J/m^2.

    F/A = (hbar/4*pi^2) * integral_0^inf dxi  integral_0^inf k_perp dk_perp [...]

    obtained by taking the Matsubara spacing to zero analytically (see
    module docstring) rather than by a finite-T evaluation at very small T.
    `xi_max` truncates the outer xi-integral; the integrand is exponentially
    suppressed once a*xi/c >> 1, so xi_max should be several times c/a
    (default is generous for laboratory-scale a >= 1 nm: a*xi_max/c ~ 3e5).
    """
    if a <= 0:
        raise ValueError(f"separation a must be > 0, got {a!r}")
    if material2 is None:
        material2 = material1

    def outer(xi: float) -> float:
        te, tm, _err = _k_perp_integral(xi, a, material1, material2, c, 0.0, epsrel, limit)
        return te + tm

    def outer_te(xi: float) -> float:
        te, _tm, _err = _k_perp_integral(xi, a, material1, material2, c, 0.0, epsrel, limit)
        return te

    def outer_tm(xi: float) -> float:
        _te, tm, _err = _k_perp_integral(xi, a, material1, material2, c, 0.0, epsrel, limit)
        return tm

    te_int, te_ierr = integrate.quad(outer_te, 0.0, xi_max, epsabs=epsabs, epsrel=epsrel, limit=limit)
    tm_int, tm_ierr = integrate.quad(outer_tm, 0.0, xi_max, epsabs=epsabs, epsrel=epsrel, limit=limit)

    prefactor = HBAR / (4.0 * math.pi**2)
    te_part = prefactor * te_int
    tm_part = prefactor * tm_int
    return LifshitzResult(
        free_energy_per_area=te_part + tm_part,
        te_part=te_part,
        tm_part=tm_part,
        temperature=0.0,
        separation=a,
        n_matsubara_terms=1,
        converged=True,
        max_quadrature_error=prefactor * max(te_ierr, tm_ierr),
        material1=material1,
        material2=material2,
    )


def finite_temperature_free_energy_per_area(
    a: float,
    temperature: float,
    material1: DielectricModel,
    material2: Optional[DielectricModel] = None,
    c: float = C_LIGHT,
    n_max: int = 100000,
    term_rel_tol: float = 1e-12,
    quad_epsrel: float = 1e-10,
    quad_limit: int = 200,
) -> LifshitzResult:
    """Finite-temperature Lifshitz free energy per unit area, J/m^2 (T > 0).

    Sums the Matsubara ladder xi_n = 2*pi*n*kB*T/hbar with the n=0 term at
    half weight (the "prime" on the sum). Terminates once a term's
    magnitude falls below `term_rel_tol` times the running partial sum's
    magnitude for a physically-decaying (exponentially suppressed) series,
    or raises if `n_max` is exhausted first -- there is no silent, arbitrary
    cutoff: `converged=False` and the terminal n are reported either way.
    """
    if a <= 0:
        raise ValueError(f"separation a must be > 0, got {a!r}")
    if temperature <= 0:
        raise ValueError(f"temperature must be > 0; use zero_temperature_free_energy_per_area for T=0")
    if material2 is None:
        material2 = material1

    xi_step = 2 * math.pi * K_BOLTZMANN * temperature / HBAR
    prefactor = K_BOLTZMANN * temperature / (2 * math.pi)

    te_sum = 0.0
    tm_sum = 0.0
    max_err = 0.0
    converged = False
    n_used = 0
    consecutive_small = 0
    for n in range(n_max + 1):
        xi_n = xi_step * n
        te_term, tm_term, err = _k_perp_integral(
            xi_n, a, material1, material2, c, 0.0, quad_epsrel, quad_limit
        )
        weight = 0.5 if n == 0 else 1.0
        te_sum += weight * te_term
        tm_sum += weight * tm_term
        max_err = max(max_err, err)
        n_used = n

        running = abs(te_sum + tm_sum)
        term_mag = abs(weight * (te_term + tm_term))
        if n > 0 and (running == 0.0 or term_mag < term_rel_tol * max(running, 1e-300)):
            consecutive_small += 1
        else:
            consecutive_small = 0
        if consecutive_small >= 3:
            converged = True
            break
    else:
        converged = False

    return LifshitzResult(
        free_energy_per_area=prefactor * (te_sum + tm_sum),
        te_part=prefactor * te_sum,
        tm_part=prefactor * tm_sum,
        temperature=temperature,
        separation=a,
        n_matsubara_terms=n_used + 1,
        converged=converged,
        max_quadrature_error=prefactor * max_err,
        material1=material1,
        material2=material2,
    )


def pressure(
    free_energy_fn,
    a: float,
    relative_step: float = 1e-4,
    **kwargs,
) -> float:
    """Casimir pressure P(a) = -d(F/A)/da via central finite difference, Pa.

    `free_energy_fn` is `zero_temperature_free_energy_per_area` or
    `finite_temperature_free_energy_per_area` (or a partial thereof);
    `**kwargs` are forwarded to it. This differentiates the free energy
    numerically rather than re-deriving a separate analytic pressure
    formula per material model; `relative_step` controls the central-
    difference step h = relative_step * a and should be validated against
    an analytically-known case (see tests/test_lifshitz.py) before trusting
    it for a new material combination.
    """
    if a <= 0:
        raise ValueError(f"separation a must be > 0, got {a!r}")
    h = relative_step * a
    f_plus = free_energy_fn(a + h, **kwargs).free_energy_per_area
    f_minus = free_energy_fn(a - h, **kwargs).free_energy_per_area
    return -(f_plus - f_minus) / (2 * h)
