# Scientific Report

## Forecast Maturity of Technical Performance Margin on NASA Li-ion Battery Aging Data

### Executive summary

Technical Performance Measures are useful only when decision makers understand both the current performance margin and the reliability of any forecast used to anticipate margin exhaustion. This study examines that second problem using four lithium ion battery aging trajectories from the NASA Ames Prognostics Center of Excellence Battery Data Set.

NASA documents an end of life criterion of 30% fade in rated capacity, from 2.0 Ah to 1.4 Ah. This repository treats measured discharge capacity as a laboratory performance parameter and defines capacity margin as measured capacity minus 1.4 Ah. The analysis does not claim that battery capacity alone is a complete project level Technical Performance Measure.

The four cells are B0005, B0006, B0007, and B0018. Every cell is evaluated at the same fixed checkpoints of 40, 60, and 80 discharge cycles. At each checkpoint, only observations available up to that cycle are used to fit a transparent ordinary least squares trend. The fitted line is then solved for the projected cycle at which capacity would reach 1.4 Ah.

The fixed checkpoint design is important. An earlier prototype used the first 60% of each cell's eventual recorded history. That design was retrospectively dependent on information unavailable at the decision time. The released protocol removes that dependence.

Across the three cells that later cross 1.4 Ah, mean absolute threshold cycle error decreases from 102.399 cycles at checkpoint 40 to 35.852 at checkpoint 60 and 11.942 at checkpoint 80. Mean absolute forecast revision also falls from 100.046 cycles between checkpoints 40 and 60 to 38.012 cycles between checkpoints 60 and 80.

These aggregate trends do not mean every cell improves monotonically. B0006 is already almost exact at checkpoint 40, with a projected crossing of 109.346 cycles versus an observed crossing at 109, but its checkpoint 80 projection moves earlier to 93.434 cycles. B0005 improves dramatically, from a 288.782 cycle error at checkpoint 40 to 20.025 cycles at checkpoint 80. B0018 improves from an 18.069 cycle early error to only 0.236 cycles at checkpoint 80.

B0007 provides the most important warning case. At checkpoint 80, the fitted trend projects a 1.4 Ah crossing at cycle 158.219, which lies inside the recorded 168 cycle horizon. Yet the observed series never reaches 1.4 Ah. The projection is therefore a false early warning under the released rule.

The main contribution is not a claim that linear regression is a strong battery prognostics model. It is a systems engineering demonstration that **forecast maturity is itself decision evidence**. A projected requirement crossing should be accompanied by information about how much that projection has changed as new evidence arrives and how similar forecasts have behaved at comparable checkpoints.

### Research questions

1. How does projected threshold crossing change as evidence accumulates at fixed 40, 60, and 80 cycle checkpoints?
2. Does aggregate threshold cycle error decrease as the monitoring checkpoint moves closer to observed end of life?
3. Are improvements consistent across individual cells?
4. Can a projected crossing enter the observed operating horizon and still become a false early warning?

### Data source

Canonical source: NASA Ames Prognostics Center of Excellence Battery Data Set.

Cells used:

- B0005
- B0006
- B0007
- B0018

The repository packages 636 discharge capacity observations derived from the official NASA archive. It does not redistribute the original MATLAB files.

NASA reports that the experiments were stopped at an end of life criterion corresponding to 30% fade from the 2.0 Ah rated capacity to 1.4 Ah.

### Systems engineering framing

NASA describes Technical Performance Measures as critical or key performance parameters monitored by comparing current achievement with anticipated current and future values so deficiencies can be detected before requirements are jeopardized.

This repository uses that logic in a laboratory setting:

- **performance parameter:** measured discharge capacity;
- **boundary:** 1.4 Ah NASA end of life criterion;
- **current margin:** capacity minus 1.4 Ah;
- **future estimate:** projected cycle of margin exhaustion;
- **forecast maturity evidence:** revision of the projected crossing as checkpoints advance.

This is a TPM style monitoring application, not a claim that discharge capacity by itself constitutes a complete system level TPM.

### Unit of analysis

A discharge cycle nested within one battery cell.

### Fixed checkpoint design

Every cell uses checkpoints at discharge cycles 40, 60, and 80.

The same checkpoints are used regardless of eventual lifetime or threshold crossing. All later observations are hidden from the fitting procedure and used only for evaluation.

### Forecast model

At checkpoint c, the model fits

```text
capacity = intercept + slope × discharge_cycle
```

using discharge cycles 1 through c.

If the fitted slope is negative, the projected threshold cycle is

```text
projected crossing = (1.4 - intercept) / slope
```

No nonlinear model, uncertainty interval, cross cell training, or parameter sharing is used.

### Observed threshold outcomes

| Battery | Recorded cycles | First capacity | Final capacity | First observed ≤ 1.4 Ah |
|---|---:|---:|---:|---:|
| B0005 | 168 | 1.8565 Ah | 1.3251 Ah | 125 |
| B0006 | 168 | 2.0353 Ah | 1.1857 Ah | 109 |
| B0007 | 168 | 1.8911 Ah | 1.4325 Ah | No crossing |
| B0018 | 132 | 1.8550 Ah | 1.3411 Ah | 97 |

### Cell level checkpoint results

| Battery | Checkpoint | Current margin | Projected crossing | Observed crossing | Signed error |
|---|---:|---:|---:|---:|---:|
| B0005 | 40 | 0.3730 Ah | 413.782 | 125 | +288.782 |
| B0005 | 60 | 0.2946 Ah | 216.817 | 125 | +91.817 |
| B0005 | 80 | 0.1649 Ah | 145.025 | 125 | +20.025 |
| B0006 | 40 | 0.3605 Ah | 109.346 | 109 | +0.346 |
| B0006 | 60 | 0.2292 Ah | 102.975 | 109 | -6.025 |
| B0006 | 80 | 0.0888 Ah | 93.434 | 109 | -15.566 |
| B0007 | 40 | 0.4114 Ah | 388.045 | — | — |
| B0007 | 60 | 0.3286 Ah | 218.983 | — | — |
| B0007 | 80 | 0.2212 Ah | 158.219 | No crossing through 168 | False warning |
| B0018 | 40 | 0.2761 Ah | 78.931 | 97 | -18.069 |
| B0018 | 60 | 0.1866 Ah | 106.715 | 97 | +9.715 |
| B0018 | 80 | 0.0479 Ah | 96.764 | 97 | -0.236 |

Positive signed error means the projected crossing is later than the observed crossing. Negative error means the projection is early.

### Aggregate checkpoint results

| Checkpoint | MAE across crossing cells | Median absolute error | Mean forecast revision | False early warnings |
|---:|---:|---:|---:|---:|
| 40 | 102.399 cycles | 18.069 | — | 0 |
| 60 | 35.852 cycles | 9.715 | 100.046 cycles | 0 |
| 80 | 11.942 cycles | 15.566 | 38.012 cycles | 1 |

The falling MAE is heavily influenced by B0005, whose early linear trend projects the crossing far beyond the observed EOL. The median and cell level values should therefore be read alongside the mean.

### Forecast revision

Forecast revision is the absolute change in projected threshold cycle between consecutive checkpoints.

For example, B0005 changes from:

```text
413.782 → 216.817 → 145.025
```

This large revision sequence is useful evidence in its own right. A forecast that repeatedly moves by large amounts should not be communicated to decision makers as if it were stable merely because it returns a precise point estimate.

### B0007 false early warning

B0007 does not cross 1.4 Ah within its 168 recorded discharge cycles.

Its projected crossing changes from 388.045 at cycle 40 to 218.983 at cycle 60 and 158.219 at cycle 80.

Only the cycle 80 projection falls inside the observed horizon. Because no actual crossing occurs, the released analysis marks this as a false early warning.

This result illustrates why an apparently actionable projection should be paired with maturity or uncertainty evidence.

### What this study supports

The release supports these descriptive statements:

- fixed checkpoints eliminate dependence on each cell's eventual recorded lifetime;
- aggregate threshold cycle MAE decreases across the three released checkpoints;
- forecast revisions remain material even at later checkpoints;
- cell level behavior is heterogeneous;
- B0007 produces a false early warning at checkpoint 80 under the linear baseline;
- the complete result is reproducible from the official NASA archive.

### What this study does not support

The analysis does not establish:

- production battery management performance;
- calibrated remaining useful life uncertainty;
- transfer to other chemistries or operating conditions;
- superiority over modern prognostics methods;
- a causal relationship between forecast revision and failure;
- a complete system level TPM framework;
- a decision threshold for when a forecast is sufficiently mature.

### Threats to validity

**Construct validity.** Capacity margin is a useful laboratory performance margin but does not capture the full set of technical measures used in a real system.

**Model validity.** A straight line is deliberately simple and cannot represent all nonlinear aging behavior or recovery effects.

**Sample validity.** Only four NASA cells are included.

**Aggregation validity.** Mean error can be dominated by large errors such as B0005 at checkpoint 40. Cell level results and median error are therefore necessary.

**Outcome validity.** B0007 has a right censored threshold outcome within the released observation horizon. It is evaluated as a false early warning case rather than assigned an artificial crossing.

**Uncertainty validity.** Point forecast revision is not a calibrated prediction interval.

**External validity.** Results do not automatically transfer to different cells, operating profiles, temperatures, chemistries, or field conditions.

### Reproducibility

Offline verification:

```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
python scripts/generate_figures.py
```

Official NASA rebuild:

```bash
python scripts/fetch_and_analyze.py --check
```

The rebuild downloads the official NASA archive, verifies its pinned SHA 256 digest, recursively expands nested archives, extracts the four MATLAB battery records, reconstructs all 636 discharge capacity observations, recomputes all 12 checkpoint forecasts, and compares them with the packaged release.

### Research integrity statement

This is a secondary analysis of public NASA laboratory data. The fixed checkpoint protocol is a documented correction to an earlier retrospective horizon dependent design and must not be described as preregistered.

The linear model is intentionally transparent and should be interpreted as a diagnostic baseline for studying forecast maturity, not as a state of the art prognostics result.
