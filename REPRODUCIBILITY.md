# Reproducibility Guide

## Reproducibility objective

A reader should be able to verify the released findings in two independent ways:

1. offline from the packaged 636 discharge observations;
2. online by rebuilding the evidence from the official NASA archive.

## Environment

```bash
python -m pip install -r requirements.txt
```

## Offline verification

```bash
pytest -q
python run_demo.py
python scripts/generate_figures.py
```

The test suite checks:

- exactly four released battery IDs;
- exactly 636 discharge observations;
- per battery cycle counts;
- fixed checkpoints 40, 60, and 80;
- checkpoints preceding observed threshold crossings;
- exact checkpoint 80 projections;
- observed threshold cycles;
- B0007 false warning behavior;
- aggregate error values;
- complete bundle consistency.

## Official NASA rebuild

```bash
python scripts/fetch_and_analyze.py --check
```

The rebuild:

1. downloads the official NASA Battery Data Set archive;
2. calculates and verifies its SHA 256 digest;
3. recursively expands nested ZIP files;
4. extracts B0005, B0006, B0007, and B0018 MATLAB records;
5. reconstructs discharge capacity series with SciPy;
6. verifies all 636 packaged capacity observations;
7. recomputes all 12 checkpoint forecasts;
8. fails on any evidence or released result mismatch.

## Source integrity

Pinned archive SHA 256:

```text
82302a7db4fc1b34e0b6676326610438d43b816bdf11a69d1d012a464ef2f92e
```

A source change is treated as a release event requiring inspection rather than silently accepted.

## Figure regeneration

The five SVG figures are generated from packaged result files:

```bash
python scripts/generate_figures.py
```

The generator validates SVG XML before writing files.

## Evidence map

| Claim | Primary evidence |
|---|---|
| 636 discharge observations | `data/derived/cycle_capacity_evidence.csv` |
| Observed threshold cycles | `data/derived/battery_summary.csv` |
| 12 checkpoint forecasts | `data/derived/checkpoint_results.csv` |
| MAE and revision summaries | `data/derived/checkpoint_aggregate.csv` |
| Headline release values | `results/empirical_summary.json` |
| Forecast implementation | `research/model.py` |
| Official source agreement | `scripts/fetch_and_analyze.py --check` |

## Failure policy

There is no synthetic fallback.

Missing cells, archive hash drift, capacity mismatch, checkpoint mismatch, or released result inconsistency causes verification failure.

## Reproducibility boundary

Computational reproducibility does not establish general prognostics validity. The released evidence verifies only this model, these cells, these checkpoints, and this threshold definition.
