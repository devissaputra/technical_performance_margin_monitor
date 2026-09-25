# Data Dictionary

## `data/derived/cycle_capacity_evidence.csv`

Complete 636 row derived cycle level evidence.

Columns:

- `battery`: one of B0005, B0006, B0007, B0018;
- `discharge_cycle`: sequential discharge cycle index within the extracted NASA cell record;
- `capacity_ah`: measured discharge capacity in ampere hours;
- `margin_to_1_4_ah`: `capacity_ah - 1.4`.

The repository does not redistribute charge waveforms, impedance spectra, temperatures, voltages, or the original MATLAB files.

## `data/derived/battery_summary.csv`

One row per battery with:

- number of discharge cycles;
- first capacity;
- final capacity;
- final margin;
- first observed discharge cycle at or below 1.4 Ah.

A blank crossing field means no crossing was observed within the packaged horizon.

## `data/derived/checkpoint_results.csv`

One row per battery by checkpoint, for 12 rows total.

Columns:

- `battery`;
- `checkpoint_cycle`;
- `last_observed_capacity_ah`;
- `margin_to_1_4_ah`;
- `slope_ah_per_cycle`;
- `projected_threshold_cycle`;
- `observed_threshold_cycle`;
- `projection_error_cycles`;
- `forecast_revision_cycles`;
- `projection_within_observed_horizon`;
- `false_early_warning`.

### Error sign

```text
projection error = projected threshold cycle - observed threshold cycle
```

Positive means the forecast is late.

Negative means the forecast is early.

## `data/derived/checkpoint_aggregate.csv`

Checkpoint level summaries:

- mean absolute error across crossing cells;
- median absolute error across crossing cells;
- mean absolute revision from the previous checkpoint;
- false early warning count.

## `results/empirical_summary.json`

Machine readable headline values used in the README and release validation.

## Source relationship

All packaged capacity values are checked against the official NASA archive during the empirical rebuild.
