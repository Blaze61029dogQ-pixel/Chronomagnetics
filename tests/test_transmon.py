"""Tests for zero_point_energy.transmon: exact charge-basis diagonalization
and the large-E_J/E_C asymptotic approximation."""
import math

import numpy as np
import pytest

from zero_point_energy.transmon import (
    asymptotic_energies,
    diagonalize,
    energies_vs_truncation,
    hamiltonian_matrix,
)

EC_DEEP = 0.2   # GHz-equivalent units
EJ_DEEP = 20.0  # EJ/EC = 100: deep transmon regime


def test_hamiltonian_is_hermitian_real_symmetric():
    h = hamiltonian_matrix(EC_DEEP, EJ_DEEP, n_g=0.3, n_max=10)
    assert np.allclose(h, h.T)
    assert np.isrealobj(h)


def test_eigenvalues_are_real_and_ascending():
    spec = diagonalize(EC_DEEP, EJ_DEEP, n_g=0.0, n_max=15, num_levels=6)
    assert np.isrealobj(spec.eigenvalues)
    assert all(math.isfinite(e) for e in spec.eigenvalues)
    assert list(spec.eigenvalues) == sorted(spec.eigenvalues)


def test_eigenvectors_are_orthonormal_when_requested():
    spec = diagonalize(EC_DEEP, EJ_DEEP, n_g=0.1, n_max=15, num_levels=4, return_eigenvectors=True)
    gram = spec.eigenvectors.T @ spec.eigenvectors
    assert np.allclose(gram, np.eye(4), atol=1e-10)


# --- charge-basis truncation convergence ------------------------------------

def test_charge_basis_truncation_converges():
    n_max_values = (5, 10, 15, 20, 30)
    energies = energies_vs_truncation(EC_DEEP, EJ_DEEP, n_max_values=n_max_values, num_levels=5)
    reference = energies[-1]  # largest truncation, most converged
    errors = [np.max(np.abs(e - reference)) for e in energies]
    assert errors == sorted(errors, reverse=True)  # monotonically improving
    assert errors[-2] < 1e-8  # n_max=20 vs n_max=30 agree to high precision
    assert errors[0] > 1e-4  # n_max=5 is genuinely under-converged, not a trivial pass


def test_num_levels_cannot_exceed_basis_dimension():
    with pytest.raises(ValueError):
        diagonalize(EC_DEEP, EJ_DEEP, n_max=2, num_levels=10)  # dimension = 5


# --- transmon asymptotic behavior at large E_J/E_C --------------------------

def test_asymptotic_anharmonicity_is_exactly_minus_ec():
    energies = asymptotic_energies(EC_DEEP, EJ_DEEP, num_levels=3)
    transitions = np.diff(energies)
    anharmonicity = transitions[1] - transitions[0]
    assert anharmonicity == pytest.approx(-EC_DEEP, rel=1e-12)


def test_exact_anharmonicity_approaches_asymptotic_as_ratio_grows():
    """The exact anharmonicity converges to the asymptotic -E_C value, but
    slowly: empirically the leading correction scales close to
    E_C/sqrt(E_J/E_C) (observed relative error / (1/sqrt(ratio)) is a
    roughly constant ~0.5-0.8 across two decades of ratio below), i.e. this
    is a leading-order approximation with a genuinely slow, not
    exponential, approach -- the threshold here is set from that observed
    scaling, not an assumption of fast convergence."""
    ec = 0.2
    ratios = (50, 200, 1000, 5000)
    errors = []
    for ratio in ratios:
        ej = ratio * ec
        n_max = max(15, int(8 * math.sqrt(ratio)))
        exact = diagonalize(ec, ej, n_max=n_max, num_levels=3)
        asymptotic_anharm = -ec  # exact formula value, see test above
        errors.append(abs(exact.anharmonicity - asymptotic_anharm))
    assert errors == sorted(errors, reverse=True)
    # relative error should stay within a factor of ~2 of 1/sqrt(ratio) at each point
    for ratio, err in zip(ratios, errors):
        assert (err / ec) < 2.0 / math.sqrt(ratio)
    assert errors[-1] < 0.02 * ec  # ratio=5000: observed relative error ~1.2%


def test_charge_dispersion_is_exponentially_small_in_deep_transmon_regime():
    """A defining transmon feature (Koch et al. 2007): ground-state charge
    dispersion (sensitivity to n_g) is exponentially suppressed as
    E_J/E_C grows."""
    dispersions = []
    for ratio in (5, 20, 100):
        ec = 0.2
        ej = ratio * ec
        n_max = max(15, int(6 * math.sqrt(ratio)))
        e0_at_0 = diagonalize(ec, ej, n_g=0.0, n_max=n_max, num_levels=1).eigenvalues[0]
        e0_at_half = diagonalize(ec, ej, n_g=0.5, n_max=n_max, num_levels=1).eigenvalues[0]
        dispersions.append(abs(e0_at_0 - e0_at_half))
    assert dispersions == sorted(dispersions, reverse=True)
    assert dispersions[-1] < 1e-6 * ec


# --- energy-shift invariance -------------------------------------------------

def test_gate_charge_integer_shift_leaves_spectrum_invariant():
    """H(n_g) and H(n_g+1) are related by relabeling n -> n+1 in the charge
    basis and must have identical spectra (periodicity of the transmon in
    n_g with period 1)."""
    spec_a = diagonalize(EC_DEEP, EJ_DEEP, n_g=0.37, n_max=20, num_levels=5)
    spec_b = diagonalize(EC_DEEP, EJ_DEEP, n_g=1.37, n_max=20, num_levels=5)
    assert spec_a.eigenvalues == pytest.approx(spec_b.eigenvalues, abs=1e-9)


def test_transition_frequencies_and_anharmonicity_are_independent_of_added_constant():
    """Adding a constant offset to E_C, E_J together does not correspond to
    a physical symmetry, but adding a constant directly to the Hamiltonian
    (an overall energy-zero shift) must leave every transition frequency
    and the anharmonicity unchanged."""
    h = hamiltonian_matrix(EC_DEEP, EJ_DEEP, n_g=0.2, n_max=15)
    shift = 123.456
    eigvals = np.linalg.eigvalsh(h)[:5]
    eigvals_shifted = np.linalg.eigvalsh(h + shift * np.eye(h.shape[0]))[:5]
    assert np.diff(eigvals) == pytest.approx(np.diff(eigvals_shifted), abs=1e-10)


# --- dimensional homogeneity ("dimensions") ---------------------------------

def test_spectrum_scales_linearly_with_overall_energy_scale():
    """H is linear in (E_C, E_J) with no other dimensionful parameters, so
    rescaling both by a common factor must rescale every eigenvalue,
    transition frequency, and the anharmonicity by that same factor."""
    scale = 3.7
    base = diagonalize(EC_DEEP, EJ_DEEP, n_g=0.15, n_max=15, num_levels=5)
    scaled = diagonalize(scale * EC_DEEP, scale * EJ_DEEP, n_g=0.15, n_max=15, num_levels=5)
    assert scaled.eigenvalues == pytest.approx(scale * base.eigenvalues, rel=1e-10)
    assert scaled.transition_frequencies == pytest.approx(scale * base.transition_frequencies, rel=1e-10)
    assert scaled.anharmonicity == pytest.approx(scale * base.anharmonicity, rel=1e-10)


# --- input validation ---------------------------------------------------------

@pytest.mark.parametrize("bad_ec", [-1.0, 0.0, float("nan"), float("inf")])
def test_rejects_nonphysical_ec(bad_ec):
    with pytest.raises(ValueError):
        hamiltonian_matrix(bad_ec, EJ_DEEP)


@pytest.mark.parametrize("bad_ej", [-1.0, 0.0, float("nan"), float("inf")])
def test_rejects_nonphysical_ej(bad_ej):
    with pytest.raises(ValueError):
        hamiltonian_matrix(EC_DEEP, bad_ej)


def test_rejects_non_finite_ng():
    with pytest.raises(ValueError):
        hamiltonian_matrix(EC_DEEP, EJ_DEEP, n_g=float("nan"))


def test_rejects_nonpositive_n_max():
    with pytest.raises(ValueError):
        hamiltonian_matrix(EC_DEEP, EJ_DEEP, n_max=0)
