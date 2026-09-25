# Research Design

## Systems engineering framing

NASA describes Technical Performance Measures as key performance parameters monitored by comparing current achievement or best estimates with anticipated current and future values so emerging deficiencies can be identified before requirements are jeopardized.

This repository applies that logic in a narrow laboratory case study.

Measured discharge capacity is treated as a performance parameter. The NASA 1.4 Ah end of life criterion is treated as a requirement like boundary. The study then examines both current margin and the stability of a projected boundary crossing.

## Important terminology boundary

This is a **TPM style laboratory application**.

It does not claim that battery capacity alone is a complete system level Technical Performance Measure or that the four cells represent an operational NASA project TPM program.

## Unit of analysis

A discharge cycle nested within one of four NASA cells:

- B0005;
- B0006;
- B0007;
- B0018.

## Evidence timing

Every cell is censored at the same checkpoints:

- cycle 40;
- cycle 60;
- cycle 80.

Only observations at or before the checkpoint enter the forecast.

Later observations enter evaluation only.

## Why fixed checkpoints matter

A checkpoint that is calculated as a percentage of eventual lifetime requires knowledge unavailable at the monitoring decision time.

Fixed checkpoints can be selected without observing the future trajectory.

## Forecast model

A transparent OLS line is fitted to capacity versus discharge cycle.

The line is projected to the 1.4 Ah boundary if slope is negative.

The model is intentionally simple so forecast revision and failure modes remain interpretable.

## Outcome structure

B0005, B0006, and B0018 have observed crossings.

B0007 does not cross 1.4 Ah within the released observation horizon and is treated as right censored for crossing time.

## Evaluation layers

1. **current state:** capacity and margin at checkpoint;
2. **forecast:** projected threshold cycle;
3. **maturity:** forecast revision from prior checkpoint;
4. **realized accuracy:** signed and absolute crossing error where outcome exists;
5. **warning validity:** false early warning for non crossing cells when projection enters the recorded horizon.

## Inference scope

The release supports descriptive statements about the four cells and the transparent model.

It does not support calibrated uncertainty, cross chemistry generalization, causal inference, or production battery management decisions.
