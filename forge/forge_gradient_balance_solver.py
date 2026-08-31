import math, time

start = time.time()

names = [
    "Thermal", "Electromagnetic", "PlasmaDensity", "Pressure",
    "MagneticTopology", "ChargeDensity", "PhaseCoherence", "FrequencySpectral",
    "MaterialComposition", "EntropyDissipation", "MechanicalStress",
    "RadiationDiagnostic", "Cryogenic", "AlphaIonization", "BetaElectronBeam",
    "NeutronTransmutation", "GammaDefect", "SynchrotronXray", "VacuumAtmosphere",
    "CentrifugalSeparation", "MagneticResonance", "OpticalPhotonic",
    "AcousticPhononic", "NeutronOpticalMatterWave", "HeavyIonCosmicRayAnalog",
]

axes = [
    "radial_force_residual", "power_residual", "entropy_margin",
    "charge_residual", "phase_residual", "material_residual", "diagnostic_coverage",
]

baseline = [1.20, 1.00, -0.55, 0.80, 0.65, 0.70, -0.30]

A = [
    [-0.15, -0.10,  0.25,  0.00,  0.00, -0.05,  0.02],
    [-0.35, -0.20,  0.18, -0.30, -0.05,  0.00,  0.06],
    [-0.25, -0.10,  0.22, -0.20,  0.00, -0.05,  0.05],
    [-0.45, -0.05,  0.10,  0.00,  0.00,  0.00,  0.02],
    [-0.20, -0.08,  0.08,  0.00, -0.20,  0.00,  0.05],
    [-0.10, -0.05,  0.08, -0.55,  0.00,  0.00,  0.04],
    [ 0.00, -0.05,  0.04,  0.00, -0.45,  0.00,  0.05],
    [ 0.00, -0.12,  0.08,  0.00, -0.35,  0.00,  0.05],
    [-0.05, -0.05,  0.10,  0.00,  0.00, -0.55,  0.05],
    [ 0.00, -0.25,  0.55,  0.00,  0.00,  0.00,  0.10],
    [-0.50, -0.05,  0.12,  0.00,  0.00, -0.10,  0.03],
    [ 0.00, -0.05,  0.05,  0.00,  0.00,  0.00,  0.70],
    [-0.05, -0.30,  0.45,  0.00,  0.00,  0.00,  0.10],
    [ 0.02, -0.08,  0.15,  0.05,  0.00, -0.20,  0.20],
    [ 0.00, -0.10,  0.18, -0.10,  0.00, -0.18,  0.15],
    [ 0.00, -0.10,  0.22,  0.00,  0.00, -0.25,  0.25],
    [ 0.00, -0.10,  0.18,  0.00,  0.00, -0.12,  0.25],
    [ 0.00, -0.15,  0.15,  0.00, -0.05, -0.15,  0.35],
    [-0.10, -0.05,  0.12, -0.05,  0.00, -0.10,  0.15],
    [-0.40, -0.10,  0.08,  0.00,  0.00, -0.05,  0.03],
    [ 0.00, -0.08,  0.08,  0.00, -0.30,  0.00,  0.25],
    [ 0.00, -0.15,  0.12,  0.00, -0.25, -0.05,  0.20],
    [-0.25, -0.12,  0.12,  0.00, -0.15, -0.10,  0.10],
    [ 0.00, -0.06,  0.08,  0.00, -0.15,  0.00,  0.20],
    [-0.03, -0.12,  0.20,  0.05,  0.00, -0.25,  0.20],
]


def state(x):
    y = baseline[:]
    for xi, row in zip(x, A):
        for j in range(len(y)):
            y[j] += xi * row[j]
    return y


def score(x):
    y = state(x)
    return (
        y[0] ** 2
        + y[1] ** 2
        + max(0, -y[2]) ** 2
        + y[3] ** 2
        + y[4] ** 2
        + y[5] ** 2
        + max(0, 1 - y[6]) ** 2
        + 0.0005 * sum(v * v for v in x)
    )


# Coordinate descent optimiser
x = [0.2] * len(names)
best = score(x)
step = 0.5

while step > 1e-5:
    improved = True
    while improved:
        improved = False
        for i in range(len(x)):
            for d in (-step, step):
                z = x[:]
                z[i] = min(1.0, max(0.0, z[i] + d))
                sc = score(z)
                if sc < best - 1e-15:
                    x = z
                    best = sc
                    improved = True
    step *= 0.5

y = state(x)

pass_force    = abs(y[0]) < 0.005
pass_power    = abs(y[1]) < 0.005
pass_entropy  = y[2] >= 0.0
pass_charge   = abs(y[3]) < 0.005
pass_phase    = abs(y[4]) < 0.005
pass_material = abs(y[5]) < 0.005
pass_diag     = y[6] >= 0.995

print("FORGE_GRADIENT_BALANCE_SOLVER")
print("source = pasted Replit transcript, local Termius file only, no app interface")
print("mode = non_operational_normalized_balance_audit")
print("gradient_count =", len(names))
print("closure_axes =", axes)
print("objective_score =", repr(best))
print("BALANCE_VECTOR name value pass_rule")

rules = [
    "abs(x)<0.005", "abs(x)<0.005", "x>=0",
    "abs(x)<0.005", "abs(x)<0.005", "abs(x)<0.005", "x>=0.995",
]
print("\n".join(axes[i] + " " + repr(y[i]) + " " + rules[i] for i in range(len(axes))))

print("ACTIVATION_VECTOR gradient normalized_activation")
print("\n".join(names[i] + " " + repr(x[i]) for i in range(len(names))))

print("PASS_force_closure =",    pass_force)
print("PASS_power_closure =",    pass_power)
print("PASS_entropy_nonnegative =", pass_entropy)
print("PASS_charge_closure =",   pass_charge)
print("PASS_phase_lock =",       pass_phase)
print("PASS_material_closure =", pass_material)
print("PASS_diagnostic_coverage =", pass_diag)
print(
    "FINAL_PASS_FORGE_GRADIENT_BALANCE =",
    pass_force and pass_power and pass_entropy
    and pass_charge and pass_phase and pass_material and pass_diag,
)
print(
    "INTERPRETATION_BOUNDARY = normalized ledger only; "
    "replace coefficients with measured calibration data before any physical claim"
)
print("elapsed_seconds =", repr(time.time() - start))
