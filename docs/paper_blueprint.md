# Paper Blueprint

## Working title

**Forecast Maturity as Decision Evidence in Technical Performance Monitoring: Fixed Checkpoint Analysis of NASA Battery Aging Data**

Alternative title:

**When Does a Threshold Forecast Become Trustworthy? Evidence from NASA Lithium Ion Battery Aging Trajectories**

## Paper identity

This should be written as a compact empirical systems engineering and prognostics decision support paper.

The contribution is not a new remaining useful life model. The paper studies how a simple forecast changes as evidence accumulates and argues that forecast revision should be visible alongside current technical performance margin.

## One sentence contribution

Using four NASA battery trajectories and future independent monitoring checkpoints, the study shows that aggregate threshold forecast error can improve while individual forecasts remain heterogeneous and occasionally generate false early warnings.

## Draft abstract

Technical Performance Measures are intended to help decision makers detect emerging risk before a requirement is missed, but a projected requirement crossing can itself be unstable as evidence accumulates. This study examines forecast maturity using four lithium ion battery aging trajectories from the NASA Ames Prognostics Center of Excellence Battery Data Set. Measured discharge capacity is treated as a laboratory performance parameter with NASA's 1.4 Ah end of life criterion as a requirement like boundary. At fixed checkpoints of 40, 60, and 80 discharge cycles, an ordinary least squares capacity trend is fitted using only observations available at that checkpoint and solved for the projected threshold crossing cycle. Across B0005, B0006, and B0018, which later cross 1.4 Ah, mean absolute threshold cycle error decreases from 102.399 cycles at checkpoint 40 to 35.852 at 60 and 11.942 at 80. Mean absolute forecast revision decreases from 100.046 cycles between checkpoints 40 and 60 to 38.012 cycles between 60 and 80. The aggregate improvement masks heterogeneous cell behavior: B0006 becomes less accurate across the released checkpoints, while B0005 improves sharply. B0007 generates a false early warning at checkpoint 80, projecting a crossing at 158.219 cycles despite remaining above 1.4 Ah through cycle 168. The results support reporting forecast stability alongside projected margin exhaustion rather than treating a point forecast as sufficient technical decision evidence.

## Introduction logic

### Paragraph 1: technical monitoring problem

Systems engineering tracks critical performance measures against expected and required values so emerging deficiencies can be detected before they jeopardize requirements.

### Paragraph 2: forecasting problem

When decision makers rely on a future threshold crossing rather than only current margin, forecast stability becomes part of the evidence.

### Paragraph 3: methodological risk

A forecast evaluated at a cutoff derived from eventual lifetime can accidentally use future information in the analysis design even if future measurements are excluded from model fitting.

### Paragraph 4: contribution

This study uses fixed lifecycle independent checkpoints and explicitly measures both realized error and forecast revision.

## Research questions

**RQ1.** How do threshold crossing projections change across fixed checkpoints?

**RQ2.** Does aggregate threshold cycle error decrease as evidence accumulates?

**RQ3.** Is forecast improvement consistent across individual cells?

**RQ4.** Can the baseline generate an apparently actionable false early warning?

## Data section

Report:

- NASA Ames PCoE Battery Data Set;
- cells B0005, B0006, B0007, B0018;
- 636 discharge observations;
- 1.4 Ah EOL criterion;
- 30% fade from 2.0 Ah rated capacity;
- official archive and pinned SHA 256;
- raw MATLAB files not redistributed.

## Systems engineering framing

Use NASA's definition of TPMs to motivate monitoring of current and future expected performance.

Be precise: this is a **TPM style laboratory case study**. Do not claim that cell capacity alone is a complete project TPM.

## Method section

### Fixed checkpoints

Use cycles 40, 60, and 80 for every cell.

Explain why fixed checkpoints remove dependence on eventual recorded lifetime.

### Forecast model

Fit:

```text
capacity = intercept + slope × cycle
```

to all observations available through the checkpoint.

For negative slope, solve the line for 1.4 Ah.

### Evaluation

For cells with observed crossings:

- signed threshold cycle error;
- absolute error.

For B0007:

- whether projection falls inside the recorded horizon;
- false early warning status.

### Forecast maturity

Report absolute revision between consecutive projected crossing cycles.

Make clear that revision is not calibrated uncertainty.

## Results section

### 1. Observed cell outcomes

Use a table with cycle counts, starting and final capacity, and observed crossing.

### 2. Cell level checkpoint forecasts

Show all 12 projections, not only aggregate MAE.

### 3. Aggregate forecast error

Report MAE and median absolute error at all checkpoints.

Explicitly note that B0005 dominates the checkpoint 40 mean.

### 4. Forecast revision

Report average revisions and selected cell trajectories.

### 5. False warning case

Discuss B0007 separately as a right censored observation.

## Key cell level interpretation

### B0005

Strong maturation example:

```text
413.782 → 216.817 → 145.025
```

Observed crossing: 125.

### B0006

Counterexample to monotonic improvement:

```text
109.346 → 102.975 → 93.434
```

Observed crossing: 109.

Absolute error increases from 0.346 to 15.566 cycles.

### B0018

Late accuracy improves substantially:

```text
78.931 → 106.715 → 96.764
```

Observed crossing: 97.

### B0007

No observed crossing through cycle 168.

Checkpoint 80 projects 158.219, creating a false early warning.

## Discussion

### Main interpretation

Forecast maturity cannot be inferred solely from elapsed observation time.

### Engineering implication

A threshold forecast should be accompanied by revision history or uncertainty evidence so decision makers can distinguish a stable warning from a moving estimate.

### Aggregation implication

A portfolio level average can improve even while one asset's forecast gets worse. Cell level evidence should remain visible.

### Prognostics implication

The transparent linear model creates a useful baseline for evaluating stronger methods, but the present study does not compare models.

## Limitations

Include at least:

1. four cells only;
2. one battery dataset;
3. one EOL threshold;
4. simple linear model;
5. no calibrated uncertainty;
6. no nonlinear degradation model;
7. no cross cell training;
8. no covariates such as temperature or impedance;
9. no decision cost model;
10. mean error sensitivity to B0005 checkpoint 40;
11. B0007 threshold outcome is censored within the recorded horizon;
12. laboratory setting rather than field operation.

## Figures

**Figure 1. Research overview.** Four NASA battery capacity trajectories with the 1.4 Ah boundary, fixed checkpoint markers, and observed crossing labels.

**Figure 2. Fixed checkpoint processing pipeline.** Source data, checkpoint censoring, margin calculation, OLS fit, threshold projection, evaluation, and revision.

**Figure 3. Cell level absolute forecast error at checkpoints.** Show B0005, B0006, and B0018 separately so heterogeneity is visible.

**Figure 4. Forecast revision by checkpoint transition.**

**Figure 5. Evidence and claim boundary.**

## Tables

**Table 1.** Battery trajectory summary.

**Table 2.** All 12 checkpoint projections.

**Table 3.** Aggregate error and revision metrics.

## Writing rules

- Say “projected threshold crossing,” not “predicted failure” unless the distinction is defined.
- Say “TPM style laboratory application,” not “NASA project TPM.”
- Distinguish point forecast revision from uncertainty.
- Report B0006 as a counterexample to monotonic improvement.
- Describe B0007 as no observed crossing within the recorded horizon.
- Do not claim state of the art prognostics performance.
- Do not describe the corrected protocol as preregistered.

## Completion checklist

A manuscript draft is ready for external feedback when:

- all 12 checkpoint forecasts match released evidence;
- aggregate and cell level results are both shown;
- the fixed checkpoint correction is disclosed;
- NASA TPM framing is cited accurately;
- the 1.4 Ah EOL source is cited;
- B0007 censoring is described correctly;
- limitations are explicit;
- repository release or commit is cited.
