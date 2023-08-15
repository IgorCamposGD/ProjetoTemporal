up:
    cd python ; docker-compose up -d --scale python=3

down:
	cd python ; docker-compose down

restart:
	cd python ; docker-compose restart

build:
	cd python ; docker-compose up --build -d

logs:
	cd python ; docker-compose logs -f --tail=100