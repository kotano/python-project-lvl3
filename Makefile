package-install:
	poetry install

build:
	poetry build

test:
	poetry run pytest -vv --strict --cov --cov-report xml

lint:
	poetry run flake8 page_loader

check: lint
	pytest -vv --strict