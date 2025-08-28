.PHONY: install test lint format type-check clean run docker-build docker-run docker-push

# Variables
PYTHON = python3
PIP = pip3
STREAMLIT = streamlit
DOCKER = docker
DOCKER_COMPOSE = docker-compose
IMAGE_NAME = docu-judge
VERSION = 0.1.0

# Install dependencies
install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

# Install development dependencies
dev-install:
	$(PIP) install -r requirements-dev.txt

# Run tests
test:
	pytest tests/ -v --cov=./ --cov-report=term-missing

# Run linter
lint:
	pylint --disable=R,C,W1203,W1202 app.py config.py llm_service.py tests/

# Format code
format:
	black .

# Run type checking
type-check:
	mypy --ignore-missing-imports .

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	rm -rf .coverage coverage.xml htmlcov/

# Run the application
run:
	$(STREAMLIT) run app.py

# Docker build
docker-build:
	$(DOCKER) build -t $(IMAGE_NAME):$(VERSION) .
	$(DOCKER) tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest

# Docker run
docker-run:
	$(DOCKER) run -p 8501:8501 --env-file .env $(IMAGE_NAME):latest

# Docker Compose up
docker-up:
	$(DOCKER_COMPOSE) up --build -d

# Docker Compose down
docker-down:
	$(DOCKER_COMPOSE) down

# Docker push
docker-push:
	$(DOCKER) push $(IMAGE_NAME):$(VERSION)
	$(DOCKER) push $(IMAGE_NAME):latest
