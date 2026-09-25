# Data Provenance and Derived Evidence

## Canonical source

NASA Ames Prognostics Center of Excellence Battery Data Set.

Official archive:

`https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip`

Cells used:

- B0005
- B0006
- B0007
- B0018

NASA documents a battery end of life criterion of 30% fade in rated capacity, from 2.0 Ah to 1.4 Ah.

## Raw file policy

The original NASA MATLAB files are not redistributed in this repository.

## Packaged evidence

### `derived/cycle_capacity_evidence.csv`

Complete 636 row capacity and margin table needed to reproduce the released forecasts offline.

### `derived/battery_summary.csv`

Four cell summary including observed first crossing where available.

### `derived/checkpoint_results.csv`

Twelve fixed checkpoint forecasts and evaluation fields.

### `derived/checkpoint_aggregate.csv`

Released aggregate error, median error, revision, and false warning metrics.

## Official source rebuild

Run:

```bash
python scripts/fetch_and_analyze.py --check
```

The rebuild downloads the official archive, verifies its pinned SHA 256, recursively opens nested ZIP files, parses the four MATLAB records, reconstructs all discharge capacity observations, and checks the packaged release.

## Evidence policy

There is no synthetic fallback.

If the official archive changes, a required cell is missing, or any capacity or released forecast differs, the source rebuild fails.
