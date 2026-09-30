#!/usr/bin/env python3
"""Repository integrity checks (standard library only).

These checks cover the repository, not the mathematics. They verify that:

  * every entry in MANIFEST.sha256 matches the file on disk, and every
    repository file is listed;
  * every imported original (provenance/source_hashes.sha256) and every
    derived release artifact (provenance/release_hashes.sha256) has its
    recorded SHA-256;
  * relative Markdown links in the top-level documentation resolve;
  * no absolute local filesystem paths or common credential patterns occur
    in text files.

Usage:
    python3 tools/verify_repository.py                  # run all checks
    python3 tools/verify_repository.py --write-manifest # regenerate MANIFEST.sha256

Exit status: 0 if all checks pass, 1 otherwise.
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = "MANIFEST.sha256"
PDF = "paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf"
SOURCE_HASHES = "provenance/source_hashes.sha256"
RELEASE_HASHES = "provenance/release_hashes.sha256"
DOCS = [
    "README.md", "CLAIMS.md", "CITATIONS.md", "REPRODUCIBILITY.md",
    "CONTRIBUTING.md", "LICENSING.md", "CHANGELOG.md",
    "reproduction/README.md", "paper/README.md", "supplementary/README.md",
    "results/README.md", "provenance/FILES.md", ".github/RELEASE_CHECKLIST.md",
]
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", "ci-output"}
TEXT_SUFFIXES = {".md", ".py", ".txt", ".toml", ".yml", ".yaml", ".cff",
                 ".sha256", ".json", ".log", ".patch", ".bib", ""}

# Patterns are assembled from pieces so that this file does not match itself.
ABS_PATH_PATTERNS = [
    re.compile("/" + "home/"), re.compile("/" + "root/"),
    re.compile("/" + "Users/"), re.compile("/" + "tmp/"),
    re.compile("[A-Za-z]:" + r"\\\\" + "Users"),
]
SECRET_PATTERNS = [
    re.compile("gh" + "[pousr]_[A-Za-z0-9]{30,}"),
    re.compile("github" + "_pat_[A-Za-z0-9_]{20,}"),
    re.compile("AK" + "IA[0-9A-Z]{16}"),
    re.compile("sk" + r"-[A-Za-z0-9\-_]{20,}"),
    re.compile("-----BEGIN [A-Z ]*" + "PRIVATE KEY-----"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def repo_files():
    out = []
    for p in sorted(ROOT.rglob("*")):
        rel = p.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if p.is_file() and rel.as_posix() != MANIFEST:
            out.append(rel.as_posix())
    return out


def read_hash_file(path: Path):
    entries = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        digest, name = line.split(None, 1)
        entries[name.lstrip("*").strip()] = digest
    return entries


def write_manifest():
    lines = [f"{sha256(ROOT / f)}  {f}" for f in repo_files()]
    (ROOT / MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} with {len(lines)} entries")


def check_manifest(errors):
    entries = read_hash_file(ROOT / MANIFEST)
    for name, digest in entries.items():
        p = ROOT / name
        if not p.is_file():
            errors.append(f"manifest: missing file {name}")
        elif sha256(p) != digest:
            errors.append(f"manifest: hash mismatch {name}")
    for f in repo_files():
        if f not in entries:
            errors.append(f"manifest: file not listed {f}")
    return len(entries)


def check_recorded_hashes(errors):
    """Every original and release artifact must match its recorded SHA-256."""
    n = 0
    for record in (SOURCE_HASHES, RELEASE_HASHES):
        entries = read_hash_file(ROOT / record)
        if not entries:
            errors.append(f"provenance: {record} has no entries")
        for name, digest in entries.items():
            n += 1
            p = ROOT / name
            if not p.is_file():
                errors.append(f"provenance: {record} lists missing file {name}")
            elif sha256(p) != digest:
                errors.append(f"provenance: {name} differs from {record}")
    if PDF not in read_hash_file(ROOT / SOURCE_HASHES):
        errors.append(f"provenance: {PDF} not recorded as an original")
    return n


def check_links(errors):
    link = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
    for doc in DOCS:
        p = ROOT / doc
        if not p.is_file():
            errors.append(f"docs: missing {doc}")
            continue
        for target in link.findall(p.read_text(encoding="utf-8")):
            if re.match(r"^[a-z]+:", target):
                continue
            if not (p.parent / target).exists():
                errors.append(f"docs: {doc} links to missing {target}")


def check_text_hygiene(errors):
    for f in repo_files():
        p = ROOT / f
        if p.suffix not in TEXT_SUFFIXES:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for pat in ABS_PATH_PATTERNS:
            if pat.search(text):
                errors.append(f"hygiene: absolute local path in {f}")
                break
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                errors.append(f"hygiene: credential-like string in {f}")
                break


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write-manifest", action="store_true",
                    help="regenerate MANIFEST.sha256 and exit")
    args = ap.parse_args(argv)
    if args.write_manifest:
        write_manifest()
        return 0

    errors = []
    n = check_manifest(errors)
    check_recorded_hashes(errors)
    check_links(errors)
    check_text_hygiene(errors)
    for e in errors:
        print("FAIL", e)
    status = "PASS" if not errors else "FAIL"
    print(f"{status}: {n} manifest entries, {len(errors)} problem(s)")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
