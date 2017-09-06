# Conditions for Makefile

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
