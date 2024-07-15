deploy:
	sudo docker-compose -f docker/docker-compose.yml --project-directory . up --build

install:
	poetry install

dev: install
	poetry run uvicorn app.api.main:app --host 0.0.0.0 --port 10000 --reload
