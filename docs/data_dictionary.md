# Data Dictionary

## Provenance
See `data/source_manifest.json`. Raw source observations are not silently republished.

## `data/derived/primary_results.csv`
All four cells in the convenience discharge-capacity table, with the training-window endpoint shown explicitly.

## `data/derived/secondary_results.csv`
When present and non-empty, this contains a second derived table needed to reproduce a reported comparison. If empty, no second packaged table is required.

## `results/empirical_summary.json`
Machine-readable headline sample sizes, estimates, and the release finding. Values must agree with README text and the derived CSVs.

## Construct boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.
