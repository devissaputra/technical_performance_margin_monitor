# Research Bundle Definition

This repository is treated as a research bundle because it links one explicit research question to a named empirical source, a documented operationalization, executable analysis code, derived evidence, reproducibility checks, visual evidence, validity boundaries, and a paper-ready interpretation path.

## Question
How well can a transparent early-life capacity trend anticipate a 1.4 Ah end-of-life threshold without training on observations at or beyond that threshold?

## Empirical core
Leakage-aware early-history linear threshold forecasting.

## Main result
Using only the first 60% of each history, the linear baseline is 5.5 cycles late for B0005, 10.1 cycles early for B0006, and 0.2 cycles late for B0018. For B0007 it predicts a crossing near cycle 150 even though observed capacity remains above 1.4 Ah through cycle 168, a false early threshold prediction.

## Boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.

## Release criterion
A release passes only if source provenance, code, derived tables, JSON summary, README claims, figures, and tests agree numerically and semantically.
