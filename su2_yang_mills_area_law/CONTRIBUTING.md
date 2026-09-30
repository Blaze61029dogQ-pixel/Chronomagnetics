# Contributing

This repository accompanies unpublished drafts. Please use the categories
below. Code contributions are accepted under the MIT License (see
`LICENSING.md` for what the MIT License does and does not cover).

## 1. Mathematical corrections

Open an issue that gives:

- the **exact location**: theorem, lemma, proposition, equation or remark
  number, with the page in `paper/original/Paper1_AreaLaw_SU2_2026-09-28.pdf`;
- the **proposed correction**, stated precisely;
- a **derivation or counterexample** showing why the current statement fails;
- **reproduction steps** if the objection is computational: code, precision,
  and the exact output.

The manuscript is not edited through pull requests to this repository. The
author revises the source and replaces the PDF, and the hashes are updated.

## 2. Literature and attribution corrections

Give the full bibliographic reference, the page or theorem number in the
cited work, and the statement in the manuscript that it affects. Priority
statements in the manuscript are qualified ("not found recorded"). Evidence
that a result is already recorded is especially welcome.

## 3. Reproduction failures

Use the **Reproduction failure** issue template. Include the command, exit
status, full output, Python and package versions, OS, and the output of
`sha256sum -c MANIFEST.sha256`.

## 4. Software improvements

- Never change a scientific script to make a failing check pass. Report the
  failure instead.
- Never edit `reproduction/original/` or `paper/original/` or
  `supplementary/original/`: originals are provenance records. Integration
  changes go in wrappers or in documented patches under
  `reproduction/patches/`.
- Keep changes to certificate code minimal and reviewable. Preserve exact
  arithmetic where the manuscript relies on it.
- Run `make check` before opening a pull request. If files changed, run
  `make hashes` and commit the updated `MANIFEST.sha256`.

## 5. Documentation improvements

Keep theorem labels, constants and claim scope synchronised with the
manuscript. Do not add claims the manuscript does not make, in particular
anything about the continuum limit or a continuum mass gap.
