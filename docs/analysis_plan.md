# Analysis Plan

## Status
This file documents the analysis released in this repository. It is **not a preregistration** and should not be described as one.

## Primary estimand / descriptive target
How well can a transparent early-life capacity trend anticipate a 1.4 Ah end-of-life threshold without training on observations at or beyond that threshold?

## Analysis
For each battery, use discharge capacity as the technical performance measure and define margin = capacity − 1.4 Ah. Fit ordinary least squares capacity versus discharge index using only the first 60% of that battery’s observed cycles, then project the 1.4 Ah crossing and compare it with the first observed crossing when one exists. The 60% cutoff keeps every observed crossing outside the training window.

## Specified outputs for this release
1. source/sample size and provenance;
2. primary derived metric(s);
3. comparator, cross-group, cross-time, or frontier contrast where applicable;
4. uncertainty, sensitivity, or error information supported by the source;
5. explicit construct and external-validity limitations.

## Missingness / exclusions

All 636 discharge-capacity records in the processed NASA series are used. Trend fitting uses only the first 60% of each battery history. B0007 has no observed 1.4 Ah crossing through its final recorded cycle, so observed EOL remains missing rather than being extrapolated.

## Interpretation boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.
