# Research Design

## Research question
How well can a transparent early-life capacity trend anticipate a 1.4 Ah end-of-life threshold without training on observations at or beyond that threshold?

## Design
Secondary prognostics analysis of laboratory battery aging time series.

## Source and unit of analysis
Source: NASA Ames PCoE Li-ion Battery Aging Dataset (B0005, B0006, B0007, B0018). The operational unit follows the public dataset and is documented in `data/source_manifest.json` and `docs/data_dictionary.md`.

## Hypotheses
1. H1: an early-life linear capacity trend can provide a useful but imperfect threshold-crossing baseline.
2. H2: forecast error varies materially across cells, revealing trajectory heterogeneity that a single deterministic trend does not capture.
3. H3: a model may predict an early threshold crossing that the observed series does not realize, providing a concrete false-warning case.

## Method
For each battery, use discharge capacity as the technical performance measure and define margin = capacity − 1.4 Ah. Fit ordinary least squares capacity versus discharge index using only the first 60% of that battery’s observed cycles, then project the 1.4 Ah crossing and compare it with the first observed crossing when one exists. The 60% cutoff keeps every observed crossing outside the training window.

## Validity boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.
