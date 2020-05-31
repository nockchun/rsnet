# GLOBAL VARIABLES ----------------------------------------------------------
DK  := docker
DC  := docker-compose
DCF := /data/notebooks/rsnet/how_to_make_system/docker/devcpu.compose.yml
HUB := 192.168.0.17:5000

# COLORS & UTIL FUNCTION ----------------------------------------------------
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RED    := $(shell tput -Txterm setaf 1)
RESET  := $(shell tput -Txterm sgr0)
HELP_FUN = \
    %help; \
    while(<>) { push @{$$help{$$2 // 'options'}}, \
    [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
    print "usage: make option t=[target]\n\n"; \
    for (sort keys %help) { \
    print "${WHITE}$$_:${RESET}\n"; \
    for (@{$$help{$$_}}) { \
    $$sep = " " x (16 - length $$_->[0]); \
    print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
    }; \
    print "\n"; }
.DEFAULT_GOAL := help
# GLOBAL FUNCTIONS ----------------------------------------------------------
CRLF:
	@echo ""

define fun_imgrm
	@docker container stop ${1}
    @docker image rm ${1}
endef

define fun_conrm
	@docker container stop ${1}
    @docker container rm ${1}
endef
# List Up Images And Containers ---------------------------------------------
svc: ##@Show All services of compose.
	@$(DC) -f $(DCF) config --services

ls: lsimg CRLF lscon ##@Show Listing all images & containers

lsimg: ##@Show Listing images
	@$(DK) image ls

lscon: ##@Show Listing containers
	@$(DK) container ls -a

# Docker-Compose Control For Service ----------------------------------------
build: ## Build all. OR t=<name>
	@$(DC) -f $(DCF) build $(t)

up: ## Start all interactively. OR t=<name>
	@$(DC) -f $(DCF) up $(t)

down: ## Stop & Remove all containers. OR t=<name>
ifeq ($(t), )
	@$(DC) -f $(DCF) down
else
	@$(call fun_conrm, $(t); exit 0)
endif

start: ## Start all. OR t=<name>
	@$(DC) -f $(DCF) up -d $(t)

stop: ## Stop all or t=<name>
	@$(DC) -f $(DCF) stop $(t)

restart: ## Restart all or t=<name>
	@$(DC) -f $(DCF) stop $(t) 2>/dev/null
	@$(DC) -f $(DCF) up -d $(t)

# Show The Information ------------------------------------------------------
ps: ##@Show Status compose container. t=<all> for all
ifeq ($(t), all)
	@$(DK) ps
else
	@$(DC) -f $(DCF) ps
endif

info: ##@Show Container information. t=<name>
ifeq ($(t), )
	@echo ${YELLOW}"\n[+] You have to specify target name with 't' argument.${RESET}\n"
else
	@$(DK) history $(t)
endif

find: ##@Show Searching Docker Hub. t=<distributor> g=<image>
ifeq ($(t), )
	@echo ${YELLOW}"\n[+] You have to specify search name with 't' argument.${RESET}\n"
else
ifeq ($(g), )
	@$(DK) search --no-trunc --format "table {{.Name}} [ {{.StarCount}} ]\t{{.Description}}" $(t)
else
	@curl -s https://registry.hub.docker.com/v1/repositories/$(t)/$(g)/tags | sed "s/,/\n/g" | grep name | cut -d '"' -f 4
endif	
endif

# Enter Into Container For Manage -------------------------------------------
in: ##@Manage Enter into running container. t=<container name>
	@$(DK) exec --privileged -it $(t) /bin/bash

inother: ##@Manage Create new container & into the container. t=<container name>
	@$(DC) -f $(DCF) run --rm $(t) bash

# Cleaning Images And Containers --------------------------------------------
rm: rmcon rmimg ##@Manage Remove All. t=<image/container name, none, all>

rmimg: ##@Manage Remove Image. t=<name, none, all>
ifeq ($(t), )
	@$(DK) image rm -f $(shell $(DC) -f $(DCF) config --services)
else ifeq ($(t), none)
	@$(DK) image rm -f $(shell $(DK) image ls -f "dangling=true" -q) 2>/dev/null; true
else ifeq ($(t), all)
	@$(DK) image rm -f $(shell $(DK) image ls -q) 2>/dev/null; true
else
	@$(call fun_imgrm, $(t); exit 0) 2>/dev/null; true
endif

rmcon: ##@Manage Remove Container. t=<container name, none, all>
ifeq ($(t), )
	@$(DC) -f $(DCF) rm -f -s $(shell $(DC) -f $(DCF) config --services)
else ifeq ($(t), none)
	@$(DK) container rm -f $(shell $(DK) container ps -a -q -f "status=exited") 2>/dev/null; true
else ifeq ($(t), all)
	@$(DK) container stop $(shell $(DK) container ls -aq) 2>/dev/null; true
	@$(DK) container rm -f $(shell $(DK) container ls -aq) 2>/dev/null; true
else
	@$(call fun_conrm, $(t); exit 0) 2>/dev/null; true
endif

## Working With Private Hub
help: ##@Other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

hub: ##@Other All list of private registry
	@curl -X GET http://$(HUB)/v2/_catalog

hubtag: ##@Other Tags List of t=<image name>
	@curl -X GET http://$(HUB)/v2/$(t)/tags/list

v ?= latest
push: ##@Other Push to private registry. t=<image name> n=<hub name> v=<version>
	@$(DK) tag $(t) $(HUB)/$(n):$(v)
	@$(DK) push $(HUB)/$(n):$(v)
	@$(DK) image rm $(HUB)/$(n):$(v)
