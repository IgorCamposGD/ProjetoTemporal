temporal-up:
	cd temporalite ; docker-compose up -d

python-up:
    cd python/workflow/ ; docker-compose up -d
	cd python/worker/ ; docker-compose up -d
