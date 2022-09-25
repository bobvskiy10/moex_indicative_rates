REQ  = requirments.txt
VENV ?= .venv

ifeq ($(OS), Windows_NT)
	BIN_PATH = $(VENV)/Scripts
else
	BIN_PATH = $(VENV)/bin
endif
CODE = moex_rates

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	$(BIN_PATH)/python -m pip install -U pip
	$(BIN_PATH)/python -m pip install -Ur $(REQ)

.PHONY: run
run:
	$(BIN_PATH)/python -m $(CODE)

.PHONY: clean
clean:
	rm -r $(VENV)
