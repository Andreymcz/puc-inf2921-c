# PoC lifecycle commands — run from tttc-poc/
# Usage: make <target>

COMPOSE = docker compose

# --------------------------------------------------------------------------- #
# Status & info
# --------------------------------------------------------------------------- #

.PHONY: status
status:
	@echo "=== Services ==="
	$(COMPOSE) ps
	@echo ""
	@echo "=== Images ==="
	$(COMPOSE) images

.PHONY: logs
logs:
	$(COMPOSE) logs --tail=50

.PHONY: logs-follow
logs-follow:
	$(COMPOSE) logs -f

.PHONY: logs-next
logs-next:
	$(COMPOSE) logs -f next-client

.PHONY: logs-express
logs-express:
	$(COMPOSE) logs -f express-server

.PHONY: logs-py
logs-py:
	$(COMPOSE) logs -f pyserver

# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

.PHONY: build
build:
	$(COMPOSE) build

.PHONY: build-next
build-next:
	$(COMPOSE) build next-client

.PHONY: build-express
build-express:
	$(COMPOSE) build express-server

.PHONY: build-pyserver
build-pyserver:
	$(COMPOSE) build pyserver

.PHONY: build-no-cache
build-no-cache:
	$(COMPOSE) build --no-cache

# --------------------------------------------------------------------------- #
# Run
# --------------------------------------------------------------------------- #

.PHONY: up
up:
	$(COMPOSE) up -d

.PHONY: up-next
up-next:
	$(COMPOSE) up -d next-client

.PHONY: up-build
up-build:
	$(COMPOSE) up -d --build

# --------------------------------------------------------------------------- #
# Stop & cleanup
# --------------------------------------------------------------------------- #

.PHONY: stop
stop:
	$(COMPOSE) stop

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: kill
kill:
	$(COMPOSE) kill

.PHONY: clean
clean:
	$(COMPOSE) down --volumes --remove-orphans
	$(COMPOSE) images -q | xargs -r docker rmi -f

# --------------------------------------------------------------------------- #
# Rebuild a single service without touching others
# --------------------------------------------------------------------------- #

.PHONY: rebuild-next
rebuild-next:
	$(COMPOSE) build next-client
	$(COMPOSE) up -d --no-deps next-client

.PHONY: rebuild-express
rebuild-express:
	$(COMPOSE) build express-server
	$(COMPOSE) up -d --no-deps express-server

.PHONY: rebuild-pyserver
rebuild-pyserver:
	$(COMPOSE) build pyserver
	$(COMPOSE) up -d --no-deps pyserver

# --------------------------------------------------------------------------- #
# Full cycle
# --------------------------------------------------------------------------- #

.PHONY: restart
restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

.PHONY: fresh
fresh:
	$(COMPOSE) down --volumes --remove-orphans
	$(COMPOSE) build
	$(COMPOSE) up -d

# --------------------------------------------------------------------------- #
# Ollama model management
# --------------------------------------------------------------------------- #

.PHONY: pull-model
pull-model:
	$(COMPOSE) exec ollama ollama pull llama3.2

.PHONY: list-models
list-models:
	$(COMPOSE) exec ollama ollama list

# --------------------------------------------------------------------------- #
# Help
# --------------------------------------------------------------------------- #

.PHONY: help
help:
	@echo "PoC lifecycle targets:"
	@echo ""
	@echo "  Status:"
	@echo "    make status          -- show running services and images"
	@echo "    make logs            -- tail last 50 lines from all services"
	@echo "    make logs-follow     -- follow logs from all services"
	@echo "    make logs-next       -- follow next-client logs"
	@echo "    make logs-express    -- follow express-server logs"
	@echo "    make logs-py         -- follow pyserver logs"
	@echo ""
	@echo "  Build:"
	@echo "    make build           -- build all services"
	@echo "    make build-next      -- build only next-client (fast iteration)"
	@echo "    make build-express   -- build only express-server"
	@echo "    make build-pyserver  -- build only pyserver"
	@echo "    make build-no-cache  -- full rebuild without Docker layer cache"
	@echo ""
	@echo "  Run:"
	@echo "    make up              -- start all services (detached)"
	@echo "    make up-build        -- build + start in one step"
	@echo "    make up-next         -- start only next-client"
	@echo ""
	@echo "  Stop:"
	@echo "    make stop            -- stop services (keep containers)"
	@echo "    make down            -- stop and remove containers"
	@echo "    make kill            -- force-kill all containers"
	@echo "    make clean           -- down + remove volumes + remove images"
	@echo ""
	@echo "  Rebuild single service:"
	@echo "    make rebuild-next      -- build + restart next-client only"
	@echo "    make rebuild-express   -- build + restart express-server only"
	@echo "    make rebuild-pyserver  -- build + restart pyserver only"
	@echo ""
	@echo "  Full cycle:"
	@echo "    make restart         -- down + up"
	@echo "    make fresh           -- clean slate: down+volumes, build, up"
	@echo ""
	@echo "  Ollama:"
	@echo "    make pull-model      -- pull llama3.2 into the ollama container"
	@echo "    make list-models     -- list models available in ollama"