install:
	pip install --force-reinstall -r requirements.txt
	pip install -e .

test:
	pytest

run:
	python scripts/main.py

clean:
	rm -rf build dist

.PHONY: install clean
