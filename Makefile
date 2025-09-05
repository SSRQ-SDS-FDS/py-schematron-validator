EXECUTABLES = poetry
require := $(foreach exec,$(EXECUTABLES),\
        		$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

all: type-check test build

build:
	@uv build

# PHONY targets
.PHONY: fmt test

fmt:
	@uv run ruff format .
	@uv run ruff --fix  .

fmt-check:
	@echo "Checking formatting using ruff..."
	@uv run ruff format --check .

lint:
	@echo "Linting using ruff..."
	@uv run ruff .

test:
	@echo "Running tests..."
	@uv run pytest

type-check:
	@echo "Checking types using pyright..."
	@uv run pyright
