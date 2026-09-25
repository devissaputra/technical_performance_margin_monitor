# Empirical Study Protocol

## Study
Forecast Maturity of Technical Performance Margin on NASA Li-ion Battery Aging Data

## Design
Secondary analysis of four NASA PCoE run-to-failure battery trajectories using fixed, lifecycle-independent monitoring checkpoints.

## Research question
How does projected margin-exhaustion timing change as evidence accumulates at fixed 40, 60, and 80-cycle checkpoints?

## Technical performance measure
Measured discharge capacity in ampere-hours. Margin is capacity minus NASA's 1.4 Ah EOL criterion.

## Prospective checkpoint rule
Every battery uses the same checkpoints: cycles 40, 60, and 80. The checkpoint is not computed from the final recorded lifetime, the eventual EOL cycle, or any future observation.

## Forecast
At each checkpoint, fit a straight-line OLS trend to all capacity observations from cycle 1 through the checkpoint. For a negative slope, solve the fitted line for capacity = 1.4 Ah.

## Evaluation
For B0005, B0006, and B0018, compare projected crossing cycle with the first later observed cycle at or below 1.4 Ah. For B0007, which has no observed crossing through cycle 168, identify a false early warning if a projected crossing lies inside the observed horizon.

## Forecast maturity
Forecast revision is the absolute change in projected threshold cycle between consecutive checkpoints. This makes forecast stability an explicit monitoring output instead of hiding it.

## Main result
Across the three cells with observed crossings, MAE declines from 102.399 cycles at checkpoint 40 to 35.852 at 60 and 11.942 at 80. Mean forecast revision declines from 100.046 cycles for 40→60 to 38.012 for 60→80. B0007 still generates a false early warning at checkpoint 80.

## Boundary
The linear model is deliberately transparent and weak. The goal is to study forecast maturity and decision risk, not to claim state-of-the-art battery prognostics.
