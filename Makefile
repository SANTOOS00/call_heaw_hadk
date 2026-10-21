UV ?= uv

PYTHON := $(UV) run python

PYPROJECT ?= pyproject.toml

PROJECT := src

FLAGS := --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

PATH_FLAKE8 = $(UV) run flake8

PATH_MYPY = $(UV) run mypy



install:
	@$(UV) sync --all-packages
	@echo "venv environment has been created"

run:
	$(PYTHON) -m $(PROJECT)

clean:
	rm -rf .venv *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint: install
	$(PATH_FLAKE8) $(PROJECT)
	$(PATH_MYPY) $(PROJECT) $(FLAGS)

lint-strict: install
	@$(PATH_MYPY) $(PROJECT) --strict
	@$(PATH_FLAKE8) $(PROJECT)

debug:
	$(UV) run python -m pdb src/__main__.py

