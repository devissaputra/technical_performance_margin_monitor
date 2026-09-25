# Final QA Report

**Release status: PASS after correction.**

## Checks completed
- provenance and source identity reviewed;
- licensing/reuse note recorded;
- derived CSV structure checked against the stated sample and estimand;
- `results/empirical_summary.json` reconciled with packaged evidence;
- README/report language reconciled with the numerical results;
- study-specific methods moved into `research/model.py`;
- tests exercise scientific logic and invariants;
- internet rebuild script has no synthetic fallback;
- four SVG assets regenerated as study-specific figures and XML-validated;
- local Markdown links checked;
- citation metadata points to the final repository slug;
- no preregistration claim is made.

## Final empirical finding
Using only the first 60% of each history, the linear baseline is 5.5 cycles late for B0005, 10.1 cycles early for B0006, and 0.2 cycles late for B0018. For B0007 it predicts a crossing near cycle 150 even though observed capacity remains above 1.4 Ah through cycle 168, a false early threshold prediction.

## Required interpretation boundary
This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.
