.PHONY: all
all: help

.PHONY: flake
flake: ## Run flake8
	flake8 --statistics --count .

.PHONY: tests
tests: ## Run tests
	  # Running tests:
		pytest --cov

.PHONY: check
check: ## Run pip check
		# Checking dependencies status:
		pip check

.PHONY: lint
lint: flake ## Run all linters

.PHONY: generate-secret-key
generate-secret-key:  ## Generate secret key
	@python -c 'import secrets; print(secrets.token_urlsafe())'

.PHONY: generate-secret-salt
generate-secret-salt:  ## Generate secret salt
	@python -c 'import secrets; print(secrets.SystemRandom().getrandbits(128))'

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
