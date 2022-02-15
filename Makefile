SHELL := /bin/bash

.PHONY: reflair
reflair: venv
	date
	./venv/bin/python src/reflair_posts.py

.PHONY: flairy
flairy: venv
	./venv/bin/python src/flairy.py

.PHONY: test
test: venv
	./venv/bin/pytest tests/test_flairy.py

venv: venv/touchfile

venv/touchfile: requirements.txt
	echo "###########################################"
	echo "Setting up virtualenv with dependencies..."
	echo "###########################################"
	python3 -m pip install virtualenv
	echo $(shell which python3.8)
	python3 -m virtualenv -p $(shell which python3.8) venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r "requirements.txt"
	touch venv/touchfile

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
