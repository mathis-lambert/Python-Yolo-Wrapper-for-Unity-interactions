install:
	pip install -e .

test:
	pytest

run:
	python -m pywui.main

build:
	python -m build

clean:
	rm -rf build dist

.PHONY: install test run build clean
