
build-image:
	docker build -t covid-vaccine-bot:latest .

pull:
	docker-compose pull

run:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f
