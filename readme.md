create migration = docker-compose exec user alembic revision --autogenerate -m "comment"
apply migration = docker-compose exec user alembic upgrade head