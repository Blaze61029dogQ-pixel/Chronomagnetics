"""Coupled electromechanical reduced-order model (Sec. 8, 18, 19, 21).

Transcribes the condensed linear system used throughout the monograph:
the electrical subsystem is condensed into the mechanical dynamic
stiffness so electrical loading feeds back into the mechanical response,
rather than being computed after an uncoupled mechanical solve.

    (K - omega^2 M + i omega C) u - Theta V = F
    i omega Theta^T u + Y V = 0,  Y = 1/R_L + i omega C_p
    => [D_m + i omega Theta Y^-1 Theta^T] u = F

This module represents the single-coordinate (scalar Theta, scalar modal
mass/stiffness/damping) reduction used for the headline operating point;
it does not resolve the full multi-branch mechanical system, 3-D stress
fields, or nonlinear/thermal effects (Appendix F).
"""
from __future__ import annotations

import math


def electrical_admittance(omega: float, load_resistance: float, capacitance: float) -> complex:
    """Y = 1/R_L + i*omega*C_p (Sec. 8)."""
    return 1.0 / load_resistance + 1j * omega * capacitance


def condensed_dynamic_stiffness(
    omega: float,
    modal_mass: float,
    modal_stiffness: float,
    modal_damping: float,
    theta: float,
    load_resistance: float,
    capacitance: float,
) -> complex:
    """Scalar condensed stiffness D_m + i*omega*Theta*Y^-1*Theta^T (Sec. 8).

    D_m = K - omega^2 M + i*omega*C is the uncoupled mechanical dynamic
    stiffness; the second term is the piezoelectric electrical back-action.
    """
    d_m = modal_stiffness - omega**2 * modal_mass + 1j * omega * modal_damping
    y = electrical_admittance(omega, load_resistance, capacitance)
    return d_m + 1j * omega * theta * (1.0 / y) * theta


def displacement_response(
    omega: float,
    force: float,
    modal_mass: float,
    modal_stiffness: float,
    modal_damping: float,
    theta: float,
    load_resistance: float,
    capacitance: float,
) -> complex:
    """u = F / [condensed dynamic stiffness] for a scalar modal coordinate."""
    d_eff = condensed_dynamic_stiffness(
        omega, modal_mass, modal_stiffness, modal_damping, theta, load_resistance, capacitance
    )
    return force / d_eff


def piezo_voltage(omega: float, theta: float, displacement: complex, admittance: complex) -> complex:
    """V = -i*omega*Theta*u / Y, from i*omega*Theta^T u + Y V = 0 (Sec. 8)."""
    return -1j * omega * theta * displacement / admittance


def load_power(voltage: complex, load_resistance: float) -> float:
    """P_load = 0.5 |V|^2 / R_L (Sec. 19/20)."""
    return 0.5 * abs(voltage) ** 2 / load_resistance


def voltage_from_power(power: float, load_resistance: float) -> float:
    """Inverse of load_power for a real resistive load: |V| = sqrt(2 P R_L)."""
    return math.sqrt(2.0 * power * load_resistance)


def impedance_matched_load(omega: float, capacitance: float) -> float:
    """R_L* ~ 1/(omega C_p), the capacitive-reactance load-matching estimate (Sec. 18/19)."""
    return 1.0 / (omega * capacitance)


def angular_frequency_from_hz(f_hz: float) -> float:
    return 2.0 * math.pi * f_hz


def resonant_frequency_hz(effective_stiffness: float, effective_mass: float) -> float:
    """f_r = (1/2pi) sqrt(k_eff / m_eff) (Sec. 18)."""
    return (1.0 / (2.0 * math.pi)) * math.sqrt(effective_stiffness / effective_mass)


def quality_factor(resonant_freq_hz: float, half_power_bandwidth_hz: float) -> float:
    """Q = f_r / BW, the effective quality factor implied by the half-power bandwidth (Sec. 17)."""
    return resonant_freq_hz / half_power_bandwidth_hz


def fractional_bandwidth(resonant_freq_hz: float, half_power_bandwidth_hz: float) -> float:
    """BW / f_r (Sec. 17): the usable window a manufacturing detuning must stay inside."""
    return half_power_bandwidth_hz / resonant_freq_hz


def robustness_ratio(worst_case_power: float, nominal_power: float) -> float:
    """R_robust = P_worst / P_nominal across manufacturing corners (Sec. 16)."""
    return worst_case_power / nominal_power


def scaled_power(nominal_power: float, acceleration_ratio: float) -> float:
    """Linear-response power scaling P ~ a^2 (Sec. 21). Not valid beyond the linear regime."""
    return nominal_power * acceleration_ratio**2


def scaled_voltage(nominal_voltage: float, acceleration_ratio: float) -> float:
    """Linear-response voltage/displacement scaling V ~ a (Sec. 21)."""
    return nominal_voltage * acceleration_ratio


def coupling_theta_from_physical_closure(
    kappa_eff_squared: float, effective_stiffness: float, capacitance: float
) -> float:
    """Theta = sqrt(kappa_eff^2 * K_eff * C_p) (Sec. 14 physical closure)."""
    return math.sqrt(kappa_eff_squared * effective_stiffness * capacitance)


def effective_stiffness_from_theta(theta: float, kappa_eff_squared: float, capacitance: float) -> float:
    """K_eff implied by Theta, kappa_eff^2 and C_p -- inverse of the closure relation above."""
    return theta**2 / (kappa_eff_squared * capacitance)
