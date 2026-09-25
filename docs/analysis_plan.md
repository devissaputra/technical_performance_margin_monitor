# Analysis Plan

## Status
This document describes the corrected released analysis. It is **not a preregistration**.

## Correction from prototype
The former “first 60% of final history” training rule depended on the eventual observation horizon. The released protocol replaces it with fixed checkpoints at cycles 40, 60, and 80.

## Primary outputs
For each battery and checkpoint:
- current capacity and margin to 1.4 Ah;
- fitted linear slope;
- projected threshold-crossing cycle;
- signed projection error when an observed crossing exists;
- forecast revision from the preceding checkpoint;
- whether the projection lies within the recorded horizon;
- false-early-warning flag for non-crossing cells.

## Aggregate outputs
For each checkpoint:
- mean absolute crossing-cycle error across B0005, B0006, and B0018;
- median absolute error across those cells;
- mean forecast revision across all four cells when a previous checkpoint exists;
- false-early-warning count.

## Missing outcomes
B0007 has no observed 1.4 Ah crossing through cycle 168. No artificial EOL is imputed.

## Interpretation
Forecast revisions are descriptive evidence of model maturity/instability. They are not calibrated uncertainty intervals.
