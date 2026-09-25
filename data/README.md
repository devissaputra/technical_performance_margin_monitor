# Data

**Primary source:** NASA Ames PCoE Li-ion Battery Aging Dataset (B0005, B0006, B0007, B0018)

**Source page:** https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

**Reuse note:** Primary NASA dataset is public. The convenience CSV is a transparent extraction of NASA MATLAB files; cite NASA/Saha & Goebel and the conversion source.

Raw source observations are not bundled here by default. Derived tables are packaged under `data/derived/`; their completeness or subset status is stated in `docs/data_dictionary.md`.

**Construct boundary:** This is a transparent prognostics baseline, not a validated production health-management model. The processed CSV is a convenience derivative of the NASA source. B0007 demonstrates that a projected crossing inside the observed horizon need not actually occur; projection is not observation.

**Pinned convenience extraction:** `amirhossein-sadeghi2003/battery-health-forecasting-baselines` at commit `e414d2e00ecc369d042637df6a6147a948718649` (`data/processed/discharge_capacity.csv`). Pinning prevents later changes on the third-party `main` branch from silently altering the released analysis.
