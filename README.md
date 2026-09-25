# Forecast Maturity of Technical Performance Margin on NASA Li-ion Battery Aging Data

> **Empirical Research Bundle** · **Engineering Management Research** · Systems Engineering / Technical Performance Measures / Prognostics

This study asks a systems-engineering question: **how trustworthy is a threshold forecast at the moment a decision must be made?** It monitors battery capacity margin to NASA's 1.4 Ah end-of-life criterion at fixed 40, 60, and 80-cycle checkpoints, so the analysis does not need to know each cell's eventual lifetime in advance.

![Workflow](assets/architecture.svg)

## Why this release is different

The prototype trained on the first 60% of each cell's final recorded history. That avoided training on the threshold crossing, but the cutoff still depended on knowing the eventual observation horizon. This release removes that retrospective dependency by using the same fixed checkpoints for every battery.

## Research questions

1. How does a transparent linear threshold forecast change as evidence accumulates at cycles 40, 60, and 80?
2. Does threshold-cycle error decrease as the monitoring checkpoint moves closer to the eventual 1.4 Ah crossing?
3. Can a forecast enter the observed operating horizon and still produce a false early warning?

## Data and engineering threshold

NASA's Li-ion aging experiments define end of life as a **30% fade in rated capacity, from 2.0 Ah to 1.4 Ah**. The four cells studied are B0005, B0006, B0007, and B0018. The official NASA PCoE Battery Data Set archive is the canonical rebuild source.

Capacity margin is:

```text
technical performance margin = measured discharge capacity − 1.4 Ah
```

This is a laboratory performance-margin application of TPM monitoring principles, not a claim that battery capacity is a complete project-level TPM.

## Method

At each fixed checkpoint (40, 60, 80 discharge cycles), fit ordinary least squares:

```text
capacity = intercept + slope × discharge_cycle
```

using only observations available at that checkpoint. If slope is negative, solve for the projected cycle at which capacity reaches 1.4 Ah. Later observations are used only for evaluation.

![Method](assets/method.svg)

## Main empirical result

| Checkpoint | MAE across cells with observed crossing | Mean forecast revision | False early warnings |
|---:|---:|---:|---:|
| 40 | 102.399 cycles | — | 0 |
| 60 | 35.852 cycles | 100.046 cycles | 0 |
| 80 | 11.942 cycles | 38.012 cycles | 1 |

Forecasts mature with additional evidence on average, but not uniformly. B0005's projected threshold shifts from **413.782 → 216.817 → 145.025 cycles**. At checkpoint 80, B0007 projects a crossing at **158.219**, inside its 168-cycle observed horizon, yet the cell never reaches 1.4 Ah in the recorded series.

![Checkpoint error](assets/checkpoint_error.svg)

![Forecast revision](assets/forecast_revision.svg)

## Interpretation

The key result is not that a straight line predicts battery EOL well. It is that **forecast maturity is itself a technical quantity worth monitoring**. Early projections can move by tens or hundreds of cycles as additional evidence arrives. A TPM-style dashboard should therefore track both margin to requirement and the stability of the forecast used to anticipate margin exhaustion.

## Claim boundary

**Supported:** descriptive behavior of this transparent baseline on the four NASA cells; fixed-checkpoint forecast error; forecast revisions; B0007 false early warning at checkpoint 80.

**Not supported:** production battery-health management, generalization to other cells or chemistries, calibrated uncertainty, causal claims, or superiority over modern prognostics models.

![Evidence boundary](assets/evaluation.svg)

## Reproduce

Offline:

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
python scripts/generate_figures.py --out-dir /tmp/tpm_figures
```

Official NASA source rebuild:

```bash
python scripts/fetch_and_analyze.py --check
```

The rebuild downloads NASA's official Battery Data Set archive, recursively extracts nested ZIPs, reads B0005/B0006/B0007/B0018 MATLAB files, reconstructs all 636 discharge-capacity observations, and compares them against the packaged evidence.

## Research integrity

This analysis is **not preregistered**. The checkpoint design is a correction to the original retrospective-horizon split. The repository reports the correction explicitly rather than presenting the revised protocol as if it had been specified in advance.
