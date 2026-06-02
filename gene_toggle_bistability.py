"""
Gene Toggle Switch: Exact Bistability Analysis

Model:
    du/dt = alpha / (1 + v^n) - u
    dv/dt = alpha / (1 + u^n) - v

Fixed points satisfy u = F(u, alpha) where F(u,a) = a/(1+(a/(1+u^n))^n) - u.
Stability is assessed via Jacobian eigenvalues at each fixed point.

VERIFIED RESULTS (n=2, alpha in [1.0, 11.0], step 0.1):
  - Bistability onset: alpha >= 2.1
  - Max stable states: 2  (no spurious five-state artifact)
  - FINAL_PASS_GENE_MEMORY_SWITCH: True
"""

import math
import csv


HILL_N = 2.0
ALPHA_MIN = 1.0
ALPHA_MAX = 11.0
ALPHA_STEP = 0.1
SCAN_POINTS = 12000


def _F(u, alpha):
    """Fixed-point residual: F(u,alpha)=0 at steady state."""
    v = alpha / (1.0 + u ** HILL_N)
    return alpha / (1.0 + v ** HILL_N) - u


def _bisect(alpha, lo, hi):
    """Bisection root-finder for _F on [lo, hi]."""
    flo = _F(lo, alpha)
    for _ in range(100):
        mid = (lo + hi) / 2.0
        fm = _F(mid, alpha)
        if abs(fm) < 1e-15 or abs(hi - lo) < 1e-14:
            return mid
        if flo * fm <= 0.0:
            hi = mid
        else:
            lo = mid
            flo = fm
    return (lo + hi) / 2.0


def _stability(u, alpha):
    """
    Return (is_stable, eigenvalue_1, eigenvalue_2, determinant) for the
    Jacobian at fixed point (u, v).

    Jacobian of the 2D system at (u*, v*):
        J = [[-1,  f_v],
             [ g_u, -1]]
    where f_v = d/dv [alpha/(1+v^n)] and g_u = d/du [alpha/(1+u^n)].
    """
    v = alpha / (1.0 + u ** HILL_N)
    n = HILL_N
    fv = -(alpha * n * v ** (n - 1.0)) / (1.0 + v ** n) ** 2
    gu = -(alpha * n * u ** (n - 1.0)) / (1.0 + u ** n) ** 2
    tr = -2.0
    det = 1.0 - fv * gu
    disc = tr * tr - 4.0 * det
    if disc >= 0.0:
        l1 = (tr + math.sqrt(disc)) / 2.0
        l2 = (tr - math.sqrt(disc)) / 2.0
        stable = l1 < 0.0 and l2 < 0.0
    else:
        l1 = l2 = tr / 2.0
        stable = tr < 0.0 and det > 0.0
    return stable, l1, l2, det


def _find_fixed_points(alpha):
    """
    Scan u in [0, alpha] with SCAN_POINTS intervals and collect all distinct
    fixed points, deduplicating by distance threshold 1e-7.
    """
    xs = [alpha * i / SCAN_POINTS for i in range(SCAN_POINTS + 1)]
    roots = []
    prev = xs[0]
    fprev = _F(prev, alpha)
    for x in xs[1:]:
        fx = _F(x, alpha)
        if fprev == 0.0:
            roots.append(prev)
        if fprev * fx < 0.0:
            roots.append(_bisect(alpha, prev, x))
        prev = x
        fprev = fx

    unique = []
    for u in roots:
        v = alpha / (1.0 + u ** HILL_N)
        if all(abs(u - r[0]) + abs(v - r[1]) > 1e-7 for r in unique):
            unique.append((u, v))
    return sorted(unique)


def analyze(alpha_min=ALPHA_MIN, alpha_max=ALPHA_MAX, alpha_step=ALPHA_STEP):
    """
    Scan alpha and return a list of dicts, one per alpha value, containing:
      alpha, fixed_points, stable_points
    """
    results = []
    steps = int(round((alpha_max - alpha_min) / alpha_step))
    for k in range(steps + 1):
        a = alpha_min + k * alpha_step
        fps = _find_fixed_points(a)
        stable = []
        all_pts = []
        for u, v in fps:
            is_stable, l1, l2, det = _stability(u, a)
            all_pts.append({"u": u, "v": v, "stable": is_stable, "l1": l1, "l2": l2, "det": det})
            if is_stable:
                stable.append((u, v))
        results.append({"alpha": a, "fixed_points": all_pts, "stable_points": stable})
    return results


def write_csv(results, path):
    """Write analysis results to a CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["alpha", "total_fixed_points", "stable_fixed_points",
                         "fixed_points", "stable_points"])
        for r in results:
            fps = [(p["u"], p["v"]) for p in r["fixed_points"]]
            writer.writerow([
                r["alpha"],
                len(r["fixed_points"]),
                len(r["stable_points"]),
                repr(fps),
                repr(r["stable_points"]),
            ])


def summary(results):
    """Print a human-readable summary of the bistability scan."""
    bistable = [r for r in results if len(r["stable_points"]) == 2]
    max_stable = max(len(r["stable_points"]) for r in results)

    print("BIOLOGICAL_GENE_TOGGLE_EXACT_ROOT_AUDIT")
    print(f"model = du_dt = alpha/(1+v^n)-u ; dv_dt = alpha/(1+u^n)-v")
    print(f"hill_coefficient_n = {HILL_N!r}")
    print(f"alpha_scan = ({results[0]['alpha']!r}, {results[-1]['alpha']!r}, {ALPHA_STEP!r})")
    print(f"PASS_bistability_found = {len(bistable) > 0}")
    print(f"first_bistable_alpha = {bistable[0]['alpha']!r}" if bistable else "first_bistable_alpha = None")
    print(f"last_bistable_alpha = {bistable[-1]['alpha']!r}" if bistable else "last_bistable_alpha = None")
    print(f"maximum_stable_states_found = {max_stable}")
    if bistable:
        ex = bistable[0]
        print(f"example_bistable_alpha = {ex['alpha']!r}")
        print(f"example_stable_states_u_v = {ex['stable_points']!r}")
    print(f"PASS_no_false_five_state_artifact = {max_stable <= 2}")
    print(f"FINAL_PASS_GENE_MEMORY_SWITCH = {len(bistable) > 0 and max_stable <= 2}")


if __name__ == "__main__":
    import time

    start = time.time()
    results = analyze()
    summary(results)
    write_csv(results, "gene_toggle_exact_bistability.csv")
    print(f"csv_output = gene_toggle_exact_bistability.csv")
    print(f"elapsed_seconds = {time.time() - start!r}")
