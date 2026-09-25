# Empirical Study Protocol

## Study title

**Forecast Maturity of Technical Performance Margin on NASA Li-ion Battery Aging Data**

## Study type

Secondary fixed checkpoint analysis of four NASA laboratory battery aging trajectories.

This document records the released protocol. It is not a preregistration.

## Research questions

**RQ1.** How does projected margin exhaustion timing change at cycles 40, 60, and 80?

**RQ2.** How does threshold cycle forecast error change as the checkpoint advances?

**RQ3.** Are aggregate improvements consistent across individual batteries?

**RQ4.** Can a projected crossing enter the recorded horizon without an observed crossing?

## Source

NASA Ames Prognostics Center of Excellence Battery Data Set.

Cells:

- B0005
- B0006
- B0007
- B0018

## Performance parameter

Measured discharge capacity in ampere hours.

NASA end of life boundary:

```text
1.4 Ah
```

Margin:

```text
measured capacity - 1.4 Ah
```

This is a laboratory TPM style application rather than a claim that capacity is a complete system level Technical Performance Measure.

## Fixed checkpoint rule

Every battery is evaluated at discharge cycles 40, 60, and 80.

Checkpoint selection does not use eventual threshold cycle, final lifetime, or future observations.

## Forecast rule

At each checkpoint:

1. use only capacity values from cycle 1 through the checkpoint;
2. fit ordinary least squares capacity versus discharge cycle;
3. if slope is negative, solve the fitted line for 1.4 Ah;
4. retain later observations only for evaluation.

## Observed outcome

For B0005, B0006, and B0018, the observed threshold cycle is the first recorded discharge cycle with capacity at or below 1.4 Ah.

B0007 does not cross within its 168 recorded cycles and remains right censored for threshold timing in this release.

## Forecast error

For cells with observed crossings:

```text
signed error = projected threshold cycle - observed threshold cycle
absolute error = |signed error|
```

Positive signed error is late. Negative signed error is early.

## Forecast revision

For consecutive checkpoints:

```text
revision = |new projected threshold cycle - previous projected threshold cycle|
```

Revision is treated as a descriptive maturity signal. It is not a probability interval.

## False early warning

For a non crossing cell, a false early warning is flagged when the projected threshold cycle lies within the recorded observation horizon but no threshold crossing is observed.

## Aggregate outputs

At each checkpoint:

- mean absolute error across cells with observed crossings;
- median absolute error across those cells;
- mean forecast revision where a previous checkpoint exists;
- false early warning count.

## Released findings

Across crossing cells, MAE is:

- 102.399 cycles at checkpoint 40;
- 35.852 at checkpoint 60;
- 11.942 at checkpoint 80.

Mean revision is:

- 100.046 cycles from 40 to 60;
- 38.012 cycles from 60 to 80.

Cell level behavior is heterogeneous. B0006 becomes less accurate across the released checkpoints even as the aggregate MAE improves.

B0007 generates a false early warning at checkpoint 80 with projected crossing 158.219 and no observed crossing through 168.

## Correction from prototype

The prototype used the first 60% of final recorded history. Because that cutoff depends on knowing the future horizon, it is not suitable for a prospective decision interpretation.

The released fixed checkpoint design removes that dependency.

## Validity boundary

The linear model is intentionally transparent and weak.

The study does not estimate calibrated uncertainty, generalize across chemistries, or validate a production battery management system.
