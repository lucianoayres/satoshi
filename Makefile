# Define the Python interpreter and virtual environment directory
PYTHON := python3
VENV_DIR := .venv
ACTIVATE := $(VENV_DIR)/bin/activate
SRC_DIR := src

# Define directories and files to clean
CLEAN_DIRS := $(VENV_DIR) build dist *.egg-info .pytest_cache
CLEAN_FILES := $(shell find . -type f -name "*.pyc")

# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make setup         - Set up the virtual environment and install dependencies"
	@echo "  make run           - Run the application"
	@echo "  make test          - Run tests"
	@echo "  make build         - Create a distribution package"
	@echo "  make clean         - Remove temporary files and the virtual environment"

# Set up virtual environment and install dependencies
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(ACTIVATE) && pip install --upgrade pip setuptools
	. $(ACTIVATE) && pip install -r requirements.txt
	. $(ACTIVATE) && pip install -e .[dev]  # Install in editable mode with dev dependencies

# Run the application
SYMBOL := BTC
CURRENCY := BRL
COST := 1

.PHONY: run
run:
	. $(ACTIVATE) && $(PYTHON) $(SRC_DIR)/main.py $(SYMBOL) $(CURRENCY) $(COST)

# Run tests with PYTHONPATH set to src/
.PHONY: test
test:
	. $(ACTIVATE) && PYTHONPATH=src pytest tests/

# Build a distribution package
.PHONY: build
build:
	. $(ACTIVATE) && python setup.py sdist bdist_wheel

# Clean temporary files, remove the virtual environment, and delete pytest cache
.PHONY: clean
clean:
	rm -rf $(CLEAN_DIRS)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage htmlcov/