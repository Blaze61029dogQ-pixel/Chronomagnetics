"""Print a full accounting of the chronometric registry and self-check it
against the numeric values recorded in the source documents.

Run with:  python3 -m chronometrics.report
"""
from __future__ import annotations

import mpmath as mp

from . import constants as C
from . import spectral as S
from . import bright_ridge as BR
from . import dark_bright as DB

mp.mp.dps = 50


def _check(label: str, computed, reference, tol, hard: bool = True) -> None:
    diff = abs(mp.mpf(computed) - mp.mpf(reference))
    ok = diff <= tol
    tag = "OK  " if ok else ("FAIL" if hard else "WARN")
    print(f"  [{tag}] {label}: computed={computed}  reference={reference}  |diff|={diff}")
    if hard and not ok:
        raise AssertionError(f"{label} did not reproduce the documented value")


def main() -> None:
    print("=" * 78)
    print("CHRONOMAGNETICS -- chronometric registry (new block)")
    print("=" * 78)

    print("\n1. Chronometric triangle seed                                  [EXACT]")
    print(f"   a, b, c = {C.A_SIDE}, {C.B_SIDE}, {C.C_SIDE}    s = {C.SEMIPERIMETER}")
    print(f"   Area^2  = {C.AREA_SQ}  (Heron: 199*55*61*83)")
    print(f"   13309   = (a^2+b^2+c^2)/4 = {C.THIRTEEN_309}")
    A, B, Cv = C.triangle_vertices()
    ab = mp.sqrt((Cv[0] - A[0]) ** 2 + (Cv[1] - A[1]) ** 2)
    cb = mp.sqrt((Cv[0] - B[0]) ** 2 + (Cv[1] - B[1]) ** 2)
    _check("|CA| == b", ab, C.B_SIDE, mp.mpf('1e-30'))
    _check("|CB| == a", cb, C.A_SIDE, mp.mpf('1e-30'))

    print("\n2. Brocard phase seed beta_Delta                                [EXACT]")
    _check("beta_Delta", C.BETA_DELTA,
           mp.mpf('0.50997646765152867533025365426394810693770916898566'),
           mp.mpf('1e-40'))

    print("\n3. q-screen constant and exact leakage defect                  [EXACT]")
    _check("q_Delta", C.Q_DELTA,
           mp.mpf('0.99998737687837740309792092424822573588866192362006'),
           mp.mpf('1e-40'))
    print(f"   delta_q_squared = {C.DELTA_Q_SQUARED}  (exact fraction)")
    # spot-check the exact leakage identity at a few thetas (mpf inputs, so
    # the check is limited by mpmath's working precision, not float64)
    for theta_val in (mp.mpf(0), mp.mpf('0.7'), mp.mpf('2.3'), mp.mpf('5.1')):
        lhs = mp.cos(theta_val) ** 2 - C.Z_Delta_of_theta(theta_val) ** 2
        rhs = mp.mpf(C.DELTA_Q_SQUARED.numerator) / C.DELTA_Q_SQUARED.denominator * mp.cos(theta_val) ** 2
        _check(f"leakage identity @ theta={theta_val}", lhs, rhs, mp.mpf('1e-40'))

    print("\n4. Brocard leakage-null branch                        [EXACT, in form]")
    _check("kappa_null(0)", C.kappa_null(0),
           mp.mpf('0.16883472431271515108588145691917103780168415428829'),
           mp.mpf('1e-30'))

    print("\n5. Bright-ridge constant K_QP                        [AUDITED, not exact]")
    _check("K_QP", C.K_QP,
           mp.mpf('0.17351379142181891012657988639923551581629750272859'),
           mp.mpf('1e-30'))
    ridge = BR.locate()
    print(f"   independent local-max search located kappa = {ridge.located_kappa!r}")
    print(f"   canonical K_QP                              = {ridge.canonical_k_qp!r}")
    print(f"   miss                                        = {ridge.miss:.3e}")
    if abs(ridge.miss) > 1e-4:
        print("   [WARN] independent bright-ridge search drifted from canonical K_QP")

    print("\n6. Frozen spectral operator L_chrono on [0,12]        [AUDITED, not exact]")
    result = S.solve(n_interior=6000, n_eigs=16)
    g12_observed = result.gap(12, 11)
    g16_observed = result.gap(16, 15)
    g12_target = float(S.g12_target())
    g16_target = float(S.g16_target())
    print(f"   G_12 target  (101/63)*q_Delta^2 = {g12_target:.12f}")
    print(f"   G_12 observed (finite-diff, N={result.n_interior}) = {g12_observed:.12f}")
    print(f"   G_16 target  6*(lambda_Delta-1) = {g16_target:.12f}  [REJECTED lead]")
    print(f"   G_16 observed (finite-diff, N={result.n_interior}) = {g16_observed:.12f}")
    g12_rel = abs(g12_observed - g12_target) / g12_target
    g16_rel = abs(g16_observed - g16_target) / g16_target
    print(f"   G_12 relative miss = {g12_rel:.3e}  (documented frozen-operator relation)")
    print(f"   G_16 relative miss = {g16_rel:.3e}  (documented as REJECTED -- should NOT be tiny)")

    print("\n7. Iso-gap lock direction                    [FROZEN, transcribed only]")
    print(f"   delta_B_gate / delta_chi ~= {C.ISO_GAP_SLOPE}  (from source audit; "
          f"not independently re-derived here)")

    print("\n8. Dark-to-Bright Chronometric Separation                 -- NEW BLOCK")
    sep = DB.compute()
    _check("Delta_kappa_DB", sep.delta_kappa_db,
           mp.mpf('0.00467906710910375904069842948006447801461334844030'),
           mp.mpf('1e-30'))
    _check("Delta_theta_DB (rad)", sep.delta_theta_db,
           mp.mpf('0.02939944571122800192040571760748416106900675057779'),
           mp.mpf('1e-30'))
    _check("R_DB (shifted-time ratio)", sep.r_db,
           mp.mpf('1.00149448315872695665033747260134572959126865147598'),
           mp.mpf('1e-30'))
    print(f"   kappa_null(0)   = {sep.kappa_null}")
    print(f"   kappa_bright    = {sep.kappa_bright}")
    print(f"   Delta_kappa_DB  = {sep.delta_kappa_db}")
    print(f"   Delta_theta_DB  = {sep.delta_theta_db} rad "
          f"({sep.delta_theta_db * 180 / mp.pi} deg)")
    print(f"   R_DB            = {sep.r_db}")
    interp = "AFTER" if sep.delta_kappa_db > 0 else "BEFORE"
    print(f"   -> bright ridge occurs {interp} the null branch in log-time.")

    print("\n" + "=" * 78)
    print("BOUNDARY STATEMENT")
    print("=" * 78)
    print(
        "These are internal chronometric constants derived from one exact\n"
        "triangle, plus a frozen gate/spectral model layered on top. None of\n"
        "this is a confirmed physical law: no measured voltage, clock, flux,\n"
        "timing, or geophysical channel has been shown to contain this\n"
        "residual. The dark-to-bright separation above is a closed-form\n"
        "consequence of the registry, not a new physical claim."
    )


if __name__ == "__main__":
    main()
