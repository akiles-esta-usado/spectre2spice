# In some systems there is only python or python3, not both.
ifneq (,$(shell which python))
#$(info Using python)
PYTHON=python
else ifneq (,$(shell which python3))
#$(info Using python3)
PYTHON=python3
else
$(error python not in path)
endif

RM=rm -rf


all: venv


.PHONY: venv
venv:
	$(RM) .venv
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && $(PYTHON) -m pip install -e .


.PHONY: test
test:
	. .venv/bin/activate && spectre2spice example/ex1/ my_top.scs output/ex1/ example/ex1/tech_example/ --log_path logs/


.PHONY: clear
clear:
	$(RM) logs output