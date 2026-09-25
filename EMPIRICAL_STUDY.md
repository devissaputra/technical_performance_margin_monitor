# Empirical Study Protocol

## Study
Technical Performance Margin Monitoring on NASA Li-ion Battery Aging Data

## Research question
How well can a transparent early-life capacity trend anticipate a 1.4 Ah end-of-life threshold without training on observations at or beyond that threshold?

## Design and source
Secondary prognostics analysis of laboratory battery aging time series. Source: NASA Ames PCoE Li-ion Battery Aging Dataset (B0005, B0006, B0007, B0018). Analysis/retrieval date: 2026-09-25.

## Hypotheses
1. H1: an early-life linear capacity trend can provide a useful but imperfect threshold-crossing baseline.
2. H2: forecast error varies materially across cells, revealing trajectory heterogeneity that a single deterministic trend does not capture.
3. H3: a model may predict an early threshold crossing that the observed series does not realize, providing a concrete false-warning case.

## Operationalization and method
For each battery, use discharge capacity as the technical performance measure and define margin = capacity − 1.4 Ah. Fit ordinary least squares capacity versus discharge index using only the first 60% of that battery’s observed cycles, then project the 1.4 Ah crossing and compare it with the first observed crossing when one exists. The 60% cutoff keeps every observed crossing outside the training window.

## Primary empirical result
Using only the first 60% of each history, the linear baseline is 5.5 cycles late for B0005, 10.1 cycles early for B0006, and 0.2 cycles late for B0018. For B0007 it predicts a crossing near cycle 150 even though observed capacity remains above 1.4 Ah through cycle 168, a false early threshold prediction.

## Validity and claim boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.

## Reproducibility status
The repository packages derived results, study-specific analysis functions, deterministic or seeded procedures where relevant, an internet-enabled source rebuild script, and tests for both computations and critical scientific invariants. The released analysis was documented after dataset selection and should not be represented as preregistered.
