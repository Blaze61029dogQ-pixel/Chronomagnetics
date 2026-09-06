"""Dielectric response on the imaginary-frequency axis, for use in lifshitz.py.

All models here supply eps(i*xi) -- the dielectric function analytically
continued to the imaginary (Matsubara) frequency axis, xi >= 0, SI units,
nonmagnetic (mu = mu_0) unless stated otherwise. This is the object the
finite-temperature Lifshitz formula actually needs (Lifshitz, 1956; see
zero_point_energy/README.md for the full reference list and
REFERENCES.bib for bibliographic details).

Reflection coefficients (nonmagnetic, imaginary frequency; e.g. Bordag,
Mohideen & Mostepanenko, Phys. Rep. 353, 1 (2001), Sec. 2; Klimchitskaya,
Mohideen & Mostepanenko, Rev. Mod. Phys. 81, 1827 (2009), Eq. (2.11)-(2.12)):

    kappa_0(xi, k_perp)   = sqrt(k_perp^2 + xi^2/c^2)              (vacuum)
    kappa(xi, k_perp)     = sqrt(k_perp^2 + eps(i*xi)*xi^2/c^2)    (medium)

    r_TM(xi, k_perp) = [eps(i*xi)*kappa_0 - kappa] / [eps(i*xi)*kappa_0 + kappa]
    r_TE(xi, k_perp) = [kappa_0 - kappa] / [kappa_0 + kappa]

CRITICAL xi -> 0 HANDLING

epsilon(0) is mathematically infinite for any model with a free-carrier
(Drude or plasma) response, because the definitions below diverge as
1/xi or 1/xi^2. What every reflection coefficient above actually needs is
NOT eps(xi) alone but the *product* eps(i*xi)*xi^2, which has a finite,
model-dependent limit as xi -> 0:

    Drude  (eps = 1 + omega_p^2/[xi(xi+gamma)]):  eps*xi^2 -> 0
    Plasma (eps = 1 + omega_p^2/xi^2):             eps*xi^2 -> omega_p^2
    Any model with finite eps(0) (dielectrics, Lorentz oscillators):
                                                    eps*xi^2 -> 0

This is exactly the physical origin of the Drude-vs-plasma TE zero-mode
distinction used in lifshitz.py: with kappa_0(xi=0) = k_perp,

    Drude / finite-eps(0):  kappa(0) = k_perp = kappa_0(0)  =>  r_TE(0) = 0
                            for every k_perp (the TE zero mode drops out).
    Plasma:                 kappa(0) = sqrt(k_perp^2 + omega_p^2/c^2) > k_perp
                            =>  r_TE(0) != 0 in general (the TE zero mode
                            survives, approaching the ideal-conductor value
                            -1 as k_perp -> 0).

Every model below therefore implements `epsilon_xi_squared(xi)` -- eps(i*xi)*xi^2
computed via its own analytic xi->0 limit -- rather than relying on
`epsilon(xi) * xi**2`, which would be an inf*0 indeterminate form at xi=0
for any conducting model. See DielectricModel.reflection_coefficients for
how this feeds into r_TE/r_TM without ever evaluating 0/0 or inf*0.

Scope: these are standard, well-documented model dielectric functions valid
over the frequency range each is normally used for (Drude/plasma: metals
from microwave through UV, ignoring interband transitions; Lorentz: a
single or a sum of bound resonances). None of these claims validity outside
its documented regime (D52 in the source ZPE document makes the same point
for the hard-cutoff mode-counting case).
"""
from __future__ import annotations

import math
from typing import Callable, Optional, Sequence, Tuple

from .constants import C_LIGHT


def _check_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return value


def _check_nonnegative(name: str, value: float) -> float:
    value = _check_finite(name, value)
    if value < 0:
        raise ValueError(f"{name} must be >= 0, got {value!r}")
    return value


def _check_positive(name: str, value: float) -> float:
    value = _check_finite(name, value)
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value!r}")
    return value


class DielectricModel:
    """Base class for a nonmagnetic dielectric response eps(i*xi), SI units.

    Subclasses implement `epsilon(xi)` and `epsilon_xi_squared(xi)`.
    `reflection_coefficients` is generic and should not normally need to be
    overridden (PerfectConductor is the one exception, since its reflection
    coefficients are not naturally expressed through a finite epsilon(xi)).
    """

    def epsilon(self, xi: float) -> float:
        """eps(i*xi), dimensionless. xi in rad/s, xi >= 0."""
        raise NotImplementedError

    def epsilon_xi_squared(self, xi: float) -> float:
        """eps(i*xi) * xi**2, computed via each model's own xi->0 limit.

        Units: (rad/s)^2 (dimensionless eps times xi^2). Must remain finite
        for all xi >= 0 for any model actually used in a Lifshitz
        calculation; see module docstring.
        """
        raise NotImplementedError

    def reflection_coefficients(self, xi: float, k_perp: float, c: float = C_LIGHT) -> Tuple[float, float]:
        """Return (r_TE, r_TM) at imaginary frequency xi and transverse momentum k_perp.

        Both dimensionless, |r| <= 1 for a passive medium. xi >= 0, k_perp >= 0.
        """
        xi = _check_nonnegative("xi", xi)
        k_perp = _check_nonnegative("k_perp", k_perp)
        kappa0 = math.sqrt(k_perp**2 + (xi / c) ** 2)
        eps_xi_sq = self.epsilon_xi_squared(xi)
        if not math.isfinite(eps_xi_sq) or eps_xi_sq < 0:
            raise ValueError(
                f"epsilon_xi_squared({xi!r}) returned non-physical value {eps_xi_sq!r}"
            )
        kappa = math.sqrt(k_perp**2 + eps_xi_sq / c**2)

        # r_TE: (kappa0 - kappa)/(kappa0 + kappa) -- guard the kappa0 == kappa
        # degenerate case (index-matched medium, or Drude/dielectric at
        # k_perp = xi = 0) so we never form a literal 0/0.
        if kappa0 == kappa:
            r_te = 0.0
        else:
            r_te = (kappa0 - kappa) / (kappa0 + kappa)

        if xi == 0.0:
            eps0 = self.epsilon(0.0)
            if math.isinf(eps0):
                # Any model with a nonzero DC conductivity (Drude, plasma):
                # standard result, model-independent (Bordag et al. 2001).
                r_tm = 1.0
            else:
                eps0 = _check_finite("epsilon(0)", eps0)
                r_tm = (eps0 * kappa0 - kappa) / (eps0 * kappa0 + kappa) if (eps0 * kappa0 + kappa) != 0 else 0.0
        else:
            eps = self.epsilon(xi)
            if not math.isfinite(eps):
                raise ValueError(f"epsilon({xi!r}) returned non-finite value {eps!r}")
            r_tm = (eps * kappa0 - kappa) / (eps * kappa0 + kappa)

        return r_te, r_tm


class PerfectConductor(DielectricModel):
    """Idealized eps -> infinity at every frequency (D24's "no eps0/mu0" limit
    pushed to a perfect metal).

    Reflection coefficients are exactly r_TE = -1, r_TM = +1 for all xi, k_perp
    (Bordag, Mohideen & Mostepanenko, Phys. Rep. 353, 1 (2001), Sec. 2.1).
    Because only r^2 enters the Lifshitz free energy, the r_TE sign is
    irrelevant to any energy or pressure computed from it. This limit
    reproduces the ideal-conductor Casimir energy/pressure exactly
    (Casimir, Proc. K. Ned. Akad. Wet. 51, 793 (1948)) and is what
    lifshitz.py's T -> 0 benchmark is checked against.
    """

    def epsilon(self, xi: float) -> float:
        _check_nonnegative("xi", xi)
        return math.inf

    def epsilon_xi_squared(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        return math.inf if xi > 0 else math.inf

    def reflection_coefficients(self, xi: float, k_perp: float, c: float = C_LIGHT) -> Tuple[float, float]:
        _check_nonnegative("xi", xi)
        _check_nonnegative("k_perp", k_perp)
        return -1.0, 1.0


class PlasmaModel(DielectricModel):
    """Lossless plasma model: eps(i*xi) = 1 + omega_p^2/xi^2.

    omega_p: plasma frequency, rad/s (omega_p = sqrt(n e^2/(eps0 m))).
    TE zero mode: SURVIVES (epsilon_xi_squared(0) = omega_p^2 != 0); see
    module docstring and D28 in the ZPE reference document, whose "ideal
    conductor or nondissipative plasma prescription" high-T limit
    (F/A -> -zeta(3) kB T/(8 pi a^2)) corresponds exactly to this model.
    """

    def __init__(self, omega_p: float):
        self.omega_p = _check_positive("omega_p", omega_p)

    def epsilon(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        if xi == 0.0:
            return math.inf
        return 1.0 + (self.omega_p / xi) ** 2

    def epsilon_xi_squared(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        return xi**2 + self.omega_p**2


class DrudeModel(DielectricModel):
    """Drude model: eps(i*xi) = 1 + omega_p^2/[xi*(xi + gamma)].

    omega_p: plasma frequency, rad/s. gamma: relaxation rate, rad/s, gamma >= 0
    (gamma = 0 degenerates to the lossless plasma model's epsilon_xi_squared,
    but is kept as a distinct class since the two prescriptions differ at
    xi = 0, see below).
    TE zero mode: VANISHES (epsilon_xi_squared(0) = 0 identically); see
    module docstring and D28's "nonmagnetic Drude metal" high-T limit
    (F/A -> -zeta(3) kB T/(16 pi a^2)), a factor of 2 below the plasma/ideal
    result. This Drude-vs-plasma zero-mode discrepancy at T > 0 is a
    genuinely debated modeling choice in the literature, not resolved here;
    see zero_point_energy/README.md and lifshitz.py for citations and a
    neutral statement of the issue (Klimchitskaya, Mohideen & Mostepanenko,
    Rev. Mod. Phys. 81, 1827 (2009), Sec. V; Brevik, Ellingsen & Milton,
    New J. Phys. 8, 236 (2006)).
    """

    def __init__(self, omega_p: float, gamma: float):
        self.omega_p = _check_positive("omega_p", omega_p)
        self.gamma = _check_nonnegative("gamma", gamma)

    def epsilon(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        if xi == 0.0:
            return math.inf
        return 1.0 + self.omega_p**2 / (xi * (xi + self.gamma))

    def epsilon_xi_squared(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        if xi == 0.0:
            return 0.0
        return xi**2 + self.omega_p**2 * xi / (xi + self.gamma)


class LorentzModel(DielectricModel):
    """Sum-of-oscillators Lorentz model on the imaginary axis:

        eps(i*xi) = eps_inf + sum_j S_j / (omega_j^2 + xi^2 + gamma_j*xi)

    This is the analytic continuation (real omega -> i*xi, so omega^2 ->
    -xi^2) of the standard real-frequency oscillator model
    eps(omega) = eps_inf + sum_j S_j/(omega_j^2 - omega^2 - i*gamma_j*omega),
    used throughout the Casimir/Lifshitz literature (e.g. Bordag, Mohideen
    & Mostepanenko, Phys. Rep. 353, 1 (2001), Sec. 2.3; Klimchitskaya,
    Mohideen & Mostepanenko, Rev. Mod. Phys. 81, 1827 (2009), Sec. II.C).

    OSCILLATOR-STRENGTH CONVENTION (do not mix with others): S_j has units
    (rad/s)^2 and is interpreted as an effective mode plasma frequency
    squared, S_j = omega_{p,j}^2. This is NOT the dimensionless
    atomic-physics oscillator strength f_j (where one instead writes
    S_j = f_j * omega_p_total^2); a model built from f_j values must be
    converted to this omega_{p,j}^2 convention before use here.

    Parameters: eps_inf >= 1 (dimensionless, high-frequency limit),
    oscillators: iterable of (omega_j, S_j, gamma_j) with omega_j > 0 (rad/s,
    resonance frequency), S_j > 0 (rad/s)^2, gamma_j >= 0 (rad/s, damping).
    A single-oscillator model is just len(oscillators) == 1.
    """

    def __init__(self, eps_inf: float, oscillators: Sequence[Tuple[float, float, float]]):
        self.eps_inf = _check_finite("eps_inf", eps_inf)
        if self.eps_inf < 1.0:
            raise ValueError(f"eps_inf must be >= 1, got {eps_inf!r}")
        oscillators = list(oscillators)
        if not oscillators:
            raise ValueError("LorentzModel requires at least one oscillator (omega_j, S_j, gamma_j)")
        checked = []
        for idx, (omega_j, s_j, gamma_j) in enumerate(oscillators):
            omega_j = _check_positive(f"oscillators[{idx}].omega_j", omega_j)
            s_j = _check_positive(f"oscillators[{idx}].S_j", s_j)
            gamma_j = _check_nonnegative(f"oscillators[{idx}].gamma_j", gamma_j)
            checked.append((omega_j, s_j, gamma_j))
        self.oscillators = tuple(checked)

    def epsilon(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        total = self.eps_inf
        for omega_j, s_j, gamma_j in self.oscillators:
            total += s_j / (omega_j**2 + xi**2 + gamma_j * xi)
        return total

    def epsilon_xi_squared(self, xi: float) -> float:
        # Finite for all xi >= 0 (every term's denominator is bounded away
        # from zero since omega_j > 0), so the generic product is safe here.
        return self.epsilon(xi) * xi**2


def single_lorentz_oscillator(eps_inf: float, omega_0: float, s: float, gamma: float) -> LorentzModel:
    """Convenience constructor: a LorentzModel with exactly one resonance."""
    return LorentzModel(eps_inf, [(omega_0, s, gamma)])


class UserDielectric(DielectricModel):
    """Wrap a user-supplied eps(i*xi) callable.

    `epsilon_func(xi)` must return a finite, dimensionless value for every
    xi > 0 used in the calculation. Because eps(0) can be legitimately
    infinite for a conducting model, the xi -> 0 limit of eps(i*xi)*xi^2
    cannot in general be recovered by calling `epsilon_func(0.0)` -- supply
    `zero_limit` (a callable taking no arguments and returning that limit)
    if the model is to be used at xi = 0 (i.e. in any finite-temperature
    Lifshitz calculation, where the n=0 Matsubara term always appears). If
    `zero_limit` is omitted, `epsilon_xi_squared(0)` falls back to
    `epsilon_func(0.0) * 0.0`, which is only correct for models with a
    finite, well-defined eps(0) (ordinary dielectrics) and will raise for
    anything that diverges there -- this is intentional: silently guessing
    a metal's zero-mode limit would misrepresent the physics.
    """

    def __init__(
        self,
        epsilon_func: Callable[[float], float],
        zero_limit: Optional[Callable[[], float]] = None,
    ):
        self._epsilon_func = epsilon_func
        self._zero_limit = zero_limit
        # Validate on a representative nonzero point so construction fails
        # fast rather than deep inside a Lifshitz quadrature.
        probe = self._epsilon_func(1.0)
        if not math.isfinite(probe):
            raise ValueError(f"epsilon_func(1.0) must be finite, got {probe!r}")

    def epsilon(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        return float(self._epsilon_func(xi))

    def epsilon_xi_squared(self, xi: float) -> float:
        xi = _check_nonnegative("xi", xi)
        if xi == 0.0:
            if self._zero_limit is not None:
                value = float(self._zero_limit())
                return _check_nonnegative("zero_limit()", value)
            eps0 = self.epsilon(0.0)
            if not math.isfinite(eps0):
                raise ValueError(
                    "UserDielectric.epsilon(0) is not finite and no zero_limit "
                    "callable was supplied; provide zero_limit=lambda: <finite "
                    "value of eps(i*xi)*xi**2 as xi->0> to use this model at xi=0."
                )
            return eps0 * 0.0
        eps = self.epsilon(xi)
        return eps * xi**2
