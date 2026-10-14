VENV   = .venv
PYTHON = $(VENV)/bin/python
PIP    = $(VENV)/bin/pip
FLAKE8 = $(VENV)/bin/flake8
MYPY   = $(VENV)/bin/mypy

MAIN   = a_maze_ing.py
CONFIG = config.txt

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint lint-strict

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	$(FLAKE8) .
	$(MYPY) . $(MYPY_FLAGS)

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict