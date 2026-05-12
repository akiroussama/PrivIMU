.PHONY: install test download train-rf train-cnn demo evaluate clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev,app]"

test:
	pytest -q

download:
	python data/download.py --dest data/raw/motionsense

train-rf:
	python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir . --window-size 50 --step-size 25 --n-splits 5

train-cnn:
	python -m privimu.train --data-root data/raw/motionsense --model cnn --output-dir . --window-size 50 --step-size 25 --n-splits 5

evaluate:
	python -m privimu.evaluate --metrics reports/metrics.json

demo:
	streamlit run streamlit_app.py

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
