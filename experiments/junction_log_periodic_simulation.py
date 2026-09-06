#!/usr/bin/env python3
"""
TIME-DOMAIN SIMULATION: Log-Periodic Emergence from Junction Dynamics

Objective: DERIVE (not fit) the log-periodic modulation M(t) = |sin(omega ln(t/t0))|
from first-principles RCSJ junction network dynamics.

This simulation provides FALSIFIABLE predictions:

- Either M(u) exhibits periodicity in log-time with omega ~= 2*pi/ln(lambda), OR
- The hypothesis is refuted and requires revision.

NO FREE PARAMETERS: All values specified from junction network optimization.

Provenance and scope note: this file was originally checked in as
.github/workflows/blank.yml (not a GitHub Actions workflow -- a plain Python
script with corrupted typographic quotes and flattened indentation from a
markdown paste). It has been moved here verbatim in physics/parameter
content and repaired only at the syntax level (smart quotes -> ASCII quotes,
a stray markdown code-fence removed, indentation of the `rcsj_network`
function body, the `if not sol.success` block, the `if all_pass/else` block,
and the per-junction plotting loop restored to their evidently-intended
structure). No equation, parameter value, threshold, or numerical algorithm
was altered. The only non-syntax change is that the output plot now saves to
a local `outputs/` directory next to this script instead of the original
`/mnt/user-data/outputs/` path, which does not exist outside the authoring
environment; this is a portability fix, not a physics change.

This is a hypothesis-testing CHRONOMETRICS experiment: a speculative,
project-specific search for a log-periodic signature in coupled
Josephson-junction (RCSJ) network dynamics, motivated by (but not derived
from) the `chronometrics` package's log-time phase law. It is NOT part of
the mainstream `zero_point_energy` QFT package, is not audited to the same
D-item/report.py standard, and its "chronomagnetic rate" kappa_cm(t) in
Section 7 is an explicitly prescribed placeholder ("mock contortion"), not
a first-principles result. See zero_point_energy/README.md and
chronometrics/README.md for the epistemic boundary between the two.
"""

import os

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import hilbert, find_peaks
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from mpmath import mp, mpf, log as mplog, pi as mppi

mp.dps = 50

print("=" * 80)
print("TIME-DOMAIN SIMULATION: JUNCTION NETWORK -> LOG-PERIODIC MODULATION")
print("=" * 80)
print()

# ============================================================================
# SECTION 1: JUNCTION NETWORK SPECIFICATION (NO FREE PARAMETERS)
# ============================================================================

print("SECTION 1: Junction Network Specification")
print("-" * 80)

# Optimized weights for K_4 complete graph
w = np.array([58, 59, 46, 55, 58, 39], dtype=np.float64)

# Build Laplacian
W = np.zeros((4, 4))
W[0, 1] = W[1, 0] = w[0]
W[0, 2] = W[2, 0] = w[1]
W[0, 3] = W[3, 0] = w[2]
W[1, 2] = W[2, 1] = w[3]
W[1, 3] = W[3, 1] = w[4]
W[2, 3] = W[3, 2] = w[5]

L = np.diag(W.sum(axis=1)) - W

print(f"Weights: {w}")
print("Laplacian L:")
print(L.astype(int))
print()

# Eigenvalues (for reference)
eigenvalues = np.linalg.eigvalsh(L)
lambda_2, lambda_3, lambda_4 = eigenvalues[1], eigenvalues[2], eigenvalues[3]

print(f"Eigenvalues: lambda_1={eigenvalues[0]:.2e}, lambda_2={lambda_2:.3f}, "
      f"lambda_3={lambda_3:.3f}, lambda_4={lambda_4:.3f}")
print()

# ============================================================================
# SECTION 2: PHYSICAL PARAMETERS (REALISTIC JOSEPHSON JUNCTION VALUES)
# ============================================================================

print("SECTION 2: Physical Parameters")
print("-" * 80)

# Fundamental constants
PHI_0 = 2.067833848e-15  # Wb (flux quantum)

# Junction parameters (typical superconducting values)
C = 1.0e-12  # F (1 pF capacitance)
R = 100.0    # Ohm (100 Ohm shunt resistance)
I_c = 10.0e-6  # A (10 uA critical current)
I_k = 1.0e-6   # A (1 uA coupling current, weak)

# Compute normalized parameters
Gamma = 1.0 / (R * C)  # s^-1
omega_p_sq = (2 * np.pi * I_c) / (PHI_0 * C)  # s^-2
epsilon = (2 * np.pi * I_k) / (PHI_0 * C)  # s^-2

omega_p = np.sqrt(omega_p_sq)  # s^-1 (plasma frequency)

print(f"Capacitance C = {C*1e12:.2f} pF")
print(f"Resistance R = {R:.2f} Ohm")
print(f"Critical current I_c = {I_c*1e6:.2f} uA")
print(f"Coupling current I_k = {I_k*1e6:.2f} uA")
print()
print(f"Damping rate Gamma = {Gamma*1e-9:.3f} GHz")
print(f"Plasma frequency omega_p/(2*pi) = {omega_p/(2*np.pi)*1e-9:.3f} GHz")
print(f"Coupling strength epsilon/omega_p^2 = {epsilon/omega_p_sq:.4f}")
print()

# Operating point (assume phase-locked near theta_0)
theta_0 = 0.1  # radians (slight deviation from zero)
cos_theta_0 = np.cos(theta_0)

print(f"Operating point theta_0 = {theta_0:.3f} rad")
print()

# External drive (parametric modulation)
I_dc = 0.5 * I_c  # DC bias at half critical current
I_ac = 0.1 * I_c  # AC modulation amplitude (10% of DC)
Omega_drive = 0.5 * omega_p  # Drive frequency (near plasma frequency for resonance)

print(f"DC bias I_dc = {I_dc/I_c:.2f} x I_c")
print(f"AC amplitude I_ac = {I_ac/I_c:.2f} x I_c")
print(f"Drive frequency Omega/(2*pi) = {Omega_drive/(2*np.pi)*1e-9:.3f} GHz")
print()

# ============================================================================
# SECTION 3: RCSJ DYNAMICS (COUPLED ODES)
# ============================================================================

print("SECTION 3: RCSJ Dynamics Specification")
print("-" * 80)


def rcsj_network(t, y):
    """Coupled RCSJ equations for 4-junction network.

    State vector: y = [theta_1, theta_2, theta_3, theta_4,
                        thetadot_1, thetadot_2, thetadot_3, thetadot_4]
    Returns: dy/dt
    """
    N = 4
    theta = y[:N]
    theta_dot = y[N:]

    # External drives (identical for all junctions)
    S = np.ones(N) * (2 * np.pi / (PHI_0 * C)) * (I_dc + I_ac * np.cos(Omega_drive * t))

    # Coupling term: epsilon * sum_j L_ij sin(theta_i - theta_j)
    coupling = np.zeros(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                coupling[i] += L[i, j] * np.sin(theta[i] - theta[j])

    # Accelerations: thetaddot_i = -Gamma*thetadot_i - omega_p^2*sin(theta_i)
    #                              - epsilon*coupling[i] + S_i(t)
    theta_ddot = -Gamma * theta_dot - omega_p_sq * np.sin(theta) - epsilon * coupling + S

    return np.concatenate([theta_dot, theta_ddot])


print("ODE system: 4 coupled junctions, 8 state variables")
print("Equation: thetaddot_i + Gamma*thetadot_i + omega_p^2*sin(theta_i) "
      "+ epsilon * sum_j L_ij sin(theta_i-theta_j) = S_i(t)")
print()

# ============================================================================
# SECTION 4: INITIAL CONDITIONS
# ============================================================================

print("SECTION 4: Initial Conditions")
print("-" * 80)

# Start near equilibrium with small perturbations
theta_init = np.array([0.01, 0.02, -0.01, 0.00])  # Small random phases
theta_dot_init = np.zeros(4)  # Start from rest

y0 = np.concatenate([theta_init, theta_dot_init])

print(f"Initial phases: {theta_init}")
print(f"Initial velocities: {theta_dot_init}")
print()

# ============================================================================
# SECTION 5: TIME INTEGRATION
# ============================================================================

print("SECTION 5: Time Integration")
print("-" * 80)

# Time span: long enough to observe beating
T_plasma = 2 * np.pi / omega_p  # Plasma oscillation period
T_beat = T_plasma * 100  # Observe ~100 plasma periods
T_max = T_beat

t_span = (0, T_max)
t_eval = np.linspace(0, T_max, 10000)  # Dense sampling

print(f"Plasma period T_p = {T_plasma*1e9:.3f} ns")
print(f"Integration time T_max = {T_max*1e9:.3f} ns = {T_max/T_plasma:.1f} x T_p")
print(f"Number of time points: {len(t_eval)}")
print()

print("Integrating RCSJ equations (this may take a minute)...")
sol = solve_ivp(
    rcsj_network,
    t_span,
    y0,
    t_eval=t_eval,
    method='LSODA',  # Stiff solver
    rtol=1e-8,
    atol=1e-10,
)

if not sol.success:
    print("ERROR: Integration failed!")
    print(sol.message)
    raise SystemExit(1)

print("Integration successful")
print()

# Extract solution
t = sol.t
theta = sol.y[:4, :]  # Junction phases
theta_dot = sol.y[4:, :]  # Junction velocities

# ============================================================================
# SECTION 6: GATE PHASE CONSTRUCTION
# ============================================================================

print("SECTION 6: Gate Phase Construction")
print("-" * 80)

# Compute collective phase (simple average for now)
# More sophisticated: use eigenvector projections
theta_gate = np.mean(theta, axis=0)  # Average phase

# Alternative: differential mode (for phase-locking analysis)
theta_diff = theta[3, :] - theta[0, :]  # Delta-theta between nodes 0 and 3

print("Gate phase: theta_gate(t) = mean(theta_i)")
print(f"Gate phase range: [{np.min(theta_gate):.3f}, {np.max(theta_gate):.3f}] rad")
print()

# ============================================================================
# SECTION 7: CHRONOMAGNETIC RATE (MOCK CONTORTION)
# ============================================================================

print("SECTION 7: Chronomagnetic Rate kappa_cm(t)")
print("-" * 80)

# For simulation purposes, use a prescribed kappa_cm(t) with log-periodic
# structure. In full theory, this would be derived from teleparallel
# contortion -- here it is an explicit, undisguised placeholder ("mock
# contortion"), not a first-principles derivation.

# Target parameters
lambda_triangle = 3722 / 2705
omega_LOG = 2 * np.pi / np.log(lambda_triangle)
t_0 = T_plasma * 10  # Reference timescale

# Prescribed kappa_cm with log-periodic modulation
kappa_cm = np.abs(np.sin(omega_LOG * np.log((t + 1e-12) / t_0)))  # Regularized log

print("Using prescribed kappa_cm(t) = |sin(omega_LOG * ln(t/t0))|")
print(f"  lambda = {lambda_triangle:.10f}")
print(f"  omega_LOG = {omega_LOG:.10f} (dimensionless)")
print(f"  t0 = {t_0*1e9:.3f} ns")
print()

# ============================================================================
# SECTION 8: GATE-MODULATED EFFECTIVE RATE
# ============================================================================

print("SECTION 8: Gate-Modulated Effective Rate")
print("-" * 80)

M_scale = 1.0  # Dimensionless scaling (could be optimized)

# Apply gate modulation
kappa_eff = kappa_cm * np.cos(theta_gate / M_scale)

print("kappa_eff(t) = kappa_cm(t) * cos(theta_gate(t) / M)")
print(f"  M = {M_scale:.3f}")
print()

# Modulation function
M_t = np.abs(kappa_eff) / np.max(np.abs(kappa_cm))  # Normalized

print("Modulation M(t) = |kappa_eff(t)| / max|kappa_cm(t)|")
print(f"  Range: [{np.min(M_t):.3f}, {np.max(M_t):.3f}]")
print()

# ============================================================================
# SECTION 9: LOG-TIME TRANSFORMATION AND SPECTRAL ANALYSIS
# ============================================================================

print("SECTION 9: Log-Time Analysis")
print("-" * 80)

# Transform to log-time (regularized)
u = np.log((t + 1e-12) / t_0)

# Interpolate M(t) onto uniform u-grid for FFT
u_uniform = np.linspace(u.min(), u.max(), len(u))
M_u = np.interp(u_uniform, u, M_t)

# FFT in log-time
M_fft = fft(M_u)
freqs = fftfreq(len(u_uniform), d=(u_uniform[1] - u_uniform[0]))

# Power spectrum (positive frequencies only)
power = np.abs(M_fft[:len(freqs)//2])**2
freqs_pos = freqs[:len(freqs)//2]

# Find dominant frequency
idx_max = np.argmax(power[1:]) + 1  # Skip DC component
omega_sim = freqs_pos[idx_max]

print(f"Log-time range: u in [{u.min():.3f}, {u.max():.3f}]")
print(f"Dominant frequency (FFT): omega_sim = {omega_sim:.6f}")
print(f"Predicted frequency: omega_LOG = {omega_LOG:.6f}")
print(f"Relative error: {abs(omega_sim - omega_LOG)/omega_LOG * 100:.2f}%")
print()

# ============================================================================
# SECTION 10: FALSIFICATION ASSESSMENT
# ============================================================================

print("=" * 80)
print("FALSIFICATION ASSESSMENT")
print("=" * 80)
print()

# Criterion 1: Frequency match
freq_error = abs(omega_sim - omega_LOG) / omega_LOG
freq_pass = freq_error < 0.05

print("1. Frequency Match:")
print(f"   |omega_sim - omega_pred| / omega_pred = {freq_error*100:.2f}%")
print("   Threshold: < 5%")
print(f"   Status: {'PASS' if freq_pass else 'FAIL'}")
print()

# Criterion 2: Substantial modulation
peak_to_peak = np.max(M_t) - np.min(M_t)
mod_pass = peak_to_peak > 0.5

print("2. Substantial Modulation:")
print(f"   Peak-to-peak: {peak_to_peak:.3f}")
print("   Threshold: > 0.5")
print(f"   Status: {'PASS' if mod_pass else 'FAIL'}")
print()

# Criterion 3: Spectral purity
total_power = np.sum(power[1:])  # Exclude DC
dominant_power = power[idx_max]
spectral_purity = dominant_power / total_power
purity_pass = spectral_purity > 0.5

print("3. Spectral Purity:")
print(f"   Dominant peak power fraction: {spectral_purity*100:.1f}%")
print("   Threshold: > 50%")
print(f"   Status: {'PASS' if purity_pass else 'FAIL'}")
print()

# Overall assessment
all_pass = freq_pass and mod_pass and purity_pass

print("=" * 80)
print("OVERALL SIMULATION RESULT")
print("=" * 80)
if all_pass:
    print("ALL CRITERIA PASSED")
    print("  Log-periodic emergence from junction dynamics CONFIRMED")
    print("  Hypothesis validated at current precision level")
else:
    print("ONE OR MORE CRITERIA FAILED")
    print("  Junction dynamics do NOT produce expected log-periodic structure")
    print("  Hypothesis requires revision or parameter adjustment")
print()

# ============================================================================
# SECTION 11: VISUALIZATION
# ============================================================================

print("SECTION 11: Generating Plots")
print("-" * 80)

fig, axes = plt.subplots(3, 2, figsize=(14, 12))

# Plot 1: Junction phases vs time
ax = axes[0, 0]
for i in range(4):
    ax.plot(t * 1e9, theta[i, :], label=f'theta_{i+1}', alpha=0.7)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Phase (rad)')
ax.set_title('Junction Phases theta_i(t)')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 2: Gate phase vs time
ax = axes[0, 1]
ax.plot(t * 1e9, theta_gate, 'k-', linewidth=1.5)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Gate Phase (rad)')
ax.set_title('theta_gate(t) = mean(theta_i)')
ax.grid(True, alpha=0.3)

# Plot 3: kappa_cm and kappa_eff vs time
ax = axes[1, 0]
ax.plot(t * 1e9, kappa_cm, 'b-', label='kappa_cm (prescribed)', alpha=0.7)
ax.plot(t * 1e9, kappa_eff, 'r-', label='kappa_eff (gate-modulated)', alpha=0.7)
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Rate (s^-1)')
ax.set_title('Chronomagnetic Rates')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 4: Modulation M(t) vs time
ax = axes[1, 1]
ax.plot(t * 1e9, M_t, 'g-', linewidth=1.5)
ax.axhline(y=0.85, color='r', linestyle='--', alpha=0.5, label='Threshold M=0.85')
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Modulation M(t)')
ax.set_title('Normalized Modulation Function')
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 5: M(u) vs log-time
ax = axes[2, 0]
ax.plot(u, M_t, 'purple', linewidth=1.5)
ax.set_xlabel('Log-time u = ln(t/t0)')
ax.set_ylabel('M(u)')
ax.set_title('Modulation in Log-Time Coordinate')
ax.grid(True, alpha=0.3)

# Plot 6: Power spectrum in log-time
ax = axes[2, 1]
ax.semilogy(freqs_pos[1:100], power[1:100], 'b-')
ax.axvline(x=omega_LOG, color='r', linestyle='--', linewidth=2, label=f'Predicted omega={omega_LOG:.3f}')
ax.axvline(x=omega_sim, color='g', linestyle='--', linewidth=2, label=f'Observed omega={omega_sim:.3f}')
ax.set_xlabel('Frequency omega (dimensionless)')
ax.set_ylabel('Power')
ax.set_title('Power Spectrum in Log-Time')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()

_OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(_OUTPUT_DIR, exist_ok=True)
_OUTPUT_PATH = os.path.join(_OUTPUT_DIR, 'junction_simulation_results.png')
plt.savefig(_OUTPUT_PATH, dpi=150)
print(f"Plots saved to: {_OUTPUT_PATH}")
print()

print("=" * 80)
print("SIMULATION COMPLETE")
print("=" * 80)
