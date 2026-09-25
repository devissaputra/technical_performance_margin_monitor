# Released Results

The release separates four evidence layers:

1. complete cycle level capacity evidence;
2. observed cell level threshold outcomes;
3. fixed checkpoint forecasts and revisions;
4. aggregate forecast maturity summaries.

## Authoritative result files

- `data/derived/battery_summary.csv`
- `data/derived/checkpoint_results.csv`
- `data/derived/checkpoint_aggregate.csv`
- `results/empirical_summary.json`

## Headline interpretation

Across the three cells with observed 1.4 Ah crossings, mean absolute threshold cycle error decreases from 102.399 at checkpoint 40 to 35.852 at 60 and 11.942 at 80.

This aggregate pattern must be interpreted with cell level evidence. B0006 becomes less accurate across the released checkpoints while B0005 improves strongly.

B0007 has no observed crossing through cycle 168 and produces a false early warning at checkpoint 80.

## Boundary

Forecast revision is a descriptive stability measure, not calibrated uncertainty.

The released figures and narrative should remain synchronized with these result files.
