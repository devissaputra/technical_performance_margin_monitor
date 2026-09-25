# Data Dictionary

## `cycle_capacity_evidence.csv`
Complete derived cycle-level evidence for the four selected NASA cells:
- `battery`
- `discharge_cycle`
- `capacity_ah`
- `margin_to_1_4_ah`

No charge/EIS waveforms or other raw NASA fields are redistributed.

## `battery_summary.csv`
Cell-level cycle counts, first/final capacity, final margin, and first observed ≤1.4 Ah cycle.

## `checkpoint_results.csv`
One row per battery × checkpoint (12 rows) containing current margin, fitted slope, projected crossing cycle, observed crossing, signed error, forecast revision, horizon flag, and false-warning flag.

## `checkpoint_aggregate.csv`
Checkpoint-level MAE, median absolute error, mean forecast revision, and false-warning count.

## Source
All packaged evidence is checked by the official NASA-source rebuild.
