.PHONY: all help compose-up compose-restart


all: help

help:
	@echo "Usage: make [target]"
	@echo "\nTargets:\n"
	@echo "  compose-up      - Start Docker Compose services"
	@echo "  compose-restart - Restart Docker Compose services"
	@echo "  help            - Show this help message"

.clear:
	@clear

compose-up:.clear
	@docker compose --project-directory .docker up --build --quiet-pull -d

compose-restart:.clear
	@docker compose --project-directory .docker restart
