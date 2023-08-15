up:
	cd temporalite ; docker-compose up -d
    cd python ; docker-compose up -d --scale python=3

down:
	cd temporalite ; docker-compose down
	cd python ; docker-compose down

restart:
	cd temporalite ; docker-compose restart
	cd python ; docker-compose restart

build:
	cd temporalite ; docker-compose up --build -d
	cd python ; docker-compose up --build -d

logs:
	cd temporalite ; docker-compose logs -f --tail=100
	cd python ; docker-compose logs -f --tail=100