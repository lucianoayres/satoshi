# Define the Python interpreter and virtual environment directory
PYTHON := python3
VENV_DIR := .venv
ACTIVATE := $(VENV_DIR)/bin/activate
SRC_DIR := src

# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make setup         - Set up the virtual environment and install dependencies"
	@echo "  make run           - Run the application"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Check code style with flake8"
	@echo "  make build         - Create a distribution package"
	@echo "  make clean         - Remove temporary files and the virtual environment"

# Set up virtual environment and install dependencies
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(ACTIVATE) && pip install --upgrade pip setuptools
	. $(ACTIVATE) && pip install -r requirements.txt

# Run the application
SYMBOL := BTC
CURRENCY := BRL
COST := 100

.PHONY: run
run:
	. $(ACTIVATE) && $(PYTHON) $(SRC_DIR)/main.py $(SYMBOL) $(CURRENCY) $(COST)

# Run tests
.PHONY: test
test:
	. $(ACTIVATE) && pytest tests/

# Build a distribution package
.PHONY: build
build:
	. $(ACTIVATE) && python setup.py sdist bdist_wheel

# Clean temporary files and remove the virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV_DIR) build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
