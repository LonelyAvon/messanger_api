deploy:
	sudo docker compose --env-file .env.deploy -f docker/docker-compose.yml --project-directory . up --build -d

install:
	poetry install

dev: install db
	poetry run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 10421 --reload
db:
	docker compose --env-file .env.develop -f docker/docker-compose-dev.yml --project-directory . up --build -d

revision:
	poetry run alembic revision --autogenerate

upgrade:
	poetry run alembic upgrade head

# logs:
# 	docker logs --tail 10 -f Qrget_api

