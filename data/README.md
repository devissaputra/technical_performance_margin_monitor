# Data

## Canonical source
NASA Ames Prognostics Center of Excellence Battery Data Set.

Official archive:
`https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip`

Cells used: B0005, B0006, B0007, B0018.

NASA states that the experiments use a 1.4 Ah end-of-life criterion corresponding to 30% fade from 2.0 Ah rated capacity.

## Packaged data
This repository does not bundle the NASA MATLAB files. It packages only compact derived capacity/margin evidence required for offline verification.

## Rebuild
`python scripts/fetch_and_analyze.py --check` downloads the official NASA archive, recursively expands nested ZIP files, extracts the four MATLAB cells, rebuilds the discharge-capacity series, and verifies the packaged results.
