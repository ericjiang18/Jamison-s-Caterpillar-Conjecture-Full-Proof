# Mean subtree order and caterpillar maximizers
## Journal-style review manuscript and reproducibility package

`main.pdf` is the complete 28-page journal-style manuscript. `main.tex` is its
editable LaTeX source, using the standard `amsart` class. Eight vector figures,
four tables, the complete mathematical argument, the cherry-case appendix, and
twelve bibliography entries are included.

## Mathematical status

This is a complete **written computer-assisted proof candidate**, not a confirmed
resolution of Jamison's conjecture. Fresh execution of the supplied verifier and
finite graph tests is reported accurately; rerunning the same code does not
independently validate the mathematical specification. No human referee report,
journal acceptance, or complete Lean proof is claimed. The earlier Lean attempt
is partial and was not compiler-checked; its status record is included for clarity.

The graphs display finite computed quantities. They are not evidence establishing
an unbounded theorem by themselves. Proof obligations and computational trust
boundaries are distinguished in the abstract, introduction, and Section 6.

## Compile the paper

In Overleaf, upload this ZIP as a project, select `main.tex`, and use pdfLaTeX.
The PDF figures are already provided: Overleaf does not need to execute Python.
No shell escape, Internet access, or custom font files are required for compilation.
A local installation can build with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The bibliography is embedded in `main.tex` so it compiles without a BibTeX step.
`references.bib` is also provided for later conversion to a journal's bibliography
style. Author names, affiliations, and contact information are intentionally unset;
edit the commented author fields in `main.tex` with the appropriate information.
The manuscript is not branded as an accepted article from any particular journal.

## Reproduce the calculations

The fresh run used Python 3.13.5, SymPy 1.14.0, NetworkX 3.6.1, and Matplotlib 3.10.8.
The latter three packages are pinned in `requirements.txt`.

```sh
python -m pip install -r requirements.txt
python verification/verify_jamison_all_orders.py --part all --output-dir fresh_checks
python analysis/run_experiments.py --max-order 17 --output-dir data
python analysis/plot_results.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Do not use Python's `-O` flag during verification. Execution time is machine-dependent;
the recorded elapsed times are measurements of this run, not performance guarantees.
The third and fourth commands regenerate the finite data and the eight figures.
They do not rewrite the tabulated manuscript text automatically. At the supplied
maximum order and seed, the mathematical data match the included manuscript.
Changing the scope of an experiment requires corresponding editorial updates.

The original verifier also supports `--part even`, `odd`, `boundary`, `stars`,
`base`, and `tests`, allowing its phases to be run separately.

## Contents

- `main.tex`, `main.pdf`: journal-style manuscript and compiled result.
- `references.bib`: twelve publication/problem-page/software references.
- `figures/`: eight vector PDF figures and PNG previews.
- `verification/`: the supplied exact verifier, graph transformation routines,
  and cherry-base verifier. These three Python files have not been modified.
- `verification/checks/`: freshly generated polynomial certificates, the
  successful run result, exit code, and execution log.
- `analysis/run_experiments.py`: the new finite experiment driver. It independently
  recounts input and returned graphs using an iterative root-deletion calculation,
  and uses exhaustive subset connectivity for the two illustrative graph pairs.
  Its transformation selection still calls the supplied graph routine, so this
  is implementation-level cross-checking, not an independent proof.
- `analysis/plot_results.py`: regenerates all eight figures from exact saved data.
  Rational numbers are converted to floating point only for plotting.
- `data/experiments.json`: per-order exact extrema, exact gain summaries, full
  adjacency lists and subtree-order distributions for the examples, timing,
  versions, and source-code hashes.
- `data/noncaterpillar_moves.csv`: 64,497 source/competitor records, including
  graph6 encodings, case classification, exact moments, and rational improvements.
- `data/enumeration_summary.csv`: exact per-order values underlying the main plots.
- `data/*_distribution.csv`: exact counts and probabilities for the two examples.
- `data/certificate_reproduction.json`: all five regenerated certificate files
  are byte-for-byte identical to the supplied versions.
- `data/equation_preservation.json`: all 158 display-math blocks in the preceding
  cited LaTeX manuscript are retained verbatim up to whitespace. The new edition
  has 161 display blocks, adding three empirical definitions in Section 6.
- `data/publication_checks.json`: compilation, document preflight, and fresh-run
  summaries. These are editorial/reproducibility checks, not theorem certification.
- `provenance/`: the supplied all-order manuscript, its earlier LaTeX edition with
  references, and the partial Lean status record.
- `MANIFEST.sha256`: integrity hashes of the delivered project files. File hashes
  establish integrity, not mathematical correctness.

## Fresh executed results

The full supplied exact verifier exited with code zero. Its five certificate files
matched the supplied counterparts. The finite experiment driver also exited with
code zero and enumerated every unlabeled tree of orders 4 through 17: 81,134 trees,
including 16,637 caterpillars and 64,497 non-caterpillars. Each non-caterpillar had
a returned same-order tree with a strictly larger mean, decided by exact integer
cross-multiplication. Every observed maximizer in this finite range was a caterpillar.

The two graph-pair examples were additionally checked by testing every nonempty
vertex subset for connectivity, for a total of 1,310,716 subset tests. Their full
subtree-order sequences appear in Table 4 and the data files. The enumeration through
17 does not extend the larger historical order-24 computation cited in the paper.

## Editorial changes relative to the supplied manuscript

The mathematical sections and their equation tags are retained. The presentation
uses AMS article styling, a concise abstract and introduction, an updated Section 6,
actual-graph illustrations, and a new computational appendix. The original two exact
example-score displays are retained. Known results keep their bibliographic attribution.
The new enumeration and plots are labeled as fresh finite computations. No mathematical
gap has been silently filled, and no new independent proof audit is claimed.
