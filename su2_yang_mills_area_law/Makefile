VENV   ?= .venv
PYTHON ?= $(shell test -x $(VENV)/bin/python && echo $(VENV)/bin/python || echo python3)

.PHONY: setup check reproduce full hashes clean

## setup: create .venv and install the pinned requirements
setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r requirements.txt

## check: integrity checks and tests (CI-suitable; needs the requirements)
check:
	$(PYTHON) -m compileall -q tools tests reproduction
	$(PYTHON) tools/verify_repository.py
	$(PYTHON) -m unittest discover -s tests -v
	sha256sum -c --quiet MANIFEST.sha256

## reproduce: quick run of the SI script (writes results/quick/; fails if any check FAILs)
reproduce:
	$(PYTHON) reproduction/run_reproduction.py

## full: full run with the papers' grids (writes results/full/; fails if any check FAILs)
full:
	$(PYTHON) reproduction/run_reproduction.py --full

## hashes: regenerate MANIFEST.sha256 (review the diff before committing)
hashes:
	$(PYTHON) tools/verify_repository.py --write-manifest

## clean: remove caches only; never sources, originals, provenance or results
clean:
	find . -path ./.git -prune -o -type d \( -name __pycache__ -o -name .pytest_cache \) -print -exec rm -rf {} +
