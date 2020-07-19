all: run

clean:
	rm -rf .venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

.venv:
	virtualenv --python=python3.8 .venv && .venv/bin/python setup.py develop

run: .venv
	FLASK_ENV=development FLASK_APP=webapp IFS_SETTINGS=../settings.cfg .venv/bin/flask run

test: .venv
	IFS_SETTINGS=../settings.cfg .venv/bin/python -m pytest -s "tests"

sdist: .venv test
	.venv/bin/python setup.py sdist
