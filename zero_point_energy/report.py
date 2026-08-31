"""Self-check: hard-code and verify the source document's own worked numbers.

Run with:

    python3 -m zero_point_energy.report

Every assertion below ties a function in this package to a specific D-item
or worked example in the source document, so a regression here means the
transcription drifted from the audited reference, not that the physics
changed.
"""
from __future__ import annotations

import math

from . import casimir, modes, resonators, stress_tensor, thermal, units
from .constants import C_LIGHT, E_CHARGE, G_NEWTON, HBAR


def _check(label: str, got: float, want: float, rtol: float) -> None:
    ok = math.isclose(got, want, rel_tol=rtol)
    status = "OK " if ok else "FAIL"
    print(f"[{status}] {label}: got {got!r}, want {want!r} (rtol={rtol})")
    assert ok, f"{label}: {got} != {want} within rtol={rtol}"


def main() -> None:
    print("Zero-Point Energy -- self-check against Revision 5 worked numbers")
    print("=" * 72)

    # D16/C1: Casimir pressure at a = 100 nm, corrected in Revision 5.
    _check(
        "Casimir pressure P(100 nm)",
        casimir.plate_pressure(100e-9),
        -13.0013,
        rtol=1e-5,
    )

    # D13/S6: 1 GeV^4 -> J/m^3.
    _check(
        "1 GeV^4 in J/m^3",
        units.GEV4_TO_JOULE_PER_M3,
        2.085215688e37,
        rtol=1e-8,
    )

    # D32: Proca (g=3) is exactly 3x the scalar (g=1) massive cutoff density.
    k_c, mass = 5.0e17, 9.1093837015e-31 * 1000.0
    scalar_rho = modes.zpe_density_massive_exact(k_c, mass, g=1.0)
    proca_rho = modes.proca_zpe_density_exact(k_c, mass)
    _check("Proca / scalar ratio (D32)", proca_rho / scalar_rho, 3.0, rtol=1e-12)

    # D3/D4: the large-k_c asymptotic expansion must match the exact
    # closed-form integral once k_c >> a_m = mc/hbar.
    electron_mass = 9.1093837015e-31
    a_m = electron_mass * C_LIGHT / HBAR
    k_c_large = 1.0e6 * a_m
    exact = modes.zpe_density_massive_exact(k_c_large, electron_mass)
    asymptotic = modes.zpe_density_massive_asymptotic(k_c_large, electron_mass)
    _check("Massive-field exact vs. asymptotic (D3/D4)", asymptotic, exact, rtol=1e-9)

    # D59: LC zero-point identities V=Q/C=omega0*Phi, I=Phi/L=omega0*Q.
    omega0 = 2 * math.pi * 5.0e9
    capacitance = 1.0e-12
    inductance = 1.0 / (capacitance * omega0**2)
    v_zpf, i_zpf, phi_zpf, q_zpf = resonators.lc_zero_point(omega0, capacitance, inductance)
    _check("V_zpf == Q_zpf/C (D59)", v_zpf, q_zpf / capacitance, rtol=1e-12)
    _check("V_zpf == omega0*Phi_zpf (D59)", v_zpf, omega0 * phi_zpf, rtol=1e-12)
    _check("I_zpf == Phi_zpf/L (D59)", i_zpf, phi_zpf / inductance, rtol=1e-12)
    _check("I_zpf == omega0*Q_zpf (D59)", i_zpf, omega0 * q_zpf, rtol=1e-12)

    # D40: Boyer sphere energy, the two displayed forms must agree.
    radius = 1.0
    _check(
        "Boyer sphere energy, two forms (D40)",
        casimir.boyer_sphere_energy(radius),
        0.046175 * HBAR * C_LIGHT / radius,
        rtol=1e-12,
    )

    # D25/D26: ring (length L) is exactly 4x the interval (length L)
    # magnitude, since pi/6 vs pi/24.
    length = 2.5
    ring = casimir.scalar_ring_energy(length)
    interval = casimir.scalar_interval_energy(length)
    _check("Ring/interval ratio (D25 vs D26)", ring / interval, 4.0, rtol=1e-12)

    # D29: T_zz of the plate stress tensor must equal the plate pressure.
    gap = 250e-9
    t00, txx, tyy, tzz = casimir.stress_tensor_diagonal(gap)
    _check("Stress tensor T_zz == P (D29)", tzz, casimir.plate_pressure(gap), rtol=1e-12)

    # D6/D10: vacuum equation of state p = -rho, independent of rho's value.
    rho_vac = 4.2e30
    _check("Vacuum EOS p = -rho (D6/D10)", stress_tensor.vacuum_pressure(rho_vac), -rho_vac, rtol=1e-12)

    # D71/D72: real-world sanity check against the well-known solar-mass
    # Hawking temperature (~6e-8 K) and evaporation time (~1e67 years).
    solar_mass = 1.98847e30
    t_h = thermal.hawking_temperature(solar_mass)
    _check("Hawking T(1 Msun) order of magnitude", t_h, 6.17e-8, rtol=1e-2)
    years = thermal.evaporation_time_benchmark(solar_mass) / 3.15576e7
    _check("Evaporation time(1 Msun) [yr] order of magnitude", years, 2.1e67, rtol=1e-2)

    # D75: Schwinger critical field for the electron (well-known ~1.32e18 V/m).
    e_s = thermal.schwinger_critical_field(electron_mass, E_CHARGE)
    _check("Schwinger critical field, electron", e_s, 1.323e18, rtol=1e-3)

    print("=" * 72)
    print("All checks passed.")


if __name__ == "__main__":
    main()
