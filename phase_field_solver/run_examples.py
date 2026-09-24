#!/usr/bin/env python3
"""Reproduce verification and all eight example jobs; stop on the first failure."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("my_runs"))
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        env.setdefault(key, "1")
    jobs = [
        ("verification", ["verify_solver.py", "--out", str(out / "verification.json")]),
        ("corrugated_spectrum", ["phasefield.py", "spectrum", "--config", "examples/corrugated.json", "--count", "9"]),
        ("lapse_spectrum", ["phasefield.py", "spectrum", "--config", "examples/variable_lapse.json", "--count", "6"]),
        ("nonlinear_wave", ["phasefield.py", "evolve", "--config", "examples/corrugated.json", "--dt", "1/200", "--steps", "1000", "--sample-every", "10"]),
        ("nonuniform_equilibrium", ["phasefield.py", "equilibrium", "--config", "examples/broken_equilibrium.json"]),
        ("driven_wave", ["phasefield.py", "evolve", "--config", "examples/driven.json", "--dt", "1/200", "--steps", "400", "--sample-every", "20"]),
        ("driven_resumed", ["phasefield.py", "resume", str(out / "driven_wave" / "checkpoint.npz"), "--steps", "200", "--sample-every", "20"]),
        ("refinement", ["phasefield.py", "converge", "--config", "examples/corrugated.json", "--cutoffs", "2,3,4,5", "--quadratures", "32,48,64", "--count", "8"]),
        ("potential_sweep", ["phasefield.py", "sweep", "--config", "examples/potential.json", "--parameter", "potential_amplitude", "--values", "0,1/40,1/20,1/10,1/5", "--count", "6"]),
    ]
    completed = []
    for name, command in jobs:
        if name != "verification":
            command += ["--out", str(out / name)]
        print("Running " + name, flush=True)
        result = subprocess.run([sys.executable, *command], cwd=ROOT, env=env)
        completed.append({"name": name, "returncode": result.returncode, "arguments": command})
        (out / "runner.json").write_text(
            json.dumps({"jobs": completed, "python": sys.executable}, indent=2) + "\n",
            encoding="utf-8",
        )
        if result.returncode:
            return result.returncode
    print("Completed verification and all eight example jobs.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
