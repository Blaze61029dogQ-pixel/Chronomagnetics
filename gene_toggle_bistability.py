#!/usr/bin/env python3
"""
BIOLOGICAL GENE TOGGLE MEMORY SWITCH SOLVER

Determines whether mutual gene repression can create stable biological memory.

Model:
    du/dt = alpha / (1 + v^n) - u
    dv/dt = alpha / (1 + u^n) - v

The system models two genes u and v that mutually repress each other.
Bistability (two coexisting stable states) is the mathematical signature
of cellular memory — the same circuit can "remember" which gene was
initially dominant.
"""

import csv
import os
import time

import numpy as np
from scipy.optimize import fsolve


# ---------------------------------------------------------------------------
# Core model equations
# ---------------------------------------------------------------------------

def equations(x, alpha, n):
    u, v = x
    return [alpha / (1.0 + v**n) - u,
            alpha / (1.0 + u**n) - v]


def jacobian_at(u, v, alpha, n):
    """Jacobian of the ODE system evaluated at (u, v)."""
    dv_denom = (1.0 + v**n) ** 2
    du_denom = (1.0 + u**n) ** 2
    return np.array([
        [-1.0,                          -alpha * n * v**(n - 1) / dv_denom],
        [-alpha * n * u**(n - 1) / du_denom, -1.0],
    ])


def is_stable(u, v, alpha, n, tol=0.0):
    """Return True when all Jacobian eigenvalues have negative real parts."""
    eigs = np.linalg.eigvals(jacobian_at(u, v, alpha, n))
    return all(ev.real < tol for ev in eigs)


# ---------------------------------------------------------------------------
# Equilibrium finder
# ---------------------------------------------------------------------------

def find_equilibria(alpha, n, grid=10, dup_tol=1e-5):
    """
    Multi-start root-finding over a 2-D grid.

    Returns (all_equilibria, stable_equilibria) as lists of (u, v) tuples.
    """
    coords = np.linspace(0.05, max(alpha * 1.5, 1.5), grid)
    all_eq, stable_eq = [], []

    for u0 in coords:
        for v0 in coords:
            try:
                sol, _, ier, _ = fsolve(
                    equations, [u0, v0], args=(alpha, n), full_output=True
                )
            except Exception:
                continue

            if ier != 1:
                continue

            u_eq, v_eq = sol
            if u_eq < 0.0 or v_eq < 0.0:
                continue

            residual = np.max(np.abs(equations(sol, alpha, n)))
            if residual > 1e-8:
                continue

            # Deduplicate with tight tolerance to capture near-bifurcation states
            if any(abs(ue - u_eq) < dup_tol and abs(ve - v_eq) < dup_tol
                   for ue, ve in all_eq):
                continue

            all_eq.append((u_eq, v_eq))
            if is_stable(u_eq, v_eq, alpha, n):
                stable_eq.append((u_eq, v_eq))

    return all_eq, stable_eq


# ---------------------------------------------------------------------------
# Alpha scan
# ---------------------------------------------------------------------------

def run_scan(alpha_min, alpha_max, alpha_step, n):
    """
    Sweep alpha over [alpha_min, alpha_max] and record stability for each value.

    Returns:
        rows                – list of dicts for CSV
        first_bistable      – first alpha with >= 2 stable states (or None)
        last_bistable       – last such alpha
        max_stable_count    – maximum number of stable states found
        best_alpha          – alpha at which max_stable_count was achieved
        best_stable_states  – the corresponding stable states
    """
    alphas = np.arange(alpha_min, alpha_max + alpha_step / 2.0, alpha_step)

    rows = []
    first_bistable = last_bistable = None
    max_stable_count = 0
    best_alpha = None
    best_stable_states = []

    for alpha in alphas:
        alpha_r = round(float(alpha), 10)
        _, stable = find_equilibria(alpha_r, n)
        n_stable = len(stable)
        bistable = n_stable >= 2

        if bistable:
            if first_bistable is None:
                first_bistable = alpha_r
            last_bistable = alpha_r

        if n_stable > max_stable_count:
            max_stable_count = n_stable
            best_alpha = alpha_r
            best_stable_states = stable

        rows.append({
            "alpha": alpha_r,
            "n_stable_states": n_stable,
            "is_bistable": bistable,
        })

    return rows, first_bistable, last_bistable, max_stable_count, best_alpha, best_stable_states


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    n = 2.0
    alpha_min = 1.0
    alpha_max = 11.0
    alpha_step = 0.10000000000000009

    print("=" * 70)
    print("BIOLOGICAL GENE TOGGLE MEMORY SWITCH SOLVER")
    print("=" * 70)
    print(f"model        = du_dt = alpha/(1+v^n)-u ; dv_dt = alpha/(1+u^n)-v")
    print(f"hill_coefficient_n   = {n}")
    print(f"alpha_scan   = {alpha_min} → {alpha_max}  (step {alpha_step})")
    print()

    t0 = time.time()

    rows, first_bistable, last_bistable, max_stable, best_alpha, best_states = run_scan(
        alpha_min, alpha_max, alpha_step, n
    )

    elapsed = time.time() - t0
    bistability_found = first_bistable is not None

    # --- CSV output ---------------------------------------------------------
    csv_path = "/root/pai/outputs/gene_toggle_bistability.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["alpha", "n_stable_states", "is_bistable"])
        writer.writeheader()
        writer.writerows(rows)

    # --- Print summary ------------------------------------------------------
    print(f"problem              = determine whether mutual gene repression can create stable biological memory")
    print(f"PASS_bistability_found = {bistability_found}")
    print(f"first_bistable_alpha   = {first_bistable}")
    print(f"last_bistable_alpha    = {last_bistable}")
    print(f"maximum_stable_states_found = {max_stable}")
    print(f"example_best_alpha     = {best_alpha}")
    print(f"example_stable_states_u_v = {best_states}")
    print(f"interpretation = the terminal found the parameter range where the same")
    print(f"  genetic circuit has two stable expression states, which is a mathematical")
    print(f"  model of cellular memory")
    print(f"csv_output     = {csv_path}")
    print(f"elapsed_seconds = {elapsed:.4f}")

    return bistability_found


if __name__ == "__main__":
    main()
