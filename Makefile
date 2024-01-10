EXECUTABLES = poetry
require := $(foreach exec,$(EXECUTABLES),\
        		$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

all: type-check build

build:
	@poetry build

# PHONY targets
.PHONY: fmt test

fmt:
	@poetry run ruff format .
	@poetry run ruff --fix  .

fmt-check:
	@echo "Checking formatting using ruff..."
	@poetry run ruff format --check .

lint:
	@echo "Linting using ruff..."
	@poetry run ruff .

test:
	@echo "Running tests..."
	@poetry run pytest

type-check:
	@echo "Checking types using pyright..."
	@poetry run pyright
