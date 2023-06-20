
setup-local:
	poetry config --local virtualenvs.in-project true
	poetry install
	pre-commit install
.PHONY: setup-local
