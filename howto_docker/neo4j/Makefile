# REQUIRED SECTION -----------------------------
include ../Makefile.docker
DK  := docker
DC  := docker-compose
DCF := docker-compose.yml

.DEFAULT_GOAL := help
help: ##@other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
containers: ##@other c=<lab, serving, flask, neo4j>
	@echo "lab, serving"
# END OF REQUIRED SECTION ----------------------

## Docker-Compose Command
build: ## Build all or c=<container>
	@$(DC) -f $(DCF) build $(c)

up: ## Start all interactively or c=<container>
	@$(DC) -f $(DCF) up $(c)

down: ## Stop all containers and Remove all.
	@$(DC) -f $(DCF) down $(c)

start: ## Start all daemon or c=<container>
	@$(DC) -f $(DCF) up -d $(c)

stop: ## Stop all or c=<container>
	@$(DC) -f $(DCF) stop $(c)

restart: ## Restart all or c=<container>
	@$(DC) -f $(DCF) stop $(c)
	@$(DC) -f $(DCF) up $(c) -d

## Show the images & containers
lsimg: ## Listing images
	@$(DK) image ls
lscon: ## Listing containers
	@$(DK) container ls -a
ls: lsimg lscon ## Listing all images

## Show the container information.
ps: ## Status of All containers
	@$(DC) -f $(DCF) ps
info: ## Container information. c=<container>
	@$(DK) history $(c)

## Enter into container
in: ## Enter into running container. c=<container>
	@$(DK) exec -it $(c) /bin/bash
inother: ## Create new container & into the container. c=<container>
	@$(DK) run --rm --privileged -it $(c) /bin/bash

## Cleaning
rmimg: ## Cleaning All images
	@$(DK) image rm -f $(shell $(DK) image ls -q)
rmcon: ## Cleaning All containers
	@$(DK) container stop $(shell $(DK) container ls -aq)
	@$(DK) container rm -f $(shell $(DK) container ls -aq)
rm: rmimg rmcon ## Cleaning All
