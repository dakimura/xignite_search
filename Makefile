
lint:
	flake8 --exclude=.tox,venv

test:
	python ./tests/runner.py tests

run:
	python ./xignite_search/main.py

build:
	docker build -t dakimura/xignite_search .