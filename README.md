# Mean subtree order and caterpillar maximizers

`main.pdf` is the complete 28-page manuscript. 

## Questions

For every integer n ≥ 1, every tree on n vertices maximizing the mean order of its nonempty connected induced vertex subsets is a caterpillar. Consequently, for every n, a caterpillar attains the maximum mean subtree order among all n-vertex trees. 

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

## Contents

- `main.tex`, `main.pdf`:  manuscript and compiled result.
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

