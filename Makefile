init:
	alembic init -t async migrations

makemigrations:
	alembic revision  --autogenerate -m 'initial commit'

up:
	alembic upgrade head

down:
	alembic downgrade

current-mig:
	alembic current

flake8:
	flake8 .

isort:
	isort .

black:
	black .