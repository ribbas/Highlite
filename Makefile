# Makefile to ease trivial tasks for the project

VENV="$(shell find . -name ".*env")"
INVENV="$(shell which python | grep ${VENV})"
REQ="requirements.txt"


.PHONY: req-venv
# checks if virtual environment is activated and exits if it isn't 
req-venv:
ifeq (${INVENV}, "")
	$(error Virtual environment not activated)
endif

.PHONY: req-pass
# checks if PASSWORD is provided and exits if it isn't
req-pass:
ifndef PASSWORD
	$(error PASSWORD is not provided)
endif

EXTRA_INCLUDES:=$(wildcard getresume.mk)
# includes rules for installing getresume
ifneq ($(strip ${EXTRA_INCLUDES}),)
  contents:=$(shell echo including extra rules $(EXTRA_INCLUDES))
  include $(EXTRA_INCLUDES)
endif


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
	echo $(contents)
	@make getresume PASSWORD=${PASSWORD}


.PHONY: update
update: req-venv
	# update PIP requirements
	@pip freeze | grep -Eiv "pkg-resources|getresume" > ${REQ}


.PHONY: sdist
sdist: req-venv
	# compile source distribution
	@python setup.py sdist


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
	@find . -name "resume*" -type f -delete


.PHONY: reset
reset:
	# remove distribution and raw data files
	@find . \( -path "./corpus/*" -o -path "./dist/*" -o -path "./data/*" -o \
		-path "./*resume.txt" \) -delete
	@find . \( -path "./corpus" -o -path "./dist" -o -path "./data" \) -empty \
		-delete
