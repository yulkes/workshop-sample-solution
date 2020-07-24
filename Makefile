all: run_docker

.PHONY: clean
clean:
	rm -rf .venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

.venv:
	virtualenv --python=python3.8 .venv && .venv/bin/pip install -r requirements.txt

.PHONY: run
run: .venv
	FLASK_ENV=development FLASK_APP=webapp IFS_SETTINGS=../settings.cfg .venv/bin/flask run

# Docker comands
app_name = ifs_webapp

.PHONY: build
build:
	docker build -t "$(app_name):latest" .

.PHONY: run_docker
run_docker: kill build
	docker run -d -p 5000:5000 \
	-e "FLASK_APP=webapp" -e "FLASK_ENV=development" -e "IFS_SETTINGS=../settings.cfg" \
		--rm --name $(app_name) $(app_name)

.PHONY: kill
kill:
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker kill

# Testing

.PHONY: test
test: .venv
	IFS_SETTINGS=../settings.cfg .venv/bin/python -m pytest -s "tests"

end_to_end_test: .venv run_docker
	sleep 3 && .venv/bin/python end_to_end_test.py

# Submission

PYTHON_FILES = $(shell find ifs tests -name '*.py')
PROJECT_FILES = README.md MANIFEST.in settings.cfg requirements.txt webapp.py Makefile
dist/home_assignment.zip: .venv test end_to_end_test
	mkdir -p dist && zip -FSr dist/home_assignment.zip $(PYTHON_FILES) $(PROJECT_FILES)

.PHONY: zip
zip: dist/home_assignment.zip
