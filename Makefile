test:
	pytest -q

demo:
	python run_demo.py

figures:
	python scripts/generate_figures.py

source-check:
	python scripts/fetch_and_analyze.py --check
