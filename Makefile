install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app run

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

selfcheck:
	poetry check

check: selfcheck test lint

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app