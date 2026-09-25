# Analysis Plan

## Status

This document describes the corrected released analysis. It is not a preregistration.

## Decision problem

At a fixed monitoring checkpoint, estimate when the measured battery capacity margin would reach the NASA 1.4 Ah boundary and quantify how that estimate changes as more evidence becomes available.

## Scientific correction

The former first 60% of final history rule depended on the eventual recorded observation horizon.

The released protocol replaces that retrospective rule with common fixed checkpoints at cycles 40, 60, and 80.

## Unit of analysis

A discharge cycle nested within one of four battery cells.

## Primary cell level outputs

For each battery and checkpoint:

- last observed capacity;
- current margin to 1.4 Ah;
- fitted OLS slope;
- projected threshold crossing cycle;
- observed crossing cycle when available;
- signed projection error;
- absolute projection error;
- forecast revision from the previous checkpoint;
- whether the projection lies inside the recorded horizon;
- false early warning flag for no crossing cells.

## Aggregate outputs

For each checkpoint:

- mean absolute crossing cycle error across cells with observed crossings;
- median absolute crossing cycle error;
- mean absolute forecast revision across all cells with a previous forecast;
- false early warning count.

## Right censored outcome

B0007 has no observed 1.4 Ah crossing through cycle 168.

No artificial crossing cycle is imputed.

## Interpretation rule

Aggregate MAE is never interpreted alone. Cell level forecasts and median error are reported because the mean can be dominated by a large individual error.

Forecast revision is interpreted as descriptive evidence of forecast stability. It is not a calibrated uncertainty interval or probability of failure.

## Released figures

1. observed capacity trajectories with threshold and checkpoints;
2. fixed checkpoint processing pipeline;
3. cell level absolute threshold cycle errors;
4. per cell forecast revision;
5. evidence and claim boundary.

## Change control

Any future change to the threshold, checkpoints, model family, crossing definition, error metric, or source cells should be released as a new analysis version rather than silently replacing this protocol.
