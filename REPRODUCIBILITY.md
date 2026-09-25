# Reproducibility

## Offline
```bash
python -m pip install -r requirements.txt
pytest -q
python run_demo.py
python scripts/generate_figures.py --out-dir /tmp/tpm_figures
```

Offline tests reconstruct all checkpoint projections from the complete 636-row packaged cycle evidence.

## Official NASA rebuild
```bash
python scripts/fetch_and_analyze.py --check
```

This downloads the NASA Battery Data Set ZIP, recursively expands nested ZIPs, finds B0005/B0006/B0007/B0018 MATLAB files, extracts discharge capacity with SciPy, prints the archive SHA-256, and compares the rebuilt series and results with the packaged release.

## Failure policy
There is no synthetic fallback. Missing cells, source drift, extraction mismatch, or result mismatch causes a non-zero exit.
