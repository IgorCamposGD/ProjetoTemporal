pizzaria-up:
	cd temporalite ; docker-compose up -d
    cd python/workflow/ ; docker-compose up -d
	cd python/worker/ ; docker-compose up -d
