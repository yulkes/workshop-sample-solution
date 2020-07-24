all: run

.PHONY: clean
clean:
	rm -rf .venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

.venv:
	virtualenv --python=python3.8 .venv && .venv/bin/pip install -r requirements.txt

.PHONY: clean
run: .venv
	FLASK_ENV=development FLASK_APP=webapp IFS_SETTINGS=../settings.cfg .venv/bin/flask run

.PHONY: clean
test: .venv
	IFS_SETTINGS=../settings.cfg .venv/bin/python -m pytest -s "tests"

.PHONY: clean
sdist: .venv test
	.venv/bin/python setup.py sdist

PYTHON_FILES = $(shell find ifs tests -name '*.py')
PROJECT_FILES = README.md MANIFEST.in settings.cfg requirements.txt webapp.py Makefile
dist/home_assignment.zip: .venv test
	mkdir -p dist && zip -FSr dist/home_assignment.zip $(PYTHON_FILES) $(PROJECT_FILES)

.PHONY: zip
zip: dist/home_assignment.zip

