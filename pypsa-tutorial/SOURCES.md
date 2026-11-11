# Sources, attribution, and reuse

Consulted 6 November 2026.

## PyPSA

- [Official installation](https://docs.pypsa.org/latest/home/installation/).
- [Quickstart 1 — Markets](https://docs.pypsa.org/latest/examples/example-1/): baseline two-zone problem and component API.
- [Quickstart 3 — Investments & Storage](https://docs.pypsa.org/latest/examples/example-3/): Seville setting, cost assumptions, and linked hourly solar profile.
- [PyPSA documentation](https://docs.pypsa.org/): further component and statistics reference.
- [conda installation documentation](https://docs.conda.io/projects/conda/en/stable/user-guide/install/): Miniconda and Miniforge as conda installers.

The notebooks use original explanatory prose, new scenario exercises, and newly generated figures. Source examples are acknowledged rather than reproduced as uncredited text. Values used to reproduce a reference problem remain attributed to that problem.

## Scenario-analysis teaching reference

- [Jansen, PyPSA meets Earth Lab 2026, D — scenario analysis](https://ljansen-iee.github.io/pypsa-meets-earth-lab-2026/notebooks/D_ZA_scenario_analysis.html).
- Code supplied within `Prompts.docx`, including B/C/D notebooks. Supplied metadata identifies adapted PyPSA-Earth/PyPSA-Eur code as AGPL-3.0-or-later and PyPSA-Earth commit `d9c6deb81ed9a03a166ac7acdc15532d8c9ecd4f`.

The collection/statistics and scenario-provenance patterns are adapted with attribution. Python code in the new PyPSA notebooks is provided under [AGPL-3.0-or-later](https://www.gnu.org/licenses/agpl-3.0.html). Preserve this notice and relevant upstream attribution when redistributing adapted code. This does not change the licence of the user's pre-existing course, PyPSA itself, logos, or third-party datasets. The accompanying AGPL licence text applies to the new notebook code.

## OpenStreetMap and geospatial references

- [OpenStreetMap](https://www.openstreetmap.org/), [copyright and ODbL](https://www.openstreetmap.org/copyright).
- [OSM API map extraction](https://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_map_data_by_bounding_box:_GET_/api/0.6/map).
- [OSMnx feature reference](https://osmnx.readthedocs.io/en/stable/user-reference.html#module-osmnx.features).
- [GeoPandas user guide](https://geopandas.org/en/stable/docs/user_guide.html).
- [PDOK](https://www.pdok.nl/), [CBS open data](https://www.cbs.nl/en-gb/our-services/open-data), [3DBAG](https://3dbag.nl/), [Copernicus Data Space](https://dataspace.copernicus.eu/).

The included OSM-derived GeoJSON is credited to © OpenStreetMap contributors and distributed under ODbL. Retrieval and processing details are in `managing-data/data/README.md`. New maps credit the contributors directly on the figure. Third-party library logos retained in the earlier GeoPandas introduction remain their owners' material.

## Solar profile

The investment notebook downloads the CSV linked by the official example:

https://model.energy/data/time-series-f17c3736a2719ce7da58484180d89e2d.csv

The original CSV is not redistributed in this package. The notebook caches it after retrieval and gives an actionable error if the download fails. Its saved outputs were computed using that actual CSV, not a synthetic fallback. The source URL is also saved in each exported scenario's metadata. See `VALIDATION.md` for the input checksum used for these results.
