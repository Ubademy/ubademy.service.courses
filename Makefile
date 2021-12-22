POETRY=poetry
PYTEST=$(POETRY) run pytest --cache-clear --cov=app tests/ --cov-report=xml > pytest-coverage.txt
MYPY=$(POETRY) run mypy --ignore-missing-imports
BLACK=$(POETRY) run black
ISORT=$(POETRY) run isort
PYLINT=$(POETRY) run pylint
UVICORN=$(POETRY) run uvicorn
PACKAGE=app

install:
	$(POETRY) install
	$(POETRY_EXPORT)

update:
	$(POETRY) update
	$(POETRY_EXPORT)

test: install
	$(PYTEST) -vv

fmt:
	$(ISORT) ./${PACKAGE} ./tests ./routers ./main.py
	$(BLACK) ./${PACKAGE} ./tests ./routers ./main.py

lint: fmt
	$(MYPY) ./${PACKAGE}/ ./routers ./main.py
	$(PYLINT) ./${PACKAGE} ./routers ./main.py

reset:
	$ docker rm dbcourses
	$ docker-compose up --build

run:
	$ docker-compose up --build

checks: lint test

all: checks reset

