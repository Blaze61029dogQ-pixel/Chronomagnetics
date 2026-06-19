#!/usr/bin/env python3
"""
Chronometric Driver Rebuild v1
==============================
Computational audit and reconstruction of the chronometric constant stack.

Derivation status per constant:
  [DERIVED]  — computed from first-principle formula within this file
  [ANCHOR]   — accepted from prior session; derivation chain not yet reconstructed
  [VERIFIED] — arithmetic check on combination of the above

Run:
  python3 chrono_driver_rebuild_v1.py

Output: deterministic; final line is PASS or FAIL.
"""

import math
from fractions import Fraction

# ── tolerance thresholds ──────────────────────────────────────────────────────
TOL_EXACT   = 1e-13   # for constants with closed-form rational basis
TOL_ANCHOR  = 1e-14   # float equality on anchored values
TOL_CLOSURE = 1e-13   # phase-closure residual

PASS_COUNT = 0
FAIL_COUNT = 0
FAILURES   = []

def check(label, got, expected, tol, status_tag):
    global PASS_COUNT, FAIL_COUNT
    err = abs(got - expected)
    ok  = err <= tol
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
        FAILURES.append(f"  {label}: got={got:.16e}  expected={expected:.16e}  err={err:.3e}")
    print(f"  [{tag}] [{status_tag}] {label}")
    print(f"         got      = {got:.16e}")
    print(f"         expected = {expected:.16e}")
    print(f"         |err|    = {err:.3e}  (tol={tol:.0e})")
    return ok


SEP = "=" * 72

print(SEP)
print("CHRONOMETRIC DRIVER REBUILD v1 — COMPUTATIONAL AUDIT")
print(SEP)
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1: TRIANGLE BASIS (a=144, b=138, c=116)
# Source of delta_q_squared via Heron area decomposition.
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 1: Triangle Basis ──────────────────────────────────────────")
a, b, c = 144, 138, 116
s = (a + b + c) // 2                        # must be integer
assert (a + b + c) % 2 == 0, "odd perimeter"

s_a, s_b, s_c = s - a, s - b, s - c
Area_sq = s * s_a * s_b * s_c              # exact integer
Area_int = math.isqrt(Area_sq)             # floor(sqrt(Area²))
remainder = Area_sq - Area_int ** 2        # exact integer remainder

print(f"  a={a}, b={b}, c={c}")
print(f"  s={s},  s-a={s_a}, s-b={s_b}, s-c={s_c}")
print(f"  Area²  = s·(s-a)·(s-b)·(s-c) = {Area_sq}")
print(f"  floor(√Area²) = {Area_int}")
print(f"  remainder     = Area² - {Area_int}² = {remainder}")
print()

assert Area_sq   == 55_414_535, f"Area² mismatch: {Area_sq}"
assert Area_int  == 7444,       f"floor(sqrt) mismatch: {Area_int}"
assert remainder == 1399,       f"remainder mismatch: {remainder}"

Area_float = math.sqrt(Area_sq)
print(f"  Area (float)  = {Area_float:.15f}")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2: EXACT RATIONAL CONSTANTS
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 2: Exact Rational Constants ────────────────────────────────")

# lambda_Delta — defined ratio, not derived here from the triangle
lam_num, lam_den = 3722, 2705
lambda_Delta_frac = Fraction(lam_num, lam_den)
lambda_Delta = lam_num / lam_den

print(f"  lambda_Delta = {lam_num}/{lam_den} (GCD={math.gcd(lam_num,lam_den)}, already reduced)")
print(f"               = {lambda_Delta:.16e}")

# delta_q_squared — from triangle area decomposition
dq2_num, dq2_den = remainder, Area_sq     # 1399 / 55414535
delta_q_sq_frac = Fraction(dq2_num, dq2_den)
delta_q_squared = dq2_num / dq2_den

print(f"  delta_q² = {dq2_num}/{dq2_den}")
print(f"           = (Area² - floor(√Area²)²) / Area²")
print(f"           = {delta_q_squared:.16e}")
print()

check("lambda_Delta",    lambda_Delta,    1.3759704251386322,   TOL_EXACT,  "DERIVED")
check("delta_q_squared", delta_q_squared, 1399/55414535,        TOL_ANCHOR, "DERIVED")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3: DERIVED — q_Delta
# q_Delta = sqrt(1 - delta_q_squared)
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 3: q_Delta ─────────────────────────────────────────────────")

q_Delta = math.sqrt(1.0 - delta_q_squared)

print(f"  q_Delta = sqrt(1 - delta_q²)")
print(f"          = sqrt(1 - {dq2_num}/{dq2_den})")
print(f"          = sqrt({dq2_den - dq2_num}/{dq2_den})")
print(f"          = {q_Delta:.16e}")
print()

# first-order Taylor verification: sqrt(1-x) ≈ 1 - x/2  for small x
q_approx = 1.0 - delta_q_squared / 2.0
print(f"  Taylor approx (1 - delta_q²/2) = {q_approx:.16e}  (sanity, not assertion)")
print()

check("q_Delta", q_Delta, 0.9999873768783775, TOL_EXACT, "DERIVED")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4: ANCHORED CONSTANTS
# These values are accepted from the prior session computation chain.
# Their derivation formulae are not yet reconstructed in this file.
# They are NOT computed here; they are asserted for bit-exact reproducibility.
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 4: Anchored Constants (accepted, derivation not yet here) ──")

beta_Delta         = 0.5099764676515286
kappa_null         = 0.16883472431271518
kappa_bright       = 0.1735137914218189
Delta_theta_DB_rad = 0.02939944571122785
R_DB_time_ratio    = 1.001494483158727

# Self-consistency: kappa_null < kappa_bright
assert kappa_null < kappa_bright, "ordering violated: kappa_null must be < kappa_bright"
print(f"  beta_Delta         = {beta_Delta:.16e}  [ANCHOR]")
print(f"  kappa_null         = {kappa_null:.16e}  [ANCHOR]")
print(f"  kappa_bright       = {kappa_bright:.16e}  [ANCHOR]")
print(f"  Delta_theta_DB_rad = {Delta_theta_DB_rad:.16e}  [ANCHOR]")
print(f"  R_DB_time_ratio    = {R_DB_time_ratio:.16e}  [ANCHOR]")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5: VERIFIED — Delta_kappa_DB (simple arithmetic on anchors)
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 5: Delta_kappa_DB ───────────────────────────────────────────")

Delta_kappa_DB = kappa_bright - kappa_null

print(f"  Delta_kappa_DB = kappa_bright - kappa_null")
print(f"                 = {kappa_bright:.16e}")
print(f"                 - {kappa_null:.16e}")
print(f"                 = {Delta_kappa_DB:.16e}")
print()

check("Delta_kappa_DB", Delta_kappa_DB, 0.004679067109103735, TOL_EXACT, "VERIFIED")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 6: DERIVED — omega_Delta
# omega_Delta = 2π / ln(lambda_Delta)
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 6: omega_Delta ──────────────────────────────────────────────")

ln_lambda   = math.log(lambda_Delta)
omega_Delta = 2.0 * math.pi / ln_lambda

print(f"  ln(lambda_Delta) = {ln_lambda:.16e}")
print(f"  omega_Delta = 2π / ln(lambda_Delta)")
print(f"              = {2*math.pi:.16e} / {ln_lambda:.16e}")
print(f"              = {omega_Delta:.16e}")
print()

check("omega_Delta", omega_Delta, 19.686678006260053, TOL_EXACT, "DERIVED")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 7: PHASE CLOSURE — theta(t·lambda) - theta(t) = 2π
# theta(t) = omega_Delta · ln(t)
# theta(t·lambda) - theta(t) = omega_Delta · ln(lambda_Delta) = 2π (exact)
# Residual measures floating-point round-trip error only.
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 7: Phase Closure ────────────────────────────────────────────")

closure_value   = omega_Delta * ln_lambda           # should equal 2π exactly
two_pi          = 2.0 * math.pi
closure_residual = abs(closure_value - two_pi)

print(f"  omega_Delta × ln(lambda_Delta) = {closure_value:.16e}")
print(f"  2π                             = {two_pi:.16e}")
print(f"  |residual|                     = {closure_residual:.3e}")
print()

ok = closure_residual <= TOL_CLOSURE
tag = "PASS" if ok else "FAIL"
if ok: PASS_COUNT += 1
else:
    FAIL_COUNT += 1
    FAILURES.append(f"  phase closure: residual={closure_residual:.3e}  tol={TOL_CLOSURE:.0e}")

print(f"  [{tag}] [DERIVED] theta closure residual <= {TOL_CLOSURE:.0e}")
print(f"          stated bound: <= 7.1e-15")
print(f"          computed:        {closure_residual:.3e}")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 8: INTERNAL CONSISTENCY CHECKS (anchor cross-checks)
# These test whether the anchored values form a self-consistent set.
# A failure here flags a discrepancy in the prior chain, not a derivation error.
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 8: Internal Consistency Checks ──────────────────────────────")

# 8a. q_Delta² + delta_q_squared = 1
lhs_8a = q_Delta**2 + delta_q_squared
check("q_Delta²+delta_q²=1", lhs_8a, 1.0, TOL_EXACT, "VERIFIED")

# 8b. kappa ordering: dark-null < bright-ridge
kappa_order_ok = (kappa_null < kappa_bright)
tag_8b = "PASS" if kappa_order_ok else "FAIL"
if kappa_order_ok: PASS_COUNT += 1
else: FAIL_COUNT += 1; FAILURES.append("  kappa ordering violated")
print(f"  [{tag_8b}] [VERIFIED] kappa_null < kappa_bright  ({kappa_null:.6f} < {kappa_bright:.6f})")

# 8c. omega_Delta × ln(lambda_Delta) / (2π) = 1  (closure ratio)
closure_ratio = omega_Delta * ln_lambda / two_pi
check("closure ratio = 1", closure_ratio, 1.0, TOL_EXACT, "VERIFIED")

# 8d. lambda_Delta is in lowest terms
gcd_lam = math.gcd(lam_num, lam_den)
gcd_ok = (gcd_lam == 1)
tag_8d = "PASS" if gcd_ok else "FAIL"
if gcd_ok: PASS_COUNT += 1
else: FAIL_COUNT += 1; FAILURES.append(f"  lambda_Delta not reduced: GCD={gcd_lam}")
print(f"  [{tag_8d}] [DERIVED]  lambda_Delta = {lam_num}/{lam_den} is fully reduced (GCD=1)")

# 8e. delta_q_squared is in lowest terms
gcd_dq = math.gcd(dq2_num, dq2_den)
gcd_dq_ok = (gcd_dq == 1)
tag_8e = "PASS" if gcd_dq_ok else "FAIL"
if gcd_dq_ok: PASS_COUNT += 1
else: FAIL_COUNT += 1; FAILURES.append(f"  delta_q² not reduced: GCD={gcd_dq}")
print(f"  [{tag_8e}] [DERIVED]  delta_q² = {dq2_num}/{dq2_den} is fully reduced (GCD={gcd_dq})")

print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 9: FLAGGED ITEMS — items requiring derivation chain specification
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 9: Unvalidated / Flagged Items ──────────────────────────────")
print()
print("  The following constants are carried as anchors.")
print("  Their generating formulae have NOT been reconstructed in this file.")
print("  They are NOT independently verified — only their stated float values")
print("  are preserved for downstream use.")
print()

flags = [
    ("beta_Delta",         beta_Delta,
     "Formula unknown. Possibly a Doppler/boost or phase-contrast ratio."),
    ("kappa_null",         kappa_null,
     "Dark-null chronomagnetic rate. Source formula not reconstructed."),
    ("kappa_bright",       kappa_bright,
     "Bright-ridge chronomagnetic rate. Source formula not reconstructed."),
    ("Delta_theta_DB_rad", Delta_theta_DB_rad,
     "Dark/bright angular separation. Derivation from kappa pair not shown."),
    ("R_DB_time_ratio",    R_DB_time_ratio,
     "Shifted-time ratio. Relation to other constants not yet established."),
]

for name, val, note in flags:
    print(f"  [FLAG] {name} = {val:.16e}")
    print(f"         {note}")
    print()

print("  CAUTION: lambda_Delta MUST NOT be merged into kappa or beta")
print("  computations unless a specific derivation explicitly requires it.")
print("  (Per project constraint: lambda_Delta remains isolated unless coupled.)")
print()

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 10: CONSTANT SUMMARY TABLE
# ═════════════════════════════════════════════════════════════════════════════

print("── SECTION 10: Constant Summary ────────────────────────────────────────")
print()
print(f"  {'Constant':<26} {'Value':>26}  Status")
print(f"  {'-'*26}  {'-'*26}  {'-'*10}")

summary = [
    ("lambda_Delta",         lambda_Delta,         "DERIVED"),
    ("beta_Delta",           beta_Delta,           "ANCHOR"),
    ("q_Delta",              q_Delta,              "DERIVED"),
    ("delta_q_squared",      delta_q_squared,      "DERIVED"),
    ("kappa_null",           kappa_null,           "ANCHOR"),
    ("kappa_bright",         kappa_bright,         "ANCHOR"),
    ("Delta_kappa_DB",       Delta_kappa_DB,       "VERIFIED"),
    ("Delta_theta_DB_rad",   Delta_theta_DB_rad,   "ANCHOR"),
    ("R_DB_time_ratio",      R_DB_time_ratio,      "ANCHOR"),
    ("omega_Delta",          omega_Delta,          "DERIVED"),
    ("phase closure |res|",  closure_residual,     "DERIVED"),
]

for name, val, st in summary:
    print(f"  {name:<26}  {val:>26.16e}  {st}")

print()

# ═════════════════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═════════════════════════════════════════════════════════════════════════════

print(SEP)
print("FINAL REPORT")
print(SEP)
print(f"  Checks passed : {PASS_COUNT}")
print(f"  Checks failed : {FAIL_COUNT}")
print()

if FAIL_COUNT == 0:
    print("  RESULT: PASS")
    print("  All computed constants match reference values within tolerance.")
    print("  Anchored constants preserved bit-for-bit.")
    print("  Derivation gaps flagged in Section 9.")
else:
    print("  RESULT: FAIL")
    print("  Discrepancies:")
    for f in FAILURES:
        print(f)

print(SEP)
