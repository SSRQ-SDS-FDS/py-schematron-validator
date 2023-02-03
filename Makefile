EXECUTABLES = poetry
require := $(foreach exec,$(EXECUTABLES),\
        		$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

all: type-check build

build:
	@poetry build

# PHONY targets
.PHONY: fmt test

fmt:
	@poetry run black .
	@poetry run ruff --fix  .

fmt-check:
	@echo "Checking formatting using black..."
	@poetry run black --check .

lint:
	@echo "Linting using ruff..."
	@poetry run ruff .

type-check:
	@echo "Checking types using pyright..."
	@poetry run pyright
