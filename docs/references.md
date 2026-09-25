# References and Data Sources

## Canonical battery dataset

Saha, B., & Goebel, K. (2007). *Battery Data Set*. NASA Prognostics Data Repository, NASA Ames Research Center, Moffett Field, California.

NASA Open Data Portal. *Li-ion Battery Aging Datasets*. The dataset documents repeated charge, discharge, and impedance measurements and states the end of life criterion as 30% fade from 2.0 Ah rated capacity to 1.4 Ah.

Official archive used by this repository:

`https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip`

## Battery prognostics context

Goebel, K., Saha, B., Saxena, A., Celaya, J. R., & Christophersen, J. P. (2008). Prognostics in battery health management. *IEEE Instrumentation & Measurement Magazine, 11*(4), 33 to 40. https://doi.org/10.1109/MIM.2008.4579269

## Systems engineering and Technical Performance Measures

NASA. *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2.

NASA describes Technical Performance Measures as physical or functional characteristics associated with Measures of Performance that are monitored by comparing actual or best estimated values with anticipated current and future values so deficiencies threatening critical requirements can be identified.

NASA. *NPR 7123.1, NASA Systems Engineering Processes and Requirements*. Technical Performance Measures definition and technical management requirements.

## How the sources are used

The NASA battery source defines the empirical evidence and the 1.4 Ah end of life boundary.

The NASA systems engineering sources motivate the forward looking technical performance monitoring interpretation.

The repository does not claim that battery capacity alone is a complete project level TPM. The work is framed as a TPM style laboratory case study.

## Convenience cross check

An early release was cross checked against `amirhossein-sadeghi2003/battery-health-forecasting-baselines` at commit `e414d2e00ecc369d042637df6a6147a948718649`.

That repository is not the canonical evidence source. The official NASA archive is used for release verification.
