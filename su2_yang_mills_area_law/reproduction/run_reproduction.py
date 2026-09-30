#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 James M. Lockwood
"""Run SI_YangMills_reproduce_all.py and record the run (standard library only).

This wrapper does not modify or re-implement any computation. It runs the
imported script unchanged in a subprocess and records:

  * the exact command (paths relative to the repository root);
  * UTC start/end times, wall-clock duration and exit status;
  * Python version, platform, and installed numpy / scipy / mpmath versions;
  * the SHA-256 of the script that was run;
  * the combined stdout/stderr, streamed to the console and saved verbatim
    except for the documented path substitutions listed in run_meta.json;
  * the script's own JSON report (its --json option).

Usage:
    python3 reproduction/run_reproduction.py                 # quick mode
    python3 reproduction/run_reproduction.py --full          # the papers' grids
    python3 reproduction/run_reproduction.py --sections S1,S4
    python3 reproduction/run_reproduction.py --outdir results/quick
    python3 reproduction/run_reproduction.py \
        --script reproduction/original/SI_YangMills_reproduce_all.py \
        --outdir results/original-export/quick

The exit status is the script's own exit status (0 only if no check FAILs),
or 124 if --timeout expires.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path("reproduction") / "SI_YangMills_reproduce_all.py"
PACKAGES = ("numpy", "scipy", "mpmath")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def package_versions():
    from importlib import metadata
    out = {}
    for name in PACKAGES:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = None
    return out


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--script", default=SCRIPT.as_posix(),
                    help="script to run, relative to the repository root "
                         "(default: the release copy)")
    ap.add_argument("--full", action="store_true",
                    help="pass --full to the script (the papers' grids; slow)")
    ap.add_argument("--sections", default=None,
                    help="pass --sections to the script, e.g. S1,S5")
    ap.add_argument("--outdir", default=None,
                    help="output directory (default results/quick or results/full)")
    ap.add_argument("--timeout", type=float, default=None,
                    help="seconds before the run is killed (default: none)")
    args = ap.parse_args(argv)

    script = Path(args.script)
    if script.is_absolute() or not (ROOT / script).is_file():
        ap.error(f"--script must be an existing path relative to the repository root: {args.script}")
    mode = "full" if args.full else "quick"
    outdir = Path(args.outdir) if args.outdir else Path("results") / mode
    outdir_abs = (ROOT / outdir) if not outdir.is_absolute() else outdir
    outdir_abs.mkdir(parents=True, exist_ok=True)
    try:
        rel_out = outdir_abs.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rel_out = outdir_abs.as_posix()
    report_rel = f"{rel_out}/report.json"

    cmd = ["python3", script.as_posix()]
    if args.full:
        cmd.append("--full")
    if args.sections:
        cmd += ["--sections", args.sections]
    cmd += ["--json", report_rel]

    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    start, t0 = utc_now(), time.monotonic()
    lines, fired = [], []
    proc = subprocess.Popen([sys.executable] + cmd[1:], cwd=ROOT, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace")

    def _kill():
        fired.append(True)
        proc.kill()

    watchdog = None
    if args.timeout is not None:
        watchdog = threading.Timer(args.timeout, _kill)
        watchdog.start()
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        lines.append(line)
    proc.wait()
    if watchdog is not None:
        watchdog.cancel()
    timed_out = bool(fired)
    wall = time.monotonic() - t0
    end = utc_now()
    code = 124 if timed_out else proc.returncode

    # Documented substitutions so that no machine-specific absolute path is
    # stored: the repository root and the interpreter prefix.
    subs = {str(ROOT): "<REPO>", sys.prefix: "<PYTHON_PREFIX>",
            sys.base_prefix: "<PYTHON_BASE_PREFIX>"}
    text = "".join(lines)
    applied = {}
    for old, new in sorted(subs.items(), key=lambda kv: -len(kv[0])):
        if old and old in text:
            applied[new] = text.count(old)
            text = text.replace(old, new)
    (outdir_abs / "stdout.log").write_text(text, encoding="utf-8")

    summary = [l.strip() for l in lines if l.startswith("SUMMARY:")]
    meta = dict(
        command=" ".join(cmd),
        interpreter=sys.executable.replace(sys.prefix, "<PYTHON_PREFIX>"),
        cwd="<REPO>",
        mode=mode,
        sections=args.sections,
        start_utc=start,
        end_utc=end,
        wall_seconds=round(wall, 3),
        exit_status=code,
        timed_out=timed_out,
        timeout_seconds=args.timeout,
        summary_line=summary[-1] if summary else None,
        script=script.as_posix(),
        script_sha256=sha256(ROOT / script),
        python=platform.python_version(),
        python_implementation=platform.python_implementation(),
        platform=f"{platform.system()} {platform.machine()}",
        cpu_count=os.cpu_count(),
        packages=package_versions(),
        log="stdout.log",
        report="report.json" if (outdir_abs / "report.json").exists() else None,
        path_substitutions_applied=applied,
    )
    (outdir_abs / "run_meta.json").write_text(json.dumps(meta, indent=1) + "\n",
                                              encoding="utf-8")
    print(f"[run_reproduction] exit_status={code} wall={wall:.1f}s "
          f"outputs in {rel_out}/", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
