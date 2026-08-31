"""Geophysical bridge: mapping the chronometric basis onto measurable units.

This is NOT part of the chronometric core -- it is a residual-audit
template for testing the core against real magnetometer / geomagnetic
data. It has its own status tag: BRIDGE (dimensioned demo/proxy
constants, not intrinsic chronometric constants).

Model under test (once real data is available):

    M0 (null):          B_obs(t) = B_base(t) + epsilon(t)
    M1 (chronometric):  B_obs(t) = B_base(t) + A_Z*Z_Delta(t) + A_L*L_null(t)
                                    + A_G*T_Gamma(t) + epsilon(t)

with lambda_Delta frozen and t_c fixed or pre-anchored (the "non-post-hoc
path" -- fit A_Z, A_L, A_G only, never the frozen shape parameters).

Nothing here is a physical claim. No measured voltage, clock, flux,
timing, or geophysical channel has been shown to contain this residual.
"""
from __future__ import annotations

import mpmath as mp

from . import constants as C

mp.mp.dps = 50

MU_0 = 4 * mp.pi * mp.mpf('1e-7')  # N/A^2, vacuum permeability


# ---------------------------------------------------------------------------
# Instantaneous chronometric rate, as a function of real time t
# ---------------------------------------------------------------------------
def omega_Delta(t, t_c) -> mp.mpf:
    """omega_Delta(t) = 2*pi / ((t+t_c) * ln(lambda_Delta)) -- rad/s."""
    return C.OMEGA_DELTA / (t + t_c)


def f_Delta(t, t_c) -> mp.mpf:
    """f_Delta(t) = 1 / ((t+t_c) * ln(lambda_Delta)) -- Hz."""
    return omega_Delta(t, t_c) / (2 * mp.pi)


def chronometric_period(t, t_c) -> mp.mpf:
    return 1 / f_Delta(t, t_c)


# ---------------------------------------------------------------------------
# Observable templates, as functions of real time t (given an anchor t_c, T_0)
# ---------------------------------------------------------------------------
def Z_Delta_t(t, t_c, T_0) -> mp.mpf:
    """Z_Delta(t) = q_Delta * cos(theta_Delta(t))."""
    kappa = C.kappa_log(t, t_c, T_0)
    return C.Z_Delta_of_theta(C.theta_Delta(kappa))


def L_null_t(t, t_c, T_0) -> mp.mpf:
    """L_null(t) = delta_q_squared * cos^2(theta_Delta(t)) -- exact leakage."""
    kappa = C.kappa_log(t, t_c, T_0)
    return C.L_dark_of_theta(C.theta_Delta(kappa))


def dGamma_dt(t, t_c, T_0) -> mp.mpf:
    """Real-time derivative of the bounded phase (chain rule through kappa_log)."""
    kappa = C.kappa_log(t, t_c, T_0)
    return C.dGamma_dkappa(kappa) / ((t + t_c) * C.LN_LAMBDA_DELTA)


def T_Gamma(t, t_c, T_0, phi_star=1) -> mp.mpf:
    """Nonlinear gate template: (dGamma/dt) sin(Gamma(t)) cos(theta_Delta(t)/M)."""
    kappa = C.kappa_log(t, t_c, T_0)
    theta = C.theta_Delta(kappa)
    gamma = C.Gamma_phase(kappa)
    return phi_star * dGamma_dt(t, t_c, T_0) * mp.sin(gamma) * mp.cos(theta / C.M_HARMONIC)


def B_obs(t, t_c, T_0, B_base, A_Z, A_L, A_G, epsilon=0) -> mp.mpf:
    """M1: measured field decomposed into baseline + locked chronometric residual."""
    return (B_base
            + A_Z * Z_Delta_t(t, t_c, T_0)
            + A_L * L_null_t(t, t_c, T_0)
            + A_G * T_Gamma(t, t_c, T_0)
            + epsilon)


def null_model(B_base, epsilon=0) -> mp.mpf:
    """M0: baseline only, no chronometric terms."""
    return B_base + epsilon


# ---------------------------------------------------------------------------
# Geophysical unit layer
# ---------------------------------------------------------------------------
def magnetic_energy_density(B) -> mp.mpf:
    """u_B = B^2 / (2*mu_0) -- J/m^3."""
    return B ** 2 / (2 * MU_0)


def magnetic_energy_perturbation(B_0, delta_B) -> mp.mpf:
    """delta_u_B ~= B_0 * delta_B / mu_0 -- J/m^3, small-perturbation linearization."""
    return B_0 * delta_B / MU_0


def skin_depth(t, t_c, sigma) -> mp.mpf:
    """Chronometric skin depth in a conducting layer of conductivity sigma (S/m) -- meters.

    delta_skin(t) = sqrt(2/(mu_0*sigma*omega_Delta(t)))
                  = sqrt((t+t_c)*ln(lambda_Delta)/(pi*mu_0*sigma))
    """
    return mp.sqrt((t + t_c) * C.LN_LAMBDA_DELTA / (mp.pi * MU_0 * sigma))


def telluric_field_amplitude(r, delta_B, t, t_c) -> mp.mpf:
    """Faraday induction proxy amplitude: E_phi ~= (r/2) * delta_B * omega_Delta(t) -- V/m."""
    return (r / 2) * delta_B * omega_Delta(t, t_c)


# ---------------------------------------------------------------------------
# Demonstration anchor (T_0 = t_c = 86400 s, one sidereal day)
# ---------------------------------------------------------------------------
DEMO_T_0 = mp.mpf(86400)
DEMO_T_C = mp.mpf(86400)


def demo_anchor():
    """Reproduce the worked numerical example from the source documents."""
    omega0 = omega_Delta(0, DEMO_T_C)
    f0 = f_Delta(0, DEMO_T_C)
    period = chronometric_period(0, DEMO_T_C)

    t_null = C.inverse_kappa_log(C.kappa_null(0), DEMO_T_C, DEMO_T_0)
    t_bright = C.inverse_kappa_log(mp.mpf(C.K_QP), DEMO_T_C, DEMO_T_0)
    delay = t_bright - t_null

    B_0 = mp.mpf('50e-6')  # T
    u_B = magnetic_energy_density(B_0)
    delta_u_B_1nt = magnetic_energy_perturbation(B_0, mp.mpf('1e-9'))
    delta_u_B_50nt = magnetic_energy_perturbation(B_0, mp.mpf('50e-9'))

    skins = {sigma: skin_depth(0, DEMO_T_C, sigma) for sigma in (mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('1'))}

    e_phi_1nt = telluric_field_amplitude(mp.mpf('100e3'), mp.mpf('1e-9'), 0, DEMO_T_C)
    e_phi_50nt = telluric_field_amplitude(mp.mpf('100e3'), mp.mpf('50e-9'), 0, DEMO_T_C)

    return {
        'omega_Delta_0': omega0,
        'f_Delta_0': f0,
        'period_s': period,
        'period_hours': period / 3600,
        't_null_s': t_null,
        't_bright_s': t_bright,
        'delay_s': delay,
        'u_B': u_B,
        'delta_u_B_1nT': delta_u_B_1nt,
        'delta_u_B_50nT': delta_u_B_50nt,
        'skin_depths_km': {float(sigma): depth / 1000 for sigma, depth in skins.items()},
        'e_phi_1nT_V_per_m': e_phi_1nt,
        'e_phi_50nT_V_per_m': e_phi_50nt,
    }
