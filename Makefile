run:
	@uvicorn main:app --reload

create-migrtions:
	@alembic revision --autogenerate -m $(d)

run-migrations:
	@alembic upgrade head
