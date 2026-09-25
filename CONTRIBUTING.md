# Contributing

Changes should preserve the timing integrity and claim boundaries of the study.

## Scientific changes

If a contribution changes the threshold, checkpoint set, model family, crossing definition, error metric, or released cells, update the protocol and add tests.

Do not silently replace the fixed checkpoint estimand.

## Evidence timing

Forecast fitting must use only observations available at or before the stated checkpoint.

Later observations may be used for evaluation only.

## Right censored outcomes

Do not impute a threshold cycle for a battery that does not cross the boundary within the released horizon.

## Data changes

Preserve official NASA provenance and archive integrity checks.

Do not introduce synthetic fallback data into the official source rebuild.

## Documentation changes

Keep aggregate and cell level results synchronized with the released CSV and JSON evidence.

Do not describe forecast revision as calibrated uncertainty.

## Claim discipline

Do not describe the repository as state of the art battery prognostics, production ready BMS validation, preregistered research, or a complete system level TPM implementation.
