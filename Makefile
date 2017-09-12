# Makefile to ease trivial tasks for the project

include conditions.mk
VENV="$(shell find . -name ".*env")"
INVENV="$(shell which python | grep ${VENV})"
REQ="requirements.txt"


.PHONY: installenv
installenv:
	# install the virtual environment
	@test -d ${VENV} && virtualenv ${VENV} || virtualenv .venv


.PHONY: init
init: req-venv
	# upgrade PIP on virtual environment
	@pip install -U pip && pip install -r ${REQ}


.PHONY: init-getresume
init-getresume: req-venv req-pass
	# installs getresume and configures Tor and Privoxy
	@echo $(contents)
	@make getresume PASSWORD=${PASSWORD}


.PHONY: update
update: req-venv
	# update PIP requirements
	@pip freeze | grep -Eiv "pkg-resources|getresume" > ${REQ}


.PHONY: test
test: req-venv
	# run backend unit tests with nose
	@nosetests -v -w tests


.PHONY: clean-all
clean-all: clean reset


.PHONY: clean
clean:
	# clean out cache and temporary files
	@find . \( -name "*.pyc" -type f -o -name "__pycache__" -type d \) -delete
	@find . \( -name "resume*" -o -name "*_results.json" \) -type f -delete


.PHONY: reset
reset:
	# remove distribution and raw data files
	@find . \( -path "./corpus/*" -o -path "./dist/*" -o -path "./data/*" -o \
		-path "./*resume.txt" \) -delete
	@find . \( -path "./corpus" -o -path "./dist" -o -path "./data" \) -empty \
		-delete
