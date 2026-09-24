.PHONY: pdf verify experiments figures clean

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

verify:
	python verification/verify_jamison_all_orders.py --part all --output-dir fresh_checks

experiments:
	python analysis/run_experiments.py --max-order 17 --output-dir data

figures:
	python analysis/plot_results.py

clean:
	latexmk -c main.tex
