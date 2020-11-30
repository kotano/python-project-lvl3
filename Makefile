package-install:
	poetry install

build:
	poetry build

test:
	poetry run pytest -vv --strict --cov --cov-report xml

lint:
	poetry run flake8 gendiff

check: lint
	pytest -vv --strict