TAG := "0.1.0"
ORGANIZATION := mkm29
APP := slock

DOCKER_URL := "docker.io"
DOCKER_USER := "mkm29"
DOCKER_PASS := ""

# HELP
# This will output the help for each task
.PHONY: help build login push test

# Tasks
help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build Docker image
	@echo Building Docker image
	@docker build -t $(ORGANIZATION)/$(APP):$(TAG) .

login: ## Login to Docker registry
	@echo Logging into Docker regisrty
	@echo $(DOCKER_PASS) | docker login --username $(DOCKER_USER) --password-stdin $(DOCKER_URL)

push: login ## Publish Docker image to Docker Hub
	@echo Pushing Image
	@docker push $(ORGANIZATION)/$(APP):$(TAG)

test: ## Run all unit/integration tests
	@echo Running all unit/integration tests for project
	@pytest