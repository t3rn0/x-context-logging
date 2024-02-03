ALL_CODE = context.py logger.py server.py client.py

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: format
format:	## format code
	isort $(ALL_CODE)
	black $(ALL_CODE)

.PHONY: lint
lint:	## lint code
	flake8 $(ALL_CODE) --config ./setup.cfg
	black --check $(ALL_CODE) 
	poetry check
