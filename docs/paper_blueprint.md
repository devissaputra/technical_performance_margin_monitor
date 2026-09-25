# Paper Blueprint

## Working title
Technical Performance Margin Monitoring on NASA Li-ion Battery Aging Data

## Motivation
Technical performance measures are useful only when forecasts are made before the threshold event they are meant to anticipate. The NASA battery trajectories create a concrete leakage test: project a 1.4 Ah threshold from early-life observations and compare that projection with later observed crossings.

## Research question
How well can a transparent early-life capacity trend anticipate a 1.4 Ah end-of-life threshold without training on observations at or beyond that threshold?

## Data and method
For each battery, use discharge capacity as the technical performance measure and define margin = capacity − 1.4 Ah. Fit ordinary least squares capacity versus discharge index using only the first 60% of that battery’s observed cycles, then project the 1.4 Ah crossing and compare it with the first observed crossing when one exists. The 60% cutoff keeps every observed crossing outside the training window.

## Results to report
Using only the first 60% of each history, the linear baseline is 5.5 cycles late for B0005, 10.1 cycles early for B0006, and 0.2 cycles late for B0018. For B0007 it predicts a crossing near cycle 150 even though observed capacity remains above 1.4 Ah through cycle 168, a false early threshold prediction. Report the packaged headline metrics and the full relevant derived table; do not cherry-pick only the strongest contrast.

## Robustness / sensitivity
The 60% training cutoff is checked battery by battery so that every observed 1.4 Ah crossing used for evaluation occurs after the training window. Results are reported separately for B0005, B0006, B0007, and B0018 instead of pooling away cell heterogeneity. B0007 is retained as a false-warning case because its projected crossing occurs within the observed horizon while the measured capacity never reaches 1.4 Ah.

## Limitations
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.

## Publication integrity
Do not describe this repository as peer reviewed, preregistered, or externally validated unless those events actually occur. Distinguish analysis of public data from original data collection.
