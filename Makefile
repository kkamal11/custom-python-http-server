VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

install:
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py examples.flask_app:app

run-workers:
	$(PYTHON) main.py examples.flask_app:app --workers 4

clean:
	rm -rf $(VENV)
