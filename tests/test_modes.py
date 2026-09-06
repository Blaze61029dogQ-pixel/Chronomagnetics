"""Tests for zero_point_energy.modes: mode counting and hard-cutoff ZPE
density, independent of the module's own internal formulas where practical."""
import math

import pytest

from zero_point_energy import modes
from zero_point_energy.constants import C_LIGHT, HBAR


def test_density_of_states_matches_direct_dispersion_relation():
    """dN/(V domega) = g*omega^2/(2*pi^2*c^3) recomputed from scratch."""
    omega = 3.7e14
    g = 2.0
    expected = g * omega**2 / (2 * math.pi**2 * C_LIGHT**3)
    assert modes.density_of_states(omega, g) == pytest.approx(expected, rel=1e-14)


def test_spectral_energy_density_is_half_hbar_omega_times_dos():
    """dρ/dω should equal (1/2 ħω) * dN/(V dω), an independent check that
    doesn't reuse modes.spectral_energy_density's own algebraic form."""
    omega = 5.5e14
    g = 3.0
    dos = modes.density_of_states(omega, g)
    expected = 0.5 * HBAR * omega * dos
    assert modes.spectral_energy_density(omega, g) == pytest.approx(expected, rel=1e-13)


def test_zpe_density_is_the_integral_of_spectral_density():
    """rho(omega_c) = int_0^omega_c dρ/dω dω, checked via numerical
    quadrature against the closed-form zpe_density_massless."""
    from scipy.integrate import quad

    omega_c = 2.1e15
    g = 2.0
    numeric, _err = quad(lambda w: modes.spectral_energy_density(w, g), 0.0, omega_c)
    assert modes.zpe_density_massless(omega_c, g) == pytest.approx(numeric, rel=1e-8)


def test_zpe_density_k_and_energy_forms_agree_with_omega_form():
    omega_c = 4.0e14
    g = 2.0
    k_c = omega_c / C_LIGHT
    e_c = HBAR * omega_c
    rho_omega = modes.zpe_density_massless(omega_c, g)
    rho_k = modes.zpe_density_massless_from_k(k_c, g)
    rho_e = modes.zpe_density_massless_from_energy(e_c, g)
    assert rho_k == pytest.approx(rho_omega, rel=1e-13)
    assert rho_e == pytest.approx(rho_omega, rel=1e-13)


def test_photon_density_is_scalar_density_times_two():
    omega_c = 1.0e15
    assert modes.photon_zpe_density(omega_c) == pytest.approx(
        2.0 * modes.zpe_density_massless(omega_c, g=1.0), rel=1e-14
    )


def test_dirac_density_is_negative_with_magnitude_four_times_scalar():
    e_c = 1.0e-9  # Joules
    scalar_form = modes.zpe_density_massless_from_energy(e_c, g=1.0)
    dirac_form = modes.dirac_zpe_density_leading(e_c)
    assert dirac_form < 0.0
    assert dirac_form == pytest.approx(-4.0 * scalar_form, rel=1e-13)


def test_proca_is_exactly_three_times_scalar_at_massive_cutoff():
    k_c = 3.0e17
    mass = 2.0e-30
    scalar = modes.zpe_density_massive_exact(k_c, mass, g=1.0)
    proca = modes.proca_zpe_density_exact(k_c, mass)
    assert proca == pytest.approx(3.0 * scalar, rel=1e-13)


def test_massive_exact_reduces_to_massless_as_mass_to_zero():
    k_c = 1.0e18
    g = 1.0
    massless = modes.zpe_density_massless_from_k(k_c, g)
    nearly_massless = modes.zpe_density_massive_exact(k_c, 1e-40, g)
    assert nearly_massless == pytest.approx(massless, rel=1e-8)


def test_massive_asymptotic_matches_exact_for_large_cutoff_and_diverges_for_small():
    """The asymptotic series should track the exact integral once
    k_c >> a_m = mc/hbar, and visibly depart from it once k_c is comparable
    to a_m (it is not claimed valid there)."""
    mass = 9.1093837015e-31  # electron
    a_m = mass * C_LIGHT / HBAR
    g = 1.0

    k_c_large = 1e5 * a_m
    exact_large = modes.zpe_density_massive_exact(k_c_large, mass, g)
    asymp_large = modes.zpe_density_massive_asymptotic(k_c_large, mass, g)
    rel_err_large = abs(asymp_large - exact_large) / abs(exact_large)

    k_c_small = 2.0 * a_m
    exact_small = modes.zpe_density_massive_exact(k_c_small, mass, g)
    asymp_small = modes.zpe_density_massive_asymptotic(k_c_small, mass, g)
    rel_err_small = abs(asymp_small - exact_small) / abs(exact_small)

    assert rel_err_large < 1e-8
    assert rel_err_small > rel_err_large  # asymptotic degrades away from its regime of validity


def test_density_of_states_dimensional_scaling_with_g():
    """Linear in g by construction; check it actually is, for two different g."""
    omega = 1e15
    assert modes.density_of_states(omega, 4.0) == pytest.approx(4.0 * modes.density_of_states(omega, 1.0))


@pytest.mark.parametrize("omega_c", [1e10, 1e14, 1e18, 1e22])
def test_zpe_density_massless_is_finite_and_negative_for_negative_g(omega_c):
    """Passing a negative g (fermion convention, see module docstring)
    should flip the sign but stay finite."""
    positive = modes.zpe_density_massless(omega_c, g=4.0)
    negative = modes.zpe_density_massless(omega_c, g=-4.0)
    assert math.isfinite(positive) and math.isfinite(negative)
    assert negative == pytest.approx(-positive)
