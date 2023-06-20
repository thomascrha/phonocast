SHELL      := /bin/bash

setup-local:
	poetry config --local virtualenvs.in-project true
	poetry install
	pre-commit install
.PHONY: setup-local

run:
	uvicorn src.api:api --reload
.PHONY: run
