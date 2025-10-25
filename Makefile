# TTS Agents Makefile
# Professional development and deployment automation

.PHONY: help install install-dev test test-cov lint format type-check security clean build publish docker docs serve-docs

# Default target
help: ## Show this help message
	@echo "TTS Agents - Professional Text-to-Speech Library"
	@echo "================================================"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "For more information, see: https://github.com/muhammadbilalkhan/tts-agents"

# Installation
install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

# Testing
test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=src/tts_agents --cov-report=term-missing --cov-report=html

test-fast: ## Run fast tests only
	pytest tests/ -v -m "not slow"

# Code Quality
lint: ## Run linting
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format: ## Format code
	black src/ tests/
	ruff check src/ tests/ --fix
	isort src/ tests/

type-check: ## Run type checking
	mypy src/

security: ## Run security checks
	safety check
	bandit -r src/ -f json -o bandit-report.json || true

# Development
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf coverage.xml
	rm -rf bandit-report.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete

# Build and Publish
build: clean ## Build package
	python -m build

build-check: ## Check package
	python -m build
	twine check dist/*

publish-test: ## Publish to TestPyPI
	python -m build
	twine upload --repository testpypi dist/*

publish: ## Publish to PyPI
	python -m build
	twine upload dist/*

# Docker
docker-build: ## Build Docker image
	docker build -t tts-agents .

docker-run: ## Run Docker container
	docker run --rm -e OPENAI_API_KEY=$$OPENAI_API_KEY tts-agents

docker-compose-up: ## Start services with Docker Compose
	docker-compose up -d

docker-compose-down: ## Stop services with Docker Compose
	docker-compose down

docker-compose-logs: ## View Docker Compose logs
	docker-compose logs -f

# Documentation
docs: ## Build documentation
	mkdocs build

serve-docs: ## Serve documentation locally
	mkdocs serve

docs-deploy: ## Deploy documentation
	mkdocs gh-deploy

# Examples
examples: ## Run examples
	python examples/basic_usage.py
	python examples/batch_processing.py
	python examples/streaming_example.py

# CLI
cli-help: ## Show CLI help
	python -m tts_agents.cli --help

cli-voices: ## List available voices
	python -m tts_agents.cli voices

cli-models: ## List available models
	python -m tts_agents.cli models

cli-formats: ## List available formats
	python -m tts_agents.cli formats

# Development workflow
dev-setup: clean install-dev ## Set up development environment
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to verify everything is working."

dev-check: lint type-check security test ## Run all development checks
	@echo "All checks passed!"

dev-full: clean install-dev dev-check build ## Full development workflow
	@echo "Full development workflow completed successfully!"

# CI/CD
ci-test: ## Run CI test suite
	pytest tests/ -v --cov=src/tts_agents --cov-report=xml --cov-report=html
	ruff check src/ tests/
	black --check src/ tests/
	mypy src/
	bandit -r src/ -f json -o bandit-report.json || true

# Release
release-check: ## Check release readiness
	@echo "Checking release readiness..."
	@echo "✓ Tests passing: $(shell make test > /dev/null 2>&1 && echo 'PASS' || echo 'FAIL')"
	@echo "✓ Linting: $(shell make lint > /dev/null 2>&1 && echo 'PASS' || echo 'FAIL')"
	@echo "✓ Type checking: $(shell make type-check > /dev/null 2>&1 && echo 'PASS' || echo 'FAIL')"
	@echo "✓ Security: $(shell make security > /dev/null 2>&1 && echo 'PASS' || echo 'FAIL')"
	@echo "✓ Build: $(shell make build > /dev/null 2>&1 && echo 'PASS' || echo 'FAIL')"

# Monitoring
monitor: ## Monitor system resources
	@echo "System monitoring..."
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Disk usage: $(shell du -sh .)"
	@echo "Memory usage: $(shell free -h 2>/dev/null || echo 'N/A')"

# Environment
env-check: ## Check environment
	@echo "Environment check..."
	@echo "Python: $(shell python --version)"
	@echo "Pip: $(shell pip --version)"
	@echo "Git: $(shell git --version)"
	@echo "Docker: $(shell docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker Compose: $(shell docker-compose --version 2>/dev/null || echo 'Not installed')"

# Helpers
version: ## Show version
	@python -c "import tts_agents; print(tts_agents.__version__)"

info: ## Show package information
	@echo "TTS Agents Package Information"
	@echo "=============================="
	@python -c "import tts_agents; print(f'Version: {tts_agents.__version__}')"
	@python -c "import tts_agents; print(f'Author: {tts_agents.__author__}')"
	@python -c "import tts_agents; print(f'Email: {tts_agents.__email__}')"
	@echo "Available voices: $(shell python -c 'from tts_agents import TTSAgent; import asyncio; print(len(asyncio.run(TTSAgent().get_available_voices())))')"
	@echo "Available models: $(shell python -c 'from tts_agents import TTSAgent; import asyncio; print(len(asyncio.run(TTSAgent().get_available_models())))')"
	@echo "Available formats: $(shell python -c 'from tts_agents import TTSAgent; import asyncio; print(len(asyncio.run(TTSAgent().get_available_formats())))')"

# Default target
.DEFAULT_GOAL := help
