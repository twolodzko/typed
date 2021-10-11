
LINE_LENGTH := 120

test: ## Run unit tests
	pytest -v .

lint: ## Run linters
	black --line-length $(LINE_LENGTH) --check .
	flake8 --max-line-length $(LINE_LENGTH) .
	mypy .

stylefix: ## Fix code style issues
	black --line-length $(LINE_LENGTH) .

help: ## Print help
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
