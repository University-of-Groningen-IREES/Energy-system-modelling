# Groningen classroom building extract

Data: **© OpenStreetMap contributors**, available under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). Attribution and licensing: https://www.openstreetmap.org/copyright.

Retrieved 6 November 2026 using one successful small OSM map API request, with bounding box `(6.563, 53.218, 6.571, 53.222)` in longitude/latitude degrees (left, bottom, right, top). Overpass was unavailable during preparation. The file is a dated classroom snapshot, not a full Groningen inventory.

Processing used OSMnx 2.1.1 `features_from_xml(..., tags={"building": True})`. The 665 tagged objects read from the API response contained 664 polygons and one point. The point was excluded. Only nonmissing, nonempty, valid Polygon/MultiPolygon geometries were kept. No invalid geometries were repaired. `osm_id` preserves the element type and identifier. The selected description tags were stored as strings or nulls. Other attributes were dropped. Geometry remains in EPSG:4326. Footprints were not clipped to the request rectangle: objects crossing the rectangle can extend beyond it. Incomplete relations in an API extract may not be reconstructable.

The 664 rows are mapped polygon elements, not certified unique cadastral buildings. Overlap, missing geometry, different representations, and changing tags can affect counts and sums. No measured electricity demand or PV installation data are supplied.

`prepare_osm_extract.py` documents how to request and process a fresh small snapshot. Do not run it repeatedly during class: use the included GeoJSON. A fresh query may produce different rows. Preserve the original snapshot for reproducible lessons. `retrieval-metadata.json` records source checksums and the retrieval details.

When redistributing the OSM-derived database, retain its attribution, ODbL notice, and source information. Maps in this lesson credit the contributors directly.
